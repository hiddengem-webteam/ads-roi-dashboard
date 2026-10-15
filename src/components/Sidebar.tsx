'use client';

import { cn } from '@/lib/utils';
import { ClientData } from '@/types';
import Wordmark from './Wordmark';

interface SidebarProps {
  clients: ClientData[];
  selectedClient: string;
  onSelectClient: (name: string) => void;
  periodLabel?: string;
}


// Account manager per client, derived from whose July 2026 direct-booking
// spreadsheet each client's data came from (every client appears in exactly
// one AM's file). Clients absent from all AM files came via the platform
// sync only and have no AM attribution here.
const ACCOUNT_MANAGERS: Record<string, string> = {
  'Three Suns Cabins': 'Anna',
  'Stay Different': 'Anna',
  'The Outpost': 'Anna',
  'Ponderosa Pines Resort': 'Anna',
  'Bison Ridge Retreat': 'Chiara',
  'Stay Southen Illinois': 'Chiara',
  'Hillside Amble': 'Chiara',
  'Paradise Pointe': 'Makenna',
  'Treetop Escapes': 'Makenna',
  'Stay Saluda': 'Makenna',
  'Inspired Retreats': 'Makenna',
  'Flohom': 'Makenna',
  'The Cohost Company': 'Makenna',
  'Stay with Branch': 'Charlotte',
  'Asheville River Cabins': 'Charlotte',
  'Myrinn': 'Charlotte',
  'Home Base': 'Charlotte',
  'Stay on 30a': 'Charlotte',
  'Big Moon Ranch': 'Charlotte',
  'Sunapee Stays': 'Charlotte',
  'Dwell': 'Charlotte',
  'Starlight Haven Hot Springs': 'Charlotte',
  'Starlight Haven Weiss Lake': 'Charlotte',
  'Nature Nooks': 'Alicia',
  'Wanderin Star Farms': 'Alicia',
  'Hiawassee Glamping': 'Alicia',
  'Awayframes': 'Alicia',
  'Tàberg Falls': 'Alicia',
  'Reflections Resorts': 'Alicia',
  'Selah Place': 'Alicia',
  'Green Springs Inn': 'Alicia',
  'Away2PA': 'Alicia',
  'American River Resort': 'Nicole',
  'Evergreen Cabins': 'Nicole',
  'Parker Reserve': 'Nicole',
  'StayLuxe': 'Nicole',
  'Endless Stays': 'Nicole',
  'Red White & Blue Views': 'Nicole',
  'Best Texas Travel': 'Nicole',
};

export default function Sidebar({ clients, selectedClient, onSelectClient, periodLabel }: SidebarProps) {
  return (
    <aside className="w-[220px] flex-shrink-0 flex flex-col h-full">
      {/* Masthead, as on the weekly pages: wordmark + mono eyebrow */}
      <div className="px-5 pt-6 pb-5 border-b border-[var(--border)]">
        <Wordmark className="mb-2.5 w-full max-w-[170px]" />
        <p className="july-tabular text-[11px] leading-[18px] font-medium uppercase tracking-[0.04em] text-[var(--muted-soft)]">
          Monthly ROI{periodLabel ? ` · ${periodLabel}` : ''}
        </p>
      </div>

      {/* Clients */}
      <div className="px-3 pt-4 pb-3 flex-1 overflow-y-auto july-scrollbar">
        <p className="text-[12px] leading-[18px] font-medium text-[var(--muted-soft)] px-3 mb-1.5">
          Clients
        </p>
        <nav className="space-y-0.5">
          {clients.map((client) => {
            const isActive = client.name === selectedClient;
            const am = ACCOUNT_MANAGERS[client.name];
            return (
              <button
                key={client.name}
                onClick={() => onSelectClient(client.name)}
                className={cn(
                  'w-full flex items-center gap-2.5 px-3 py-2 rounded-[8px] text-[13px] leading-[20px] font-medium text-left transition-colors duration-150',
                  isActive
                    ? 'bg-[var(--brand-bg)] text-[var(--brand-text)]'
                    : 'text-[var(--text-2)] hover:text-[var(--foreground)] hover:bg-[var(--panel-3)]',
                )}
              >
                <span className="min-w-0">
                  <span className="block truncate">{client.name}</span>
                  {am && (
                    <span className="block truncate text-[11px] font-normal text-[var(--muted-soft)]">
                      {am}
                    </span>
                  )}
                </span>
              </button>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}
