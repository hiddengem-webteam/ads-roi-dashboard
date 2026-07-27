'use client';

import { useState, useEffect, useMemo } from 'react';
import Sidebar from './Sidebar';
import ClientSummarySection from './ClientSummarySection';
import FacebookStatsSection from './FacebookStatsSection';
import PMSAnalysisSection from './PMSAnalysisSection';
import FlagPanel from './FlagPanel';
import SyncPanel from './SyncPanel';
import PeriodOverviewSection from './PeriodOverviewSection';
import DataStatusPanel from './DataStatusPanel';
import { ProcessedData, ClientData } from '@/types';
import { loadManifest, loadPeriod, Manifest } from '@/lib/analysis/autoLoader';
import { AlertCircle, Loader2, ChevronDown } from 'lucide-react';
import { Badge } from './ui/Badge';

export default function Dashboard() {
  const [manifest, setManifest] = useState<Manifest | null>(null);
  const [data, setData] = useState<ProcessedData | null>(null);
  const [selectedPeriodId, setSelectedPeriodId] = useState<string>('');
  const [selectedClient, setSelectedClient] = useState<string>('');
  const [activeView, setActiveView] = useState<'overview' | 'client'>('overview');

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

  useEffect(() => {
    loadManifest()
      .then((m) => {
        setManifest(m);
        if (m.periods.length > 0) setSelectedPeriodId(m.periods[0].id);
      })
      .catch((err) => setError(String(err)))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!manifest || !selectedPeriodId) return;
    const period = manifest.periods.find((p) => p.id === selectedPeriodId);
    if (!period) return;

    setLoading(true);
    setError(null);
    setData(null);

    loadPeriod(period)
      .then((result) => {
        setData(result);
        // Default to first client in manifest order
        const firstClient = period.clients[0]?.name;
        if (firstClient && result.clients[firstClient]) {
          setSelectedClient(firstClient);
        } else {
          const first = Object.keys(result.clients)[0];
          if (first) setSelectedClient(first);
        }
      })
      .catch((err) => setError(String(err)))
      .finally(() => setLoading(false));
  }, [manifest, selectedPeriodId]);

  // Ordered client list: alphabetical, FB-only clients
  const orderedClients: ClientData[] = useMemo(() => {
    if (!data) return [];
    return Object.values(data.clients)
      .filter((c) => c.facebookStats != null)
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [data]);

  const currentClient = data && selectedClient ? data.clients[selectedClient] : null;
  const clientFlags = data ? data.flags.filter((f) => f.clientName === selectedClient) : [];
  const currentPeriod = manifest?.periods.find((p) => p.id === selectedPeriodId);

  // Revenue attributed to each campaign type
  const campaignRevenue = useMemo(() => {
    const codes = currentClient?.pmsAnalysis?.promoCode.codes ?? [];

    // Build set of PMS emails already attributed to New Leads (FB lead matches).
    // When both campaigns are running, a guest matched in FB leads takes priority
    // over any promo code they also used — so we exclude them from Followers.
    const fbLeadEmailSet = new Set<string>();
    for (const match of (currentClient?.pmsAnalysis?.facebook.matches ?? [])) {
      if (match.pmsEmail) fbLeadEmailSet.add(match.pmsEmail.toLowerCase().trim());
    }

    let followers = 0;
    let followersUses = 0;
    let followersDeduped = 0; // guests moved to New Leads
    for (const code of codes) {
      const ct = code.campaignType.toLowerCase();
      if (ct.includes('follower')) {
        for (const guest of code.guests) {
          if (guest.isZeroRevenue) continue;
          const email = guest.email?.toLowerCase().trim();
          if (email && fbLeadEmailSet.has(email)) {
            followersDeduped++;
            continue; // already attributed to New Leads
          }
          followers += guest.revenue;
          followersUses++;
        }
      }
    }

    // Retargeting: FB purchase events × avg direct booking value
    const avgBookingValue = currentClient?.pmsAnalysis?.summary.avgDirectBookingValue ?? 0;
    const retargetingPurchases = currentClient?.facebookStats?.retargeting?.purchases ?? 0;
    const retargeting = retargetingPurchases * avgBookingValue;

    // New Leads: revenue from matched Facebook leads in PMS
    const newLeads = currentClient?.pmsAnalysis?.facebook.totalRevenue ?? 0;

    return { followers, followersUses, followersDeduped, retargeting, newLeads };
  }, [currentClient]);

  return (
    <div className="flex h-screen bg-[#f8f8f7] overflow-hidden">
      {/* Sidebar */}
      {!loading && !error && orderedClients.length > 0 && (
        <div className="bg-white border-r border-gray-100 flex flex-col overflow-hidden flex-shrink-0 w-[220px]">
          <Sidebar
            clients={orderedClients}
            selectedClient={activeView === 'client' ? selectedClient : ''}
            onSelectClient={(name) => goToClient(name)}
            periodLabel={currentPeriod?.label}
          />
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 overflow-y-auto" id="main-scroll">
        {/* Top bar */}
        {!loading && !error && data && (
          <div className="sticky top-0 z-10 bg-[#f8f8f7]/90 backdrop-blur-sm border-b border-gray-100 px-8 py-3 flex items-center justify-between gap-4">
            {/* View tabs */}
            <div className="flex items-center gap-1">
              <button
                onClick={() => setActiveView('overview')}
                className={`px-3 py-1.5 text-sm font-medium rounded-lg transition-colors ${activeView === 'overview' ? 'bg-gray-900 text-white' : 'text-gray-500 hover:text-gray-700'}`}
              >
                Overview
              </button>
              <button
                onClick={() => setActiveView('client')}
                className={`flex items-center gap-2 px-3 py-1.5 text-sm font-medium rounded-lg transition-colors ${activeView === 'client' ? 'bg-gray-900 text-white' : 'text-gray-500 hover:text-gray-700'}`}
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
            </div>

            {/* Period selector (only if multiple periods) */}
            {manifest && manifest.periods.length > 1 && (
              <div className="relative">
                <select
                  value={selectedPeriodId}
                  onChange={(e) => setSelectedPeriodId(e.target.value)}
                  className="appearance-none text-sm font-medium border border-gray-200 rounded-xl pl-4 pr-9 py-2 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-900 shadow-sm"
                >
                  {manifest.periods.map((p) => (
                    <option key={p.id} value={p.id}>{p.label}</option>
                  ))}
                </select>
                <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-400" />
              </div>
            )}
          </div>
        )}

        {/* Overview tab */}
        {!loading && !error && data && activeView === 'overview' && (
          <PeriodOverviewSection
            manifestClients={currentPeriod?.clients ?? []}
            data={data}
            onSelectClient={(name) => goToClient(name)}
          />
        )}

        <div className="px-8 py-8 max-w-5xl space-y-6">
          {/* Loading */}
          {loading && (
            <div className="flex flex-col items-center justify-center py-40 gap-4">
              <Loader2 className="w-7 h-7 text-gray-300 animate-spin" />
              <p className="text-sm text-gray-400">
                {!manifest ? 'Loading data...' : `Processing ${currentPeriod?.label ?? 'data'}...`}
              </p>
            </div>
          )}

          {/* Error */}
          {error && !loading && (
            <div className="max-w-lg p-6 bg-red-50 border border-red-100 rounded-2xl flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-red-700 text-sm">Failed to load data</p>
                <p className="text-sm text-red-500 mt-1">{error}</p>
              </div>
            </div>
          )}

          {/* Client content */}
          {!loading && !error && currentClient && activeView === 'client' && (
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
              />

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
                <PMSAnalysisSection analysis={currentClient.pmsAnalysis} />
              )}

              {!currentClient.facebookStats && !currentClient.pmsAnalysis && (
                <div className="rounded-2xl border border-dashed border-gray-200 px-8 py-16 text-center">
                  <p className="text-sm text-gray-400">No data available for this client.</p>
                </div>
              )}

              {/* Per-client flags */}
              {clientFlags.length > 0 && <FlagPanel flags={clientFlags} />}
            </>
          )}

          <SyncPanel />
        </div>
      </div>
    </div>
  );
}
