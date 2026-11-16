'use client';

import { ChevronDown } from 'lucide-react';
import { cn } from '@/lib/utils';
import { ClientData } from '@/types';
import { ACCOUNT_MANAGERS, NO_AM, matchesAm } from '@/lib/accountManagers';
import Wordmark from './Wordmark';

interface SidebarProps {
  clients: ClientData[];
  selectedClient: string;
  onSelectClient: (name: string) => void;
  /** Account manager filter ('' = everyone, NO_AM = clients with no AM listed). */
  amFilter: string;
  onAmFilter: (am: string) => void;
}

export default function Sidebar({ clients, selectedClient, onSelectClient, amFilter, onAmFilter }: SidebarProps) {
  const counts = new Map<string, number>();
  let unassigned = 0;
  for (const c of clients) {
    const am = ACCOUNT_MANAGERS[c.name];
    if (am) counts.set(am, (counts.get(am) ?? 0) + 1);
    else unassigned++;
  }
  const ams = [...counts.keys()].sort();
  const shown = clients.filter((c) => matchesAm(c.name, amFilter));

  return (
    <aside className="w-[240px] flex-shrink-0 flex flex-col h-full">
      {/* Masthead: wordmark only, as on the weekly pages */}
      <div className="px-5 pt-6 pb-5 border-b border-[var(--border)]">
        <Wordmark className="w-full max-w-[170px]" />
      </div>

      {/* Account manager filter: narrows this list and the Overview table */}
      <div className="px-4 pt-4">
        <label htmlFor="am-filter" className="block text-[13px] leading-[20px] font-medium text-[var(--text-2)] mb-1.5">
          Account manager
        </label>
        <div className="relative">
          <select
            id="am-filter"
            value={amFilter}
            onChange={(e) => onAmFilter(e.target.value)}
            className={cn(
              'appearance-none w-full h-9 pl-3 pr-8 text-[13px] font-medium rounded-[8px] border shadow-[var(--shadow-xs)] cursor-pointer transition-colors duration-100',
              amFilter
                ? 'border-[var(--brand)] !bg-[var(--brand-bg)] !text-[var(--brand-text)]'
                : 'border-[var(--border-strong)] hover:border-[var(--muted-soft)]',
            )}
          >
            <option value="">All account managers</option>
            {ams.map((am) => (
              <option key={am} value={am}>
                {am} ({counts.get(am)})
              </option>
            ))}
            {unassigned > 0 && <option value={NO_AM}>No AM listed ({unassigned})</option>}
          </select>
          <ChevronDown className="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--muted)]" />
        </div>
      </div>

      {/* Clients */}
      <div className="px-3 pt-4 pb-3 flex-1 overflow-y-auto july-scrollbar">
        <p className="text-[12px] leading-[18px] font-medium text-[var(--muted-soft)] px-3 mb-1.5">
          Clients · {shown.length}
          {amFilter ? ` of ${clients.length}` : ''}
        </p>
        <nav className="space-y-0.5">
          {shown.map((client) => {
            const isActive = client.name === selectedClient;
            const am = ACCOUNT_MANAGERS[client.name];
            return (
              <button
                key={client.name}
                onClick={() => onSelectClient(client.name)}
                className={cn(
                  'w-full flex items-center gap-2.5 px-3 py-2 rounded-[8px] text-[13px] leading-[20px] font-medium text-left transition-colors duration-100',
                  isActive
                    ? 'bg-[var(--brand-bg)] text-[var(--brand-text)]'
                    : 'text-[var(--text-2)] hover:text-[var(--foreground)] hover:bg-[var(--panel-3)]',
                )}
              >
                <span className="min-w-0">
                  <span className="block truncate">{client.name}</span>
                  {am && !amFilter && (
                    <span className="block truncate text-[11px] font-normal text-[var(--muted-soft)]">{am}</span>
                  )}
                </span>
              </button>
            );
          })}
          {shown.length === 0 && (
            <p className="px-3 py-2 text-[13px] text-[var(--muted-soft)]">No clients for this account manager this month.</p>
          )}
        </nav>
      </div>
    </aside>
  );
}
