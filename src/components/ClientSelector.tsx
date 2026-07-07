'use client';
import { ChevronDown } from 'lucide-react';

interface ClientSelectorProps {
  clients: string[];
  selected: string | 'all';
  onChange: (value: string | 'all') => void;
}

export default function ClientSelector({ clients, selected, onChange }: ClientSelectorProps) {
  return (
    <div className="relative inline-block">
      <select
        value={selected}
        onChange={(e) => onChange(e.target.value as string | 'all')}
        className="appearance-none bg-white border border-gray-200 rounded-lg pl-4 pr-10 py-2 text-sm font-medium text-gray-800 shadow-sm cursor-pointer hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-1 min-w-48"
      >
        <option value="all">All Clients</option>
        {clients.map((c) => (
          <option key={c} value={c}>
            {c}
          </option>
        ))}
      </select>
      <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
    </div>
  );
}
