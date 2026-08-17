'use client';

import { ProcessedData, Flag } from '@/types';
import { CheckCircle2, XCircle, Minus, AlertTriangle } from 'lucide-react';

interface ManifestClient {
  name: string;
  pms?: string;
  ghl?: string;
}

interface PeriodOverviewSectionProps {
  manifestClients: ManifestClient[];
  data: ProcessedData;
  onSelectClient: (name: string) => void;
}

function StatusIcon({ status }: { status: 'ok' | 'missing' | 'none' }) {
  if (status === 'ok') return <CheckCircle2 className="w-4 h-4 text-[var(--success-ink)]" />;
  if (status === 'missing') return <XCircle className="w-4 h-4 text-[var(--danger)]" />;
  return <Minus className="w-4 h-4 text-[var(--muted-soft)]" />;
}

function statusLabel(status: 'ok' | 'missing' | 'none') {
  if (status === 'ok') return 'Synced';
  if (status === 'missing') return 'Missing';
  return '—';
}

export default function PeriodOverviewSection({
  manifestClients,
  data,
  onSelectClient,
}: PeriodOverviewSectionProps) {
  // Build a unified client list: manifest clients + any FB-only clients not in manifest
  const manifestNames = new Set(manifestClients.map((c) => c.name));
  const allNames = new Set([
    ...manifestClients.map((c) => c.name),
    ...Object.keys(data.clients),
  ]);

  // Sort: manifest order first (spend-sorted already), then FB-only extras alphabetically
  const fbOnlyExtras = Object.keys(data.clients)
    .filter((n) => !manifestNames.has(n))
    .sort();

  const orderedNames = [
    ...manifestClients.map((c) => c.name).filter((n) => data.clients[n] || manifestClients.find(mc => mc.name === n)),
    ...fbOnlyExtras,
  ];

  const flagsByClient: Record<string, Flag[]> = {};
  for (const flag of data.flags) {
    if (!flagsByClient[flag.clientName]) flagsByClient[flag.clientName] = [];
    flagsByClient[flag.clientName].push(flag);
  }

  // Totals
  const withPMS = orderedNames.filter((n) => data.clients[n]?.pmsAnalysis).length;
  const withGHL = orderedNames.filter((n) => data.clients[n]?.hasGHL).length;
  const withFB = orderedNames.filter((n) => data.clients[n]?.facebookStats).length;
  const totalFlags = data.flags.length;

  return (
    <div className="px-8 py-8 max-w-5xl space-y-6">
      {/* Top stats */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Total Clients', value: allNames.size },
          { label: 'With Facebook', value: withFB },
          { label: 'With PMS', value: withPMS },
          { label: 'With GHL', value: withGHL },
        ].map(({ label, value }) => (
          <div key={label} className="bg-[var(--surface)] rounded-[16px] border border-[var(--border)] shadow-[0_8px_22px_rgba(15,23,42,.04)] px-5 py-4">
            <p className="text-[12px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em] mb-1">{label}</p>
            <p className="text-[24px] font-extrabold text-[var(--foreground)] tracking-[-0.01em] july-tabular">{value}</p>
          </div>
        ))}
      </div>

      {/* Client table */}
      <div className="bg-[var(--surface)] rounded-[16px] border border-[var(--border)] shadow-[0_8px_22px_rgba(15,23,42,.04)] overflow-hidden">
        <div className="px-6 py-4 border-b border-[var(--border)] flex items-center justify-between">
          <p className="text-[14px] font-bold text-[var(--foreground)]">Client Data Status</p>
          {totalFlags > 0 && (
            <span className="flex items-center gap-1.5 text-[11px] font-semibold text-[var(--warning-ink)] bg-[rgba(255,159,10,.1)] border border-[rgba(255,159,10,.25)] px-2.5 py-1 rounded-full">
              <AlertTriangle className="w-3.5 h-3.5" />
              {totalFlags} flag{totalFlags !== 1 ? 's' : ''} across all clients
            </span>
          )}
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full text-[13px]">
            <thead>
              <tr className="bg-[var(--fill-gray)] border-b border-[var(--border)]">
                <th className="px-6 py-3 text-left text-[11px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em]">Client</th>
                <th className="px-4 py-3 text-center text-[11px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em]">Facebook</th>
                <th className="px-4 py-3 text-center text-[11px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em]">PMS</th>
                <th className="px-4 py-3 text-center text-[11px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em]">GHL</th>
                <th className="px-4 py-3 text-center text-[11px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em]">Flags</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--divider)]">
              {orderedNames.map((name) => {
                const client = data.clients[name];
                const mc = manifestClients.find((c) => c.name === name);
                const flags = flagsByClient[name] ?? [];

                const fbStatus: 'ok' | 'missing' | 'none' = client?.facebookStats ? 'ok' : 'none';
                const pmsStatus: 'ok' | 'missing' | 'none' = client?.pmsAnalysis
                  ? 'ok'
                  : mc?.pms
                  ? 'missing'
                  : 'none';
                // GHL missing only if manifest explicitly has a ghl path that didn't load
                const ghlStatus: 'ok' | 'missing' | 'none' = client?.hasGHL
                  ? 'ok'
                  : mc?.ghl
                  ? 'missing'
                  : 'none';

                const hasMissing = pmsStatus === 'missing' || ghlStatus === 'missing';

                return (
                  <tr
                    key={name}
                    onClick={() => client && onSelectClient(name)}
                    className={`bg-white transition-colors duration-150 ${client ? 'cursor-pointer hover:bg-[var(--fill-cool)]' : 'opacity-50'} ${hasMissing ? 'bg-[rgba(220,38,38,.03)]' : ''}`}
                  >
                    <td className="px-6 py-3 font-semibold text-[var(--foreground)]">{name}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-center gap-1.5">
                        <StatusIcon status={fbStatus} />
                        <span className={`text-[12px] ${fbStatus === 'ok' ? 'text-[var(--success-ink)]' : 'text-[var(--muted-soft)]'}`}>
                          {statusLabel(fbStatus)}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-center gap-1.5">
                        <StatusIcon status={pmsStatus} />
                        <span className={`text-[12px] ${pmsStatus === 'ok' ? 'text-[var(--success-ink)]' : pmsStatus === 'missing' ? 'text-[var(--danger)] font-semibold' : 'text-[var(--muted-soft)]'}`}>
                          {statusLabel(pmsStatus)}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-center gap-1.5">
                        <StatusIcon status={ghlStatus} />
                        <span className={`text-[12px] ${ghlStatus === 'ok' ? 'text-[var(--success-ink)]' : ghlStatus === 'missing' ? 'text-[var(--danger)] font-semibold' : 'text-[var(--muted-soft)]'}`}>
                          {statusLabel(ghlStatus)}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-center">
                      {flags.length > 0 ? (
                        <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-[var(--warning-ink)] bg-[rgba(255,159,10,.1)] px-2 py-0.5 rounded-[6px]">
                          <AlertTriangle className="w-3 h-3" />
                          {flags.length}
                        </span>
                      ) : (
                        <span className="text-[var(--muted-soft)] text-[12px]">—</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
