'use client';

import { Flag, FlagType } from '@/types';
import { AlertTriangle, Info, AlertCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';
import { cn } from '@/lib/utils';

const FLAG_CONFIG: Record<FlagType, { label: string; className: string; icon: React.ElementType }> = {
  'unrecognized-code': {
    label: 'Unrecognized Code',
    className: 'text-[var(--danger)] bg-[rgba(220,38,38,.06)] border-[rgba(220,38,38,.18)]',
    icon: AlertCircle,
  },
  'missing-from-promo-sheet': {
    label: 'Missing from Promo Sheet',
    className: 'text-[var(--warning-ink)] bg-[rgba(255,159,10,.1)] border-[rgba(255,159,10,.25)]',
    icon: AlertTriangle,
  },
  'net-income-warning': {
    label: 'NET INCOME Revenue',
    className: 'text-[var(--warning-ink)] bg-[rgba(255,159,10,.1)] border-[rgba(255,159,10,.25)]',
    icon: AlertTriangle,
  },
  'name-only-match': {
    label: 'Name-Only Match',
    className: 'text-[var(--brand)] bg-[var(--fill-blue)] border-[var(--border)]',
    icon: Info,
  },
  'platform-email': {
    label: 'Platform Email Excluded',
    className: 'text-[var(--muted)] bg-[var(--fill-gray)] border-[var(--border)]',
    icon: Info,
  },
  'no-pms-data': {
    label: 'Parse Error',
    className: 'text-[var(--danger)] bg-[rgba(220,38,38,.06)] border-[rgba(220,38,38,.18)]',
    icon: AlertCircle,
  },
  'missing-ghl': {
    label: 'Missing GHL Data',
    className: 'text-[var(--warning-ink)] bg-[rgba(255,159,10,.1)] border-[rgba(255,159,10,.25)]',
    icon: AlertTriangle,
  },
};

export default function FlagPanel({ flags }: { flags: Flag[] }) {
  const [expanded, setExpanded] = useState(false);
  if (flags.length === 0) return null;

  const byType: Record<string, Flag[]> = {};
  for (const f of flags) {
    if (!byType[f.type]) byType[f.type] = [];
    byType[f.type].push(f);
  }

  return (
    <div className="rounded-[16px] border border-[rgba(255,159,10,.25)] overflow-hidden shadow-[0_2px_12px_rgba(15,23,42,.04)]">
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full flex items-center justify-between px-6 py-4 bg-[rgba(255,159,10,.1)] text-[13px] font-semibold text-[var(--warning-ink)] hover:bg-[rgba(255,159,10,.16)] transition-colors duration-150"
      >
        <span className="flex items-center gap-2">
          <AlertTriangle className="w-4 h-4" />
          {flags.length} Flag{flags.length !== 1 ? 's' : ''} Requiring Attention
        </span>
        {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
      </button>

      {expanded && (
        <div className="bg-[var(--surface-strong)] divide-y divide-[var(--divider)]">
          {Object.entries(byType).map(([type, typeFlags]) => {
            const config = FLAG_CONFIG[type as FlagType];
            const Icon = config.icon;
            return (
              <div key={type} className="px-6 py-4">
                <p className="text-[11px] font-semibold text-[var(--muted-soft)] uppercase tracking-[0.04em] mb-2">
                  {config.label}
                </p>
                <ul className="space-y-2">
                  {typeFlags.map((f) => (
                    <li
                      key={f.id}
                      className={cn(
                        'flex items-start gap-2 text-[13px] rounded-[10px] px-4 py-3 border',
                        config.className,
                      )}
                    >
                      <Icon className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      <div>
                        <span className="font-semibold">[{f.clientName}]</span> {f.message}
                        {f.details && (
                          <p className="text-[12px] opacity-70 mt-0.5">{f.details}</p>
                        )}
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
