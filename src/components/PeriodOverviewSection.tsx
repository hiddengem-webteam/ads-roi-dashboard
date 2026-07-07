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
  if (status === 'ok') return <CheckCircle2 className="w-4 h-4 text-emerald-500" />;
  if (status === 'missing') return <XCircle className="w-4 h-4 text-red-400" />;
  return <Minus className="w-4 h-4 text-gray-300" />;
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
      <div className="grid grid-cols-4 gap-3">
        {[
          { label: 'Total Clients', value: withFB },
          { label: 'With Facebook', value: withFB },
          { label: 'With PMS', value: withPMS },
          { label: 'With GHL', value: withGHL },
        ].map(({ label, value }) => (
          <div key={label} className="bg-white rounded-2xl border border-gray-100 shadow-[0_1px_4px_rgba(0,0,0,0.06)] px-5 py-4">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-1">{label}</p>
            <p className="text-2xl font-bold text-gray-900">{value}</p>
          </div>
        ))}
      </div>

      {/* Client table */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-[0_1px_4px_rgba(0,0,0,0.06)] overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <p className="text-sm font-semibold text-gray-700">Client Data Status</p>
          {totalFlags > 0 && (
            <span className="flex items-center gap-1.5 text-xs font-medium text-amber-600 bg-amber-50 border border-amber-100 px-2.5 py-1 rounded-lg">
              <AlertTriangle className="w-3.5 h-3.5" />
              {totalFlags} flag{totalFlags !== 1 ? 's' : ''} across all clients
            </span>
          )}
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="px-6 py-3 text-left text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Client</th>
                <th className="px-4 py-3 text-center text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Facebook</th>
                <th className="px-4 py-3 text-center text-[11px] font-semibold text-gray-400 uppercase tracking-wider">PMS</th>
                <th className="px-4 py-3 text-center text-[11px] font-semibold text-gray-400 uppercase tracking-wider">GHL</th>
                <th className="px-4 py-3 text-center text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Flags</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
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
                    className={`transition-colors ${client ? 'cursor-pointer hover:bg-gray-50/60' : 'opacity-50'} ${hasMissing ? 'bg-red-50/30' : ''}`}
                  >
                    <td className="px-6 py-3 font-medium text-gray-800">{name}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-center gap-1.5">
                        <StatusIcon status={fbStatus} />
                        <span className={`text-xs ${fbStatus === 'ok' ? 'text-emerald-600' : 'text-gray-300'}`}>
                          {statusLabel(fbStatus)}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-center gap-1.5">
                        <StatusIcon status={pmsStatus} />
                        <span className={`text-xs ${pmsStatus === 'ok' ? 'text-emerald-600' : pmsStatus === 'missing' ? 'text-red-500 font-medium' : 'text-gray-300'}`}>
                          {statusLabel(pmsStatus)}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center justify-center gap-1.5">
                        <StatusIcon status={ghlStatus} />
                        <span className={`text-xs ${ghlStatus === 'ok' ? 'text-emerald-600' : ghlStatus === 'missing' ? 'text-red-500 font-medium' : 'text-gray-300'}`}>
                          {statusLabel(ghlStatus)}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-center">
                      {flags.length > 0 ? (
                        <span className="inline-flex items-center gap-1 text-xs font-medium text-amber-600 bg-amber-50 px-2 py-0.5 rounded-md">
                          <AlertTriangle className="w-3 h-3" />
                          {flags.length}
                        </span>
                      ) : (
                        <span className="text-gray-300 text-xs">—</span>
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
