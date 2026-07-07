'use client';

import { Flag, FlagType } from '@/types';
import { AlertTriangle, Info, AlertCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';
import { cn } from '@/lib/utils';

const FLAG_CONFIG: Record<FlagType, { label: string; className: string; icon: React.ElementType }> = {
  'unrecognized-code': {
    label: 'Unrecognized Code',
    className: 'text-red-700 bg-red-50 border-red-100',
    icon: AlertCircle,
  },
  'missing-from-promo-sheet': {
    label: 'Missing from Promo Sheet',
    className: 'text-amber-700 bg-amber-50 border-amber-100',
    icon: AlertTriangle,
  },
  'net-income-warning': {
    label: 'NET INCOME Revenue',
    className: 'text-amber-700 bg-amber-50 border-amber-100',
    icon: AlertTriangle,
  },
  'name-only-match': {
    label: 'Name-Only Match',
    className: 'text-blue-700 bg-blue-50 border-blue-100',
    icon: Info,
  },
  'platform-email': {
    label: 'Platform Email Excluded',
    className: 'text-gray-600 bg-gray-50 border-gray-200',
    icon: Info,
  },
  'no-pms-data': {
    label: 'Parse Error',
    className: 'text-red-700 bg-red-50 border-red-100',
    icon: AlertCircle,
  },
  'missing-ghl': {
    label: 'Missing GHL Data',
    className: 'text-amber-700 bg-amber-50 border-amber-100',
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
    <div className="rounded-2xl border border-amber-100 overflow-hidden shadow-[0_1px_4px_rgba(0,0,0,0.04)]">
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full flex items-center justify-between px-6 py-4 bg-amber-50 text-sm font-semibold text-amber-800 hover:bg-amber-100 transition-colors"
      >
        <span className="flex items-center gap-2">
          <AlertTriangle className="w-4 h-4" />
          {flags.length} Flag{flags.length !== 1 ? 's' : ''} Requiring Attention
        </span>
        {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
      </button>

      {expanded && (
        <div className="bg-white divide-y divide-gray-50">
          {Object.entries(byType).map(([type, typeFlags]) => {
            const config = FLAG_CONFIG[type as FlagType];
            const Icon = config.icon;
            return (
              <div key={type} className="px-6 py-4">
                <p className="text-[11px] font-semibold text-gray-400 uppercase tracking-widest mb-2">
                  {config.label}
                </p>
                <ul className="space-y-2">
                  {typeFlags.map((f) => (
                    <li
                      key={f.id}
                      className={cn(
                        'flex items-start gap-2 text-sm rounded-xl px-4 py-3 border',
                        config.className,
                      )}
                    >
                      <Icon className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      <div>
                        <span className="font-semibold">[{f.clientName}]</span> {f.message}
                        {f.details && (
                          <p className="text-xs opacity-70 mt-0.5">{f.details}</p>
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
