'use client';

import { Flag, FlagType } from '@/types';
import { AlertTriangle, XCircle, Info } from 'lucide-react';

interface DataStatusPanelProps {
  hasPMS: boolean;
  hasGHL: boolean;
  flags: Flag[];
}

const CRITICAL_TYPES: FlagType[] = ['no-pms-data', 'missing-ghl'];

const MESSAGES: Partial<Record<FlagType, (f: Flag) => string>> = {
  'no-pms-data': (f) => f.details ? `PMS: ${f.details}` : 'PMS data could not be parsed',
  'missing-ghl': () => 'No GHL file — Instagram & Facebook lead analysis unavailable',
  'net-income-warning': () => 'Revenue shown as NET INCOME — verify totals with client',
  'missing-from-promo-sheet': () => 'Client not found in promo codes sheet — add them to enable promo attribution',
};

export default function DataStatusPanel({ hasPMS, hasGHL, flags }: DataStatusPanelProps) {
  const issues: { type: 'error' | 'warning' | 'info'; message: string }[] = [];

  if (!hasPMS) {
    issues.push({ type: 'error', message: 'No PMS data synced — run Google Drive sync or check the sheet tab name matches the client name' });
  }
  if (!hasGHL) {
    issues.push({ type: 'warning', message: 'No GHL data synced — Instagram & Facebook lead analysis unavailable' });
  }

  for (const flag of flags) {
    if (flag.type in MESSAGES) {
      const msg = MESSAGES[flag.type as FlagType]?.(flag);
      if (msg) {
        const type = CRITICAL_TYPES.includes(flag.type as FlagType) ? 'error' : 'warning';
        if (!issues.find(i => i.message === msg)) {
          issues.push({ type, message: msg });
        }
      }
    }
  }

  if (issues.length === 0) return null;

  return (
    <div className="space-y-2">
      {issues.map((issue, i) => (
        <div
          key={i}
          className={`flex items-start gap-2.5 rounded-[10px] px-4 py-3 text-[13px] border ${
            issue.type === 'error'
              ? 'bg-[rgba(220,38,38,.06)] border-[rgba(220,38,38,.18)] text-[var(--danger)]'
              : issue.type === 'warning'
              ? 'bg-[rgba(255,159,10,.1)] border-[rgba(255,159,10,.25)] text-[var(--warning-ink)]'
              : 'bg-[var(--fill-blue)] border-[var(--border)] text-[var(--brand)]'
          }`}
        >
          {issue.type === 'error' ? (
            <XCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
          ) : issue.type === 'warning' ? (
            <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5" />
          ) : (
            <Info className="w-4 h-4 flex-shrink-0 mt-0.5" />
          )}
          <span>{issue.message}</span>
        </div>
      ))}
    </div>
  );
}
