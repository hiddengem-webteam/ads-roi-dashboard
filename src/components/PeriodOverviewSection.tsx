'use client';

import { ProcessedData, Flag } from '@/types';
import { AlertTriangle, ChevronRight, Info } from 'lucide-react';
import { Badge } from './ui/Badge';
import { accountManagerFor, matchesAm, NO_AM } from '@/lib/accountManagers';

interface ManifestClient {
  name: string;
  pms?: string;
  ghl?: string;
  /** PMS provider (guesty/hostaway/hospitable/uplisting) from the platform sync */
  pmsProvider?: string;
}

interface PeriodOverviewSectionProps {
  manifestClients: ManifestClient[];
  data: ProcessedData;
  onSelectClient: (name: string) => void;
  /** Period id (e.g. "october-2026") and label, for the header's date range. */
  periodId: string;
  periodLabel: string;
  /** Account manager filter from the sidebar ('' = everyone). */
  amFilter: string;
}

type Status = 'ok' | 'missing' | 'none';

const MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
const MONTHS_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

/** "october-2026" -> "1 Oct – 31 Oct 2026"; anything else falls back to the period label. */
export function periodRange(id: string, label: string): string {
  const m = /^([a-z]+)-(\d{4})$/.exec(id);
  const i = m ? MONTHS.indexOf(m[1]) : -1;
  if (!m || i < 0) return label;
  const year = Number(m[2]);
  const last = new Date(year, i + 1, 0).getDate();
  return `1 ${MONTHS_SHORT[i]} – ${last} ${MONTHS_SHORT[i]} ${year}`;
}

function StatusCell({ status }: { status: Status }) {
  if (status === 'ok') return <Badge variant="success">Synced</Badge>;
  if (status === 'missing') return <Badge variant="error">Missing</Badge>;
  return <span className="text-[var(--muted-soft)]">—</span>;
}

/** Flag text without the leading "Client name: ". */
function flagText(f: Flag): string {
  const prefix = `${f.clientName}: `;
  return f.message.startsWith(prefix) ? f.message.slice(prefix.length) : f.message;
}

export default function PeriodOverviewSection({
  manifestClients,
  data,
  onSelectClient,
  periodId,
  periodLabel,
  amFilter,
}: PeriodOverviewSectionProps) {
  // Unified client list: manifest clients (spend-sorted) first, then FB-only extras alphabetically
  const manifestNames = new Set(manifestClients.map((c) => c.name));
  const fbOnlyExtras = Object.keys(data.clients).filter((n) => !manifestNames.has(n)).sort();
  const orderedNames = [
    ...manifestClients.map((c) => c.name).filter((n) => data.clients[n] || manifestClients.find((mc) => mc.name === n)),
    ...fbOnlyExtras,
  ];

  const rows = orderedNames.map((name) => {
    const client = data.clients[name];
    const mc = manifestClients.find((c) => c.name === name);
    const fb: Status = client?.facebookStats ? 'ok' : 'none';
    const pms: Status = client?.pmsAnalysis ? 'ok' : mc?.pms ? 'missing' : 'none';
    // GHL is missing only if the manifest names a GHL file that didn't load
    const ghl: Status = client?.hasGHL ? 'ok' : mc?.ghl ? 'missing' : 'none';
    return { name, client, mc, fb, pms, ghl, am: accountManagerFor(name) };
  });

  // A flag type raised for every client with data says one thing about the month, not about each
  // client (finalized months have no GHL files, so "No GHL data file" lands on all of them). Show it
  // once as a note and keep it out of the per-client counts.
  const withData = new Set(rows.filter((r) => r.client).map((r) => r.name));
  const clientsByType = new Map<string, Set<string>>();
  for (const f of data.flags) {
    if (!clientsByType.has(f.type)) clientsByType.set(f.type, new Set());
    clientsByType.get(f.type)!.add(f.clientName);
  }
  const monthWide = new Set(
    [...clientsByType].filter(([, names]) => withData.size > 1 && [...withData].every((n) => names.has(n))).map(([t]) => t),
  );
  // "No GHL data file" is raised for every client with PMS data; when no client has GHL at all this
  // month (every finalized month), it is a fact about the month too.
  if (clientsByType.has('missing-ghl') && !rows.some((r) => r.client?.hasGHL)) monthWide.add('missing-ghl');
  const monthNotes = [...monthWide].map((type) => {
    const sample = data.flags.find((f) => f.type === type)!;
    const n = data.flags.filter((f) => f.type === type).length;
    return type === 'missing-ghl'
      ? `No GHL data this month, so lead matching is unavailable for every client (${n} flags).`
      : `Every client: ${flagText(sample)} (${n} flags).`;
  });
  const flagsByClient: Record<string, Flag[]> = {};
  for (const f of data.flags) {
    if (monthWide.has(f.type)) continue;
    (flagsByClient[f.clientName] ??= []).push(f);
  }

  // Columns that are empty for every client this month are left out
  const showProvider = rows.some((r) => r.mc?.pmsProvider);
  const showGhl = rows.some((r) => r.ghl !== 'none');

  const shown = rows.filter((r) => matchesAm(r.name, amFilter));
  const flagCount = shown.reduce((n, r) => n + (flagsByClient[r.name]?.length ?? 0), 0);
  const stats = [
    { label: 'Clients', value: shown.length, hint: amFilter ? `of ${rows.length}` : 'in this month' },
    { label: 'With Facebook', value: shown.filter((r) => r.fb === 'ok').length, hint: 'ad data synced' },
    { label: 'With PMS', value: shown.filter((r) => r.pms === 'ok').length, hint: 'bookings synced' },
    ...(showGhl ? [{ label: 'With GHL', value: shown.filter((r) => r.ghl === 'ok').length, hint: 'leads synced' }] : []),
    { label: 'Flags', value: flagCount, hint: monthWide.size ? 'excluding month-wide notes' : 'across these clients', warn: flagCount > 0 },
  ];
  const amLabel = amFilter === NO_AM ? 'No AM listed' : amFilter;

  return (
    <div className="px-8 py-8 max-w-[1200px] mx-auto w-full">
      {/* Header: title and the month's date range only */}
      <header className="mb-6">
        <h1 className="text-[36px] leading-[44px] font-semibold tracking-[-0.02em] text-[var(--foreground)]">Monthly ROI Report</h1>
        <p className="mt-1 text-[16px] leading-[24px] text-[var(--muted)]">{periodRange(periodId, periodLabel)}</p>
      </header>

      {/* Stat band */}
      <div
        className="grid bg-[var(--surface)] rounded-[12px] border border-[var(--border)] shadow-[var(--shadow-xs)] mb-12 overflow-hidden"
        style={{ gridTemplateColumns: `repeat(${stats.length}, minmax(0, 1fr))` }}
      >
        {stats.map(({ label, value, hint, warn }, i) => (
          <div key={label} className={`px-5 py-4 ${i > 0 ? 'border-l border-[var(--border)]' : ''}`}>
            <p className="flex items-center gap-1.5 text-[13px] leading-[18px] font-medium text-[var(--muted)]">
              {warn && <span className="w-2 h-2 rounded-full bg-[var(--warn-dot)]" />}
              {label}
            </p>
            <p className="text-[24px] leading-[32px] font-semibold tracking-[-0.02em] text-[var(--foreground)] july-tabular">{value}</p>
            <p className="text-[12px] leading-[16px] text-[var(--muted-soft)]">{hint}</p>
          </div>
        ))}
      </div>

      {/* Section 01: client data status */}
      <section>
        <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
          <div>
            <span className="block july-tabular text-[12px] leading-[18px] font-medium uppercase tracking-[0.14em] text-[var(--brand-text)] mb-1.5">
              01 · Clients
            </span>
            <h2 className="text-[30px] leading-[38px] font-semibold tracking-[-0.02em] text-[var(--foreground)]">Client data status</h2>
            <p className="mt-1.5 text-[14px] leading-[20px] text-[var(--muted)] max-w-[80ch]">
              What synced for each client this month. Click a row to open the client. Columns with no data for any client
              this month are left out.
            </p>
          </div>
          {amFilter && (
            <Badge variant="default">
              Showing {shown.length} of {rows.length} · {amLabel}
            </Badge>
          )}
        </div>

        {monthNotes.map((note) => (
          <div
            key={note}
            className="mb-4 flex items-start gap-2.5 rounded-[12px] border border-[var(--border)] bg-[var(--panel-2)] px-4 py-3 text-[14px] leading-[20px] text-[var(--text-2)]"
          >
            <Info className="w-4 h-4 mt-0.5 flex-none text-[var(--muted)]" />
            {note}
          </div>
        ))}

        <div className="bg-[var(--surface)] rounded-[12px] border border-[var(--border)] shadow-[var(--shadow-xs)] overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full text-[14px] leading-[20px]">
              <thead>
                <tr className="bg-[var(--panel-2)] border-b border-[var(--border)] text-[12px] leading-[18px] font-medium text-[var(--muted)]">
                  <th className="pl-5 pr-3 py-2.5 text-left font-medium">Client</th>
                  {showProvider && <th className="px-3 py-2.5 text-left font-medium">PMS</th>}
                  <th className="px-3 py-2.5 text-left font-medium">Promo codes</th>
                  <th className="px-3 py-2.5 text-left font-medium">Facebook</th>
                  <th className="px-3 py-2.5 text-left font-medium">PMS data</th>
                  {showGhl && <th className="px-3 py-2.5 text-left font-medium">GHL</th>}
                  <th className="px-3 py-2.5 text-left font-medium">Flags</th>
                  <th className="pr-5 py-2.5" aria-hidden="true" />
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--divider)]">
                {shown.map(({ name, client, mc, fb, pms, ghl, am }) => {
                  const flags = flagsByClient[name] ?? [];
                  const all = client?.pmsAnalysis?.promoCode.codes ?? [];
                  const used = all.filter((c) => c.uses > 0);
                  return (
                    <tr
                      key={name}
                      onClick={() => client && onSelectClient(name)}
                      className={`group transition-colors duration-100 ${client ? 'cursor-pointer hover:bg-[var(--panel-2)]' : 'opacity-50'}`}
                    >
                      <td className="pl-5 pr-3 py-3 align-top">
                        <span className="block font-semibold text-[var(--foreground)]">{name}</span>
                        <span className="block text-[12px] leading-[18px] text-[var(--muted-soft)]">{am ?? 'No AM listed'}</span>
                      </td>
                      {showProvider && (
                        <td className="px-3 py-3 align-top text-[13px] text-[var(--muted)] capitalize whitespace-nowrap">
                          {mc?.pmsProvider || <span className="text-[var(--muted-soft)]">—</span>}
                        </td>
                      )}
                      <td className="px-3 py-3 align-top text-[13px] text-[var(--muted)]">
                        {used.length > 0 ? (
                          <span title={used.map((c) => `${c.code} ×${c.uses}`).join(', ')}>
                            {used.slice(0, 3).map((c) => `${c.code} ×${c.uses}`).join(', ')}
                            {used.length > 3 && <span className="text-[var(--muted-soft)]"> +{used.length - 3}</span>}
                          </span>
                        ) : all.length > 0 ? (
                          // No uses this month: still show the registry codes so it's clear what exists
                          <span className="text-[var(--muted-soft)]" title={all.map((c) => c.code).join(', ') + ', no uses this month'}>
                            {all.slice(0, 3).map((c) => c.code).join(', ')}
                            {all.length > 3 && ` +${all.length - 3}`}
                            {' · no uses'}
                          </span>
                        ) : (
                          <span className="text-[var(--muted-soft)]">—</span>
                        )}
                      </td>
                      <td className="px-3 py-3 align-top"><StatusCell status={fb} /></td>
                      <td className="px-3 py-3 align-top"><StatusCell status={pms} /></td>
                      {showGhl && <td className="px-3 py-3 align-top"><StatusCell status={ghl} /></td>}
                      <td className="px-3 py-3 align-top">
                        {flags.length > 0 ? (
                          <span title={flags.map(flagText).join('\n')}>
                            <Badge variant="warning" noDot>
                              <AlertTriangle className="w-3 h-3 -ml-0.5" />
                              {flags.length}
                            </Badge>
                          </span>
                        ) : (
                          <span className="text-[var(--muted-soft)]">—</span>
                        )}
                      </td>
                      <td className="pr-5 py-3 align-top text-right">
                        {client && (
                          <ChevronRight className="inline w-4 h-4 text-[var(--muted-soft)] group-hover:text-[var(--brand)] transition-colors duration-100" />
                        )}
                      </td>
                    </tr>
                  );
                })}
                {shown.length === 0 && (
                  <tr>
                    <td colSpan={8} className="px-5 py-6 text-[14px] text-[var(--muted-soft)]">
                      No clients for this account manager this month.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  );
}
