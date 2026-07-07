'use client';

import { useRef, useState, DragEvent, ChangeEvent, useCallback } from 'react';
import { Upload, FileText, X, ChevronDown, ChevronUp } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from './ui/Button';
import { detectFileType, detectClientNameFromFilename } from '@/lib/analysis/processor';

export interface StagedFiles {
  metaAds: File | null;
  promoCodes: File | null;
  pmsFiles: Record<string, File>;
  ghlFiles: Record<string, File>;
}

interface UploadZoneProps {
  onProcess: (files: StagedFiles) => void;
  isProcessing: boolean;
}

interface FileEntry {
  file: File;
  type: ReturnType<typeof detectFileType>;
  clientName?: string;
}

export default function UploadZone({ onProcess, isProcessing }: UploadZoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [entries, setEntries] = useState<FileEntry[]>([]);
  const [showDetails, setShowDetails] = useState(false);

  const addFiles = useCallback((files: FileList | File[]) => {
    const arr = Array.from(files);
    setEntries((prev) => {
      const existing = new Set(prev.map((e) => e.file.name));
      const newEntries: FileEntry[] = [];
      for (const file of arr) {
        if (existing.has(file.name)) continue;
        const type = detectFileType(file.name);
        const clientName = (type === 'pms' || type === 'ghl')
          ? detectClientNameFromFilename(file.name)
          : undefined;
        newEntries.push({ file, type, clientName });
      }
      return [...prev, ...newEntries];
    });
  }, []);

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setDragging(false);
    if (e.dataTransfer.files) addFiles(e.dataTransfer.files);
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) addFiles(e.target.files);
    e.target.value = '';
  };

  const removeEntry = (name: string) => {
    setEntries((prev) => prev.filter((e) => e.file.name !== name));
  };

  const updateClientName = (filename: string, newName: string) => {
    setEntries((prev) =>
      prev.map((e) => (e.file.name === filename ? { ...e, clientName: newName } : e)),
    );
  };

  const handleProcess = () => {
    const staged: StagedFiles = { metaAds: null, promoCodes: null, pmsFiles: {}, ghlFiles: {} };
    for (const entry of entries) {
      if (entry.type === 'meta-ads') staged.metaAds = entry.file;
      else if (entry.type === 'promo-codes') staged.promoCodes = entry.file;
      else if (entry.type === 'pms' && entry.clientName) staged.pmsFiles[entry.clientName] = entry.file;
      else if (entry.type === 'ghl' && entry.clientName) staged.ghlFiles[entry.clientName] = entry.file;
    }
    onProcess(staged);
  };

  const typeLabel = (type: FileEntry['type'], client?: string): string => {
    if (type === 'meta-ads') return 'Meta Ads Report';
    if (type === 'promo-codes') return 'Promo Codes';
    if (type === 'pms') return `PMS — ${client ?? '?'}`;
    if (type === 'ghl') return `GHL — ${client ?? '?'}`;
    return 'Unknown (will be skipped)';
  };

  const typeColor = (type: FileEntry['type']): string => {
    if (type === 'meta-ads') return 'text-blue-600 bg-blue-50';
    if (type === 'promo-codes') return 'text-purple-600 bg-purple-50';
    if (type === 'pms') return 'text-green-700 bg-green-50';
    if (type === 'ghl') return 'text-amber-700 bg-amber-50';
    return 'text-gray-500 bg-gray-100';
  };

  const canProcess = entries.length > 0 && entries.some((e) => e.type !== 'unknown');

  return (
    <div className="space-y-4">
      {/* Drop zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={cn(
          'border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors',
          dragging ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-400 hover:bg-gray-50',
        )}
      >
        <input ref={inputRef} type="file" multiple accept=".csv" className="hidden" onChange={handleChange} />
        <Upload className="mx-auto mb-3 w-8 h-8 text-gray-400" />
        <p className="font-medium text-gray-700">Drop CSV files here or click to browse</p>
        <p className="mt-1 text-sm text-gray-400">
          Meta Ads, Promo Codes, PMS data, GHL leads — all at once
        </p>
        <p className="mt-2 text-xs text-gray-400">
          Files are named automatically: <em>Flohom PMS data.csv</em>, <em>Flohom GHL data.csv</em>, etc.
        </p>
      </div>

      {/* Staged files */}
      {entries.length > 0 && (
        <div className="border border-gray-200 rounded-xl overflow-hidden">
          <button
            className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 text-sm font-medium text-gray-700 hover:bg-gray-100"
            onClick={() => setShowDetails((v) => !v)}
          >
            <span>{entries.length} file{entries.length !== 1 ? 's' : ''} staged</span>
            {showDetails ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {showDetails && (
            <ul className="divide-y divide-gray-100">
              {entries.map((e) => (
                <li key={e.file.name} className="flex items-center gap-3 px-4 py-2.5">
                  <FileText className="w-4 h-4 text-gray-400 flex-shrink-0" />
                  <span className="flex-1 text-sm text-gray-800 truncate">{e.file.name}</span>
                  <span className={cn('text-xs px-2 py-0.5 rounded font-medium flex-shrink-0', typeColor(e.type))}>
                    {typeLabel(e.type, e.clientName)}
                  </span>
                  {(e.type === 'pms' || e.type === 'ghl') && (
                    <input
                      className="text-xs border border-gray-200 rounded px-2 py-1 w-36 flex-shrink-0"
                      value={e.clientName ?? ''}
                      onChange={(ev) => updateClientName(e.file.name, ev.target.value)}
                      placeholder="Client name"
                    />
                  )}
                  <button onClick={() => removeEntry(e.file.name)} className="ml-1 text-gray-400 hover:text-red-500">
                    <X className="w-4 h-4" />
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      <Button onClick={handleProcess} disabled={!canProcess || isProcessing} className="w-full justify-center py-3">
        {isProcessing ? 'Processing...' : 'Run Analysis'}
      </Button>
    </div>
  );
}
