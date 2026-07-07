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
          className={`flex items-start gap-2.5 rounded-xl px-4 py-3 text-sm border ${
            issue.type === 'error'
              ? 'bg-red-50 border-red-100 text-red-700'
              : issue.type === 'warning'
              ? 'bg-amber-50 border-amber-100 text-amber-700'
              : 'bg-blue-50 border-blue-100 text-blue-700'
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
