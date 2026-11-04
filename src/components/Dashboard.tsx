'use client';

import { useState, useEffect, useMemo, useRef } from 'react';
import Sidebar from './Sidebar';
import ClientSummarySection, { GhlTagLeadCounts } from './ClientSummarySection';
import { ClientEmailMatches } from './PMSAnalysisSection';
import FacebookStatsSection from './FacebookStatsSection';
import PMSAnalysisSection from './PMSAnalysisSection';
import FlagPanel from './FlagPanel';
import PeriodOverviewSection from './PeriodOverviewSection';
import DataStatusPanel from './DataStatusPanel';
import FinalizedReportingSummarySection from './FinalizedReportingSummarySection';
import ClientMonthlyComparisonSection from './ClientMonthlyComparisonSection';
import { ProcessedData, ClientData } from '@/types';
import { loadManifest, loadPeriod, Manifest, ManifestClient, ManifestPeriod } from '@/lib/analysis/autoLoader';
import { FINALIZED_PERIODS, FinalizedPeriod, isFinal, periodSortKey } from '@/lib/analysis/finalizedPeriods';
import { computeCampaignRevenue } from '@/lib/analysis/campaignRevenue';
import { AlertCircle, Loader2, ChevronDown } from 'lucide-react';
import { Badge } from './ui/Badge';

// A month in the period selector: either a live-synced manifest period, a
// finalized snapshot, or both (finalized wins for rendering).
interface DashboardPeriod {
  id: string;
  label: string;
  clients: ManifestClient[];
  manifest?: ManifestPeriod;
  finalized?: FinalizedPeriod;
}

interface Snapshot {
  period: { id: string; label: string; clients: ManifestClient[] };
  data: ProcessedData;
}

// Finalized months first (newest), then live-synced months not finalized yet.
function mergePeriods(manifest: Manifest | null): DashboardPeriod[] {
  const byId = new Map<string, DashboardPeriod>();
  for (const p of manifest?.periods ?? []) {
    byId.set(p.id, { id: p.id, label: p.label, clients: p.clients, manifest: p });
  }
  for (const f of FINALIZED_PERIODS) {
    const existing = byId.get(f.id);
    byId.set(f.id, { id: f.id, label: f.label, clients: existing?.clients ?? [], manifest: existing?.manifest, finalized: f });
  }
  return [...byId.values()].sort((a, b) => periodSortKey(b.id) - periodSortKey(a.id));
}

type View = 'overview' | 'client' | 'compare';

// The selected month, client and view live in the URL (?period=&client=&view=)
// so a refresh, a shared link or a month switch keeps the page you were on
// (Nicole, Nov 2026). Read once on load, written on every change.
function readUrlState(): { period: string | null; client: string | null; view: View | null } {
  if (typeof window === 'undefined') return { period: null, client: null, view: null };
  const params = new URLSearchParams(window.location.search);
  const view = params.get('view');
  return {
    period: params.get('period'),
    client: params.get('client'),
    view: view === 'client' || view === 'compare' || view === 'overview' ? view : null,
  };
}

function writeUrlState(period: string, client: string, view: View) {
  if (typeof window === 'undefined') return;
  const params = new URLSearchParams();
  params.set('period', period);
  if (view !== 'overview' && client) {
    params.set('client', client);
    params.set('view', view);
  }
  const next = `${window.location.pathname}?${params.toString()}`;
  if (`${window.location.pathname}${window.location.search}` !== next) {
    window.history.replaceState(null, '', next);
  }
}

export default function Dashboard() {
  const [manifest, setManifest] = useState<Manifest | null>(null);
  const [manifestReady, setManifestReady] = useState(false);
  const [data, setData] = useState<ProcessedData | null>(null);
  // Client list of the loaded period (from the snapshot for finalized months).
  const [loadedClients, setLoadedClients] = useState<ManifestClient[] | null>(null);
  const [selectedPeriodId, setSelectedPeriodId] = useState<string>('');
  const [selectedClient, setSelectedClient] = useState<string>('');
  const [activeView, setActiveView] = useState<View>('overview');
  // Client/view the URL asked for on first load, applied once the period's data is in.
  const pendingUrlState = useRef<{ client: string | null; view: View | null } | null>(null);
  // Current selection, readable from the period-load effect without re-running it.
  const selectionRef = useRef<{ client: string; view: View }>({ client: '', view: 'overview' });
  useEffect(() => {
    selectionRef.current = { client: selectedClient, view: activeView };
  }, [selectedClient, activeView]);
  // Every finalized snapshot loaded so far, for the month-by-month view;
  // ids whose fetch failed are remembered so they are not retried every render.
  const [snapshotCache, setSnapshotCache] = useState<Record<string, ProcessedData>>({});
  const [snapshotFailed, setSnapshotFailed] = useState<Record<string, true>>({});

  function scrollToTop() {
    document.getElementById('main-scroll')?.scrollTo({ top: 0, behavior: 'instant' });
  }

  function goToClient(name: string) {
    setSelectedClient(name);
    setActiveView('client');
    scrollToTop();
  }
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  // Live GHL tag counts, keyed periodId -> clientName -> tag -> count.
  // Generated by scripts/sync-ghl-lead-counts.mts; optional (older checkouts
  // or environments without GHL creds simply show the placeholder cards).
  const [ghlLeadCounts, setGhlLeadCounts] = useState<Record<string, Record<string, GhlTagLeadCounts>> | null>(null);
  // Ads/Organic email-match analysis, keyed periodId -> clientName
  // (sync-ghl-email-matches.mts; optional like the lead counts).
  const [emailMatches, setEmailMatches] = useState<Record<string, Record<string, ClientEmailMatches>> | null>(null);

  useEffect(() => {
    fetch('/data/ghl-lead-counts.json')
      .then((res) => (res.ok ? res.json() : null))
      .then((d) => setGhlLeadCounts(d?.periods ?? null))
      .catch(() => setGhlLeadCounts(null));
    fetch('/data/ghl-email-matches.json')
      .then((res) => (res.ok ? res.json() : null))
      .then((d) => setEmailMatches(d?.periods ?? null))
      .catch(() => setEmailMatches(null));
  }, []);

  useEffect(() => {
    // The manifest is optional: finalized months render from their snapshots
    // even when the platform sync hasn't run (no manifest on disk).
    loadManifest()
      .catch((): Manifest => ({ periods: [] }))
      .then((m) => {
        setManifest(m);
        const merged = mergePeriods(m);
        const url = readUrlState();
        pendingUrlState.current = { client: url.client, view: url.view };
        const fromUrl = url.period ? merged.find((p) => p.id === url.period) : undefined;
        const first = fromUrl ?? merged[0];
        if (first) setSelectedPeriodId(first.id);
      })
      .finally(() => setManifestReady(true));
  }, []);

  const periods: DashboardPeriod[] = useMemo(() => mergePeriods(manifest), [manifest]);

  useEffect(() => {
    if (!selectedPeriodId) return;
    const period = periods.find((p) => p.id === selectedPeriodId);
    if (!period) return;

    setLoading(true);
    setError(null);
    setData(null);
    setLoadedClients(null);
    scrollToTop();

    const load: Promise<{ data: ProcessedData; clients: ManifestClient[] }> = period.finalized
      ? fetch(period.finalized.snapshot)
          .then((res) => {
            if (!res.ok) throw new Error(`Could not load ${period.label} snapshot (${res.status})`);
            return res.json() as Promise<Snapshot>;
          })
          .then((snap) => ({ data: snap.data, clients: snap.period.clients }))
      : period.manifest
        ? loadPeriod(period.manifest).then((d) => ({ data: d, clients: period.clients }))
        : Promise.reject(new Error(`No data source for ${period.label}`));

    load
      .then(({ data: result, clients }) => {
        setData(result);
        setLoadedClients(clients);
        if (period.finalized) {
          setSnapshotCache((cache) => (cache[period.id] ? cache : { ...cache, [period.id]: result }));
        }
        // Keep the client you were looking at (or the one the URL named) when
        // it exists in this month; otherwise land on the Overview rather than
        // the manifest's first client.
        const pending = pendingUrlState.current;
        pendingUrlState.current = null;
        const wantedClient = pending?.client ?? selectionRef.current.client;
        const wantedView = pending?.view ?? selectionRef.current.view;
        if (wantedClient && result.clients[wantedClient] && wantedView !== 'overview') {
          setSelectedClient(wantedClient);
          setActiveView(wantedView);
          return;
        }
        setActiveView('overview');
        const firstClient = clients[0]?.name;
        if (firstClient && result.clients[firstClient]) {
          setSelectedClient(firstClient);
        } else {
          const first = Object.keys(result.clients)[0];
          if (first) setSelectedClient(first);
        }
      })
      .catch((err) => setError(String(err)))
      .finally(() => setLoading(false));
  }, [periods, selectedPeriodId]);

  const currentPeriod = periods.find((p) => p.id === selectedPeriodId);
  const isFinalized = !!currentPeriod?.finalized;

  // Mirror the selection into the URL once the month has loaded.
  useEffect(() => {
    if (loading || !selectedPeriodId) return;
    writeUrlState(selectedPeriodId, selectedClient, activeView);
  }, [loading, selectedPeriodId, selectedClient, activeView]);

  // The month-by-month view needs every finalized snapshot; fetch the missing
  // ones the first time it opens and keep them for the session.
  useEffect(() => {
    if (activeView !== 'compare') return;
    const missing = FINALIZED_PERIODS.filter((p) => !snapshotCache[p.id] && !snapshotFailed[p.id]);
    if (missing.length === 0) return;
    let cancelled = false;
    Promise.all(
      missing.map((p) =>
        fetch(p.snapshot)
          .then((res) => (res.ok ? (res.json() as Promise<Snapshot>) : null))
          .then((snap) => [p.id, snap?.data ?? null] as const)
          .catch(() => [p.id, null] as const),
      ),
    ).then((entries) => {
      if (cancelled) return;
      setSnapshotCache((cache) => {
        const next = { ...cache };
        for (const [id, d] of entries) if (d) next[id] = d;
        return next;
      });
      setSnapshotFailed((failed) => {
        const next = { ...failed };
        for (const [id, d] of entries) if (!d) next[id] = true;
        return next;
      });
    });
    return () => {
      cancelled = true;
    };
    // The caches are read, not triggers: re-running on every cache update would refetch nothing but churn.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeView]);

  const loadingAllSnapshots =
    activeView === 'compare' && FINALIZED_PERIODS.some((p) => !snapshotCache[p.id] && !snapshotFailed[p.id]);

  // Ordered client list: alphabetical. Live months list clients with ad data;
  // finalized months also list PMS-only clients, as their month pages did.
  const orderedClients: ClientData[] = useMemo(() => {
    if (!data) return [];
    return Object.values(data.clients)
      .filter((c) => c.facebookStats != null || (isFinalized && c.pmsAnalysis != null))
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [data, isFinalized]);

  const currentClient = data && selectedClient ? data.clients[selectedClient] : null;
  const clientFlags = data ? data.flags.filter((f) => f.clientName === selectedClient) : [];

  // Revenue attributed to each campaign type
  const campaignRevenue = useMemo(() => computeCampaignRevenue(currentClient), [currentClient]);

  const ghlTagLeads = ghlLeadCounts?.[selectedPeriodId]?.[selectedClient] ?? null;
  const clientEmailMatches = emailMatches?.[selectedPeriodId]?.[selectedClient] ?? null;

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      {!loading && !error && orderedClients.length > 0 && (
        <div className="bg-[var(--surface-strong)] border-r border-[var(--border)] flex flex-col overflow-hidden flex-shrink-0 w-[220px]">
          <Sidebar
            clients={orderedClients}
            selectedClient={activeView !== 'overview' ? selectedClient : ''}
            onSelectClient={(name) => goToClient(name)}
            periodLabel={currentPeriod?.label}
          />
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 overflow-y-auto july-scrollbar" id="main-scroll">
        {/* Top bar */}
        {!loading && !error && data && (
          <div className="sticky top-0 z-10 bg-[var(--surface)] border-b border-[var(--border)] px-8 py-3 flex items-center justify-between gap-4">
            {/* View tabs */}
            <div className="flex items-center gap-1">
              <button
                onClick={() => setActiveView('overview')}
                className={`px-3.5 py-2 text-[13px] font-semibold rounded-[8px] transition-colors duration-150 ${activeView === 'overview' ? 'bg-[var(--brand-bg)] text-[var(--brand-text)]' : 'text-[var(--muted)] hover:text-[var(--foreground)] hover:bg-[var(--fill-cool)]'}`}
              >
                Overview
              </button>
              <button
                onClick={() => setActiveView('client')}
                className={`flex items-center gap-2 px-3.5 py-2 text-[13px] font-semibold rounded-[8px] transition-colors duration-150 ${activeView === 'client' ? 'bg-[var(--brand-bg)] text-[var(--brand-text)]' : 'text-[var(--muted)] hover:text-[var(--foreground)] hover:bg-[var(--fill-cool)]'}`}
              >
                {activeView === 'client' && currentClient ? (
                  <>
                    {selectedClient}
                    <div className="flex gap-1">
                      {currentClient.facebookStats && <Badge variant="info">Facebook</Badge>}
                      {currentClient.pmsAnalysis && <Badge variant="success">PMS</Badge>}
                      {currentClient.hasGHL && <Badge variant="neutral">GHL</Badge>}
                    </div>
                    {clientFlags.length > 0 && <Badge variant="warning">{clientFlags.length} flag{clientFlags.length !== 1 ? 's' : ''}</Badge>}
                  </>
                ) : 'Client View'}
              </button>
              {currentClient && (
                <button
                  onClick={() => { setActiveView('compare'); scrollToTop(); }}
                  title={`${selectedClient}: key metrics for every month, with the change against the month before`}
                  className={`px-3.5 py-2 text-[13px] font-semibold rounded-[8px] transition-colors duration-150 ${activeView === 'compare' ? 'bg-[var(--brand-bg)] text-[var(--brand-text)]' : 'text-[var(--muted)] hover:text-[var(--foreground)] hover:bg-[var(--fill-cool)]'}`}
                >
                  Month by month
                </button>
              )}
            </div>

            <div className="flex items-center gap-3">
            <a
              href="/weekly/"
              className="px-3.5 py-2 text-[13px] font-semibold rounded-[8px] text-[var(--muted)] hover:text-[var(--foreground)] hover:bg-[var(--fill-cool)] transition-colors duration-150"
            >
              Weekly reviews
            </a>
            {currentPeriod?.finalized && isFinal(currentPeriod.finalized) && (
              <span title={`Numbers signed off ${currentPeriod.finalized.finalizedOn}. Rendered from the frozen snapshot and the Client Performance Tracking sheet.`}>
                <Badge variant="success">Final</Badge>
              </span>
            )}
            {/* Period selector (only if multiple periods) */}
            {periods.length > 1 && (
              <div className="relative">
                <select
                  value={selectedPeriodId}
                  onChange={(e) => setSelectedPeriodId(e.target.value)}
                  className="appearance-none text-[13px] font-semibold border border-[var(--border-strong)] rounded-[12px] pl-4 pr-9 py-2 bg-[var(--surface-strong)] text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--brand)] shadow-[var(--shadow-xs)]"
                >
                  {periods.map((p) => (
                    <option key={p.id} value={p.id}>{p.label}{p.finalized && isFinal(p.finalized) ? ' · Final' : ''}</option>
                  ))}
                </select>
                <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[var(--muted-soft)]" />
              </div>
            )}
            </div>
          </div>
        )}

        {/* Overview tab */}
        {!loading && !error && data && activeView === 'overview' && (
          <PeriodOverviewSection
            manifestClients={loadedClients ?? currentPeriod?.clients ?? []}
            data={data}
            onSelectClient={(name) => goToClient(name)}
          />
        )}

        <div className="px-8 py-8 max-w-5xl space-y-6">
          {/* Loading */}
          {loading && (
            <div className="flex flex-col items-center justify-center py-40 gap-4">
              <Loader2 className="w-7 h-7 text-[var(--muted-soft)] animate-spin" />
              <p className="text-[13px] text-[var(--muted-soft)]">
                {!manifestReady
                  ? 'Loading data...'
                  : currentPeriod?.finalized
                    ? `Loading ${currentPeriod.label} snapshot...`
                    : `Processing ${currentPeriod?.label ?? 'data'}...`}
              </p>
            </div>
          )}

          {/* Error */}
          {error && !loading && (
            <div className="max-w-lg p-6 bg-[var(--err-bg)] border border-[var(--err-border)] rounded-[12px] flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-[var(--danger)] flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-[var(--danger)] text-[13px]">Failed to load data</p>
                <p className="text-[13px] text-[var(--err-text)] mt-1">{error}</p>
              </div>
            </div>
          )}

          {/* Month-by-month comparison for the selected client */}
          {!loading && !error && currentClient && activeView === 'compare' && (
            <ClientMonthlyComparisonSection
              clientName={selectedClient}
              periods={FINALIZED_PERIODS}
              snapshots={snapshotCache}
              loading={loadingAllSnapshots}
              currentPeriodId={selectedPeriodId}
              onSelectPeriod={(id) => {
                setActiveView('client');
                if (id !== selectedPeriodId) setSelectedPeriodId(id);
                scrollToTop();
              }}
            />
          )}

          {/* Client content */}
          {!loading && !error && currentClient && activeView === 'client' && (
            <>
              {currentPeriod?.finalized && isFinal(currentPeriod.finalized) ? (
                /* Signed-off month: sheet revenue + leads, AM note, no sync diagnostics */
                <FinalizedReportingSummarySection
                  clientName={currentClient.name}
                  period={currentPeriod.finalized}
                  facebookStats={currentClient.facebookStats}
                  pmsSummary={currentClient.pmsAnalysis?.summary ?? null}
                  campaignRevenue={campaignRevenue}
                  instagramLeads={currentClient.pmsAnalysis?.instagram ?? null}
                  facebookLeads={currentClient.pmsAnalysis?.facebook ?? null}
                />
              ) : (
                <>
                  {/* Data status diagnostics */}
                  <DataStatusPanel
                    hasPMS={currentClient.hasPMS}
                    hasGHL={currentClient.hasGHL}
                    flags={clientFlags}
                  />

                  {/* Summary bar */}
                  <ClientSummarySection
                    facebookStats={currentClient.facebookStats}
                    pmsSummary={currentClient.pmsAnalysis?.summary ?? null}
                    campaignRevenue={campaignRevenue}
                    instagramLeads={currentClient.pmsAnalysis?.instagram ?? null}
                    facebookLeads={currentClient.pmsAnalysis?.facebook ?? null}
                    ghlTagLeads={ghlTagLeads}
                  />
                </>
              )}

              {currentClient.facebookStats && (
                <FacebookStatsSection
                  key={selectedClient}
                  stats={currentClient.facebookStats}
                  campaignRevenue={campaignRevenue}
                  instagramLeads={currentClient.pmsAnalysis?.instagram ?? null}
                  facebookLeads={currentClient.pmsAnalysis?.facebook ?? null}
                  avgDirectBookingValue={currentClient.pmsAnalysis?.summary.avgDirectBookingValue}
                />
              )}

              {currentClient.pmsAnalysis && (
                <PMSAnalysisSection
                  analysis={currentClient.pmsAnalysis}
                  facebookStats={currentClient.facebookStats}
                  emailMatches={clientEmailMatches}
                />
              )}

              {!currentClient.facebookStats && !currentClient.pmsAnalysis && (
                <div className="rounded-[12px] border border-dashed border-[var(--border-strong)] px-8 py-16 text-center">
                  <p className="text-[13px] text-[var(--muted-soft)]">No data available for this client.</p>
                </div>
              )}

              {/* Per-client flags */}
              {clientFlags.length > 0 && <FlagPanel flags={clientFlags} />}
            </>
          )}

        </div>
      </div>
    </div>
  );
}
