'use client';

import { cn } from '@/lib/utils';
import { ClientData } from '@/types';
import { BarChart3, Users } from 'lucide-react';

interface SidebarProps {
  clients: ClientData[];
  selectedClient: string;
  onSelectClient: (name: string) => void;
  periodLabel?: string;
}

export default function Sidebar({ clients, selectedClient, onSelectClient, periodLabel }: SidebarProps) {
  return (
    <aside className="w-[220px] flex-shrink-0 flex flex-col h-full">
      {/* Brand */}
      <div className="px-5 pt-6 pb-5 border-b border-[var(--border)]">
        <div className="flex items-center gap-2.5 mb-1">
          <div className="w-7 h-7 bg-[var(--brand)] rounded-[10px] flex items-center justify-center flex-shrink-0">
            <BarChart3 className="w-3.5 h-3.5 text-white" />
          </div>
          <span className="font-bold text-[var(--foreground)] text-[14px] tracking-[-0.01em]">ROI Dashboard</span>
        </div>
        <p className="text-[12px] text-[var(--muted-soft)] pl-9">HiddenGem Media</p>
        {periodLabel && (
          <p className="mt-3 text-[12px] font-semibold text-[var(--brand)] bg-[var(--fill-blue)] rounded-[8px] px-3 py-1.5 text-center">
            {periodLabel}
          </p>
        )}
      </div>

      {/* Clients */}
      <div className="px-3 pt-4 pb-3 flex-1 overflow-y-auto july-scrollbar">
        <p className="text-[11px] font-semibold text-[var(--muted-soft)] uppercase tracking-[0.04em] px-2 mb-2">
          Clients
        </p>
        <nav className="space-y-0.5">
          {clients.map((client) => {
            const isActive = client.name === selectedClient;
            return (
              <button
                key={client.name}
                onClick={() => onSelectClient(client.name)}
                className={cn(
                  'relative w-full flex items-center gap-2.5 px-3 py-2.5 rounded-[10px] text-[13px] font-semibold text-left transition-colors duration-150',
                  isActive
                    ? 'bg-[var(--fill-blue)] text-[var(--brand)]'
                    : 'text-[var(--muted)] hover:text-[var(--foreground)] hover:bg-[var(--fill-cool)]',
                )}
              >
                {isActive && (
                  <span className="absolute left-0 top-1.5 bottom-1.5 w-[3px] rounded-full bg-[var(--brand)]" />
                )}
                <Users className={cn('w-3.5 h-3.5 flex-shrink-0', isActive ? 'text-[var(--brand)]' : 'text-[var(--muted-soft)]')} />
                <span className="truncate">{client.name}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}
