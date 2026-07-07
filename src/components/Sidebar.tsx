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
      <div className="px-5 pt-6 pb-5 border-b border-gray-100">
        <div className="flex items-center gap-2.5 mb-1">
          <div className="w-7 h-7 bg-gray-900 rounded-lg flex items-center justify-center flex-shrink-0">
            <BarChart3 className="w-3.5 h-3.5 text-white" />
          </div>
          <span className="font-semibold text-gray-900 text-sm">ROI Dashboard</span>
        </div>
        <p className="text-xs text-gray-400 pl-9">HiddenGem Media</p>
        {periodLabel && (
          <p className="mt-3 text-xs font-medium text-gray-500 bg-gray-100 rounded-lg px-3 py-1.5 text-center">
            {periodLabel}
          </p>
        )}
      </div>

      {/* Clients */}
      <div className="px-3 pt-4 pb-3 flex-1 overflow-y-auto">
        <p className="text-[11px] font-semibold text-gray-400 uppercase tracking-widest px-2 mb-2">
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
                  'w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-sm font-medium text-left transition-all',
                  isActive
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900',
                )}
              >
                <Users className={cn('w-3.5 h-3.5 flex-shrink-0', isActive ? 'text-gray-400' : 'text-gray-400')} />
                <span className="truncate">{client.name}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}
