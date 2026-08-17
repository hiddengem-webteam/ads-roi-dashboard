'use client';

import { useState, useEffect } from 'react';
import { Loader2, RefreshCw, X, CheckCircle, AlertCircle } from 'lucide-react';

interface MonthEntry {
  folderId: string;
  name: string;
  periodId: string;
  alreadySynced: boolean;
}

interface SyncResult {
  periodId: string;
  label: string;
  clientsSynced: string[];
  clientsMissingGHL: string[];
  log: string[];
  errors: string[];
}

export default function SyncPanel() {
  const [isLocalhost, setIsLocalhost] = useState(false);
  const [open, setOpen] = useState(false);
  const [months, setMonths] = useState<MonthEntry[]>([]);
  const [loadingMonths, setLoadingMonths] = useState(false);
  const [monthsError, setMonthsError] = useState<string | null>(null);
  const [syncingId, setSyncingId] = useState<string | null>(null);
  const [syncLog, setSyncLog] = useState<string[]>([]);
  const [syncResult, setSyncResult] = useState<SyncResult | null>(null);
  const [syncError, setSyncError] = useState<string | null>(null);

  // Only render on localhost
  useEffect(() => {
    setIsLocalhost(
      window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1',
    );
  }, []);

  // Fetch months when panel opens
  useEffect(() => {
    if (!open) return;
    setLoadingMonths(true);
    setMonthsError(null);
    setSyncResult(null);
    setSyncError(null);
    setSyncLog([]);

    fetch('/api/sync-months')
      .then((r) => r.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setMonths(data);
        } else {
          setMonthsError(data.error ?? 'Unknown error');
        }
      })
      .catch((err) => setMonthsError(String(err)))
      .finally(() => setLoadingMonths(false));
  }, [open]);

  async function handleSync(entry: MonthEntry) {
    setSyncingId(entry.periodId);
    setSyncLog([]);
    setSyncResult(null);
    setSyncError(null);

    try {
      const res = await fetch('/api/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folderId: entry.folderId, label: entry.name }),
      });
      const data = await res.json();
      if (!res.ok) {
        setSyncError(data.error ?? `HTTP ${res.status}`);
      } else {
        setSyncResult(data as SyncResult);
        setSyncLog(data.log ?? []);
        // Refresh months list so alreadySynced updates
        const refreshed = await fetch('/api/sync-months').then((r) => r.json());
        if (Array.isArray(refreshed)) setMonths(refreshed);
      }
    } catch (err) {
      setSyncError(String(err));
    } finally {
      setSyncingId(null);
    }
  }

  if (!isLocalhost) return null;

  return (
    <>
      {/* Floating button */}
      <button
        onClick={() => setOpen((v) => !v)}
        className="fixed bottom-6 right-6 z-50 flex items-center gap-2 bg-[var(--brand)] text-white text-[13px] font-semibold px-4 py-2.5 rounded-[14px] shadow-lg hover:bg-[var(--brand-deep)] transition-colors"
        aria-label="Sync Month"
      >
        <RefreshCw className="w-4 h-4" />
        Sync Month
      </button>

      {/* Panel */}
      {open && (
        <div className="fixed bottom-20 right-6 z-50 w-96 bg-[var(--surface-strong)] rounded-[16px] border border-[var(--border)] shadow-xl flex flex-col max-h-[80vh]">
          {/* Header */}
          <div className="flex items-center justify-between px-5 py-4 border-b border-[var(--border)]">
            <p className="font-semibold text-[var(--foreground)] text-[13px]">Sync from Google Drive</p>
            <button
              onClick={() => setOpen(false)}
              className="text-[var(--muted-soft)] hover:text-[var(--muted)] transition-colors"
              aria-label="Close"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="overflow-y-auto flex-1 px-5 py-4 space-y-4">
            {/* Loading months */}
            {loadingMonths && (
              <div className="flex items-center gap-2 text-[13px] text-[var(--muted-soft)] py-4 justify-center">
                <Loader2 className="w-4 h-4 animate-spin" />
                Loading months...
              </div>
            )}

            {/* Months error */}
            {monthsError && (
              <div className="flex items-start gap-2 text-sm text-red-600 bg-red-50 rounded-xl p-3">
                <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                <span>{monthsError}</span>
              </div>
            )}

            {/* Month list */}
            {!loadingMonths && !monthsError && months.length === 0 && (
              <p className="text-[13px] text-[var(--muted-soft)] text-center py-4">No months found in Drive.</p>
            )}

            {!loadingMonths && months.map((entry) => (
              <div
                key={entry.periodId}
                className="flex items-center justify-between gap-3 rounded-[12px] px-4 py-3 border border-[var(--border-strong)] bg-[var(--surface)]"
              >
                <div>
                  <p className={`text-sm font-medium ${entry.alreadySynced ? 'text-[var(--muted-soft)]' : 'text-[var(--foreground)]'}`}>
                    {entry.name}
                  </p>
                  {entry.alreadySynced && (
                    <p className="text-xs text-[var(--muted-soft)] mt-0.5">Already synced</p>
                  )}
                </div>
                <button
                  onClick={() => handleSync(entry)}
                  disabled={syncingId !== null}
                  className={`flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg disabled:opacity-40 disabled:cursor-not-allowed transition-colors ${
                    entry.alreadySynced
                      ? 'bg-[var(--fill-gray)] text-[var(--muted)] hover:bg-[var(--fill-cool)]'
                      : 'bg-[var(--brand)] text-white hover:bg-[var(--brand-deep)]'
                  }`}
                >
                  {syncingId === entry.periodId ? (
                    <>
                      <Loader2 className="w-3 h-3 animate-spin" />
                      Syncing...
                    </>
                  ) : entry.alreadySynced ? (
                    'Re-sync'
                  ) : (
                    'Sync'
                  )}
                </button>
              </div>
            ))}

            {/* Sync log */}
            {syncLog.length > 0 && (
              <div className="mt-2">
                <p className="text-xs font-semibold text-[var(--muted)] mb-1.5 uppercase tracking-wide">
                  Progress log
                </p>
                <div className="bg-[var(--fill-cool)] rounded-[12px] p-3 space-y-0.5 max-h-48 overflow-y-auto font-mono">
                  {syncLog.map((line, i) => (
                    <p key={i} className="text-xs text-[var(--muted)] leading-relaxed">
                      {line}
                    </p>
                  ))}
                </div>
              </div>
            )}

            {/* Sync error */}
            {syncError && (
              <div className="flex items-start gap-2 text-sm text-red-600 bg-red-50 rounded-xl p-3">
                <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                <span>{syncError}</span>
              </div>
            )}

            {/* Sync success */}
            {syncResult && !syncError && (
              <div className="bg-green-50 border border-green-100 rounded-xl p-4 space-y-2">
                <div className="flex items-center gap-2 text-green-700">
                  <CheckCircle className="w-4 h-4 flex-shrink-0" />
                  <p className="text-sm font-semibold">
                    {syncResult.label} synced — {syncResult.clientsSynced.length} client(s)
                  </p>
                </div>
                {syncResult.clientsMissingGHL.length > 0 && (
                  <p className="text-xs text-amber-600">
                    Missing GHL: {syncResult.clientsMissingGHL.join(', ')}
                  </p>
                )}
                {syncResult.errors.length > 0 && (
                  <p className="text-xs text-red-500">
                    {syncResult.errors.length} error(s) — see log above
                  </p>
                )}
                <button
                  onClick={() => window.location.reload()}
                  className="mt-1 w-full text-sm font-semibold bg-green-700 text-white py-2 rounded-lg hover:bg-green-800 transition-colors"
                >
                  Reload dashboard
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}
