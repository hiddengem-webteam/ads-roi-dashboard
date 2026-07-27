import fs from 'fs';
import path from 'path';
import {
  getPlatformConfig,
  platformGet,
  PlatformConfig,
  PlatformClient,
  RoiExportResponse,
  RoiExportTenant,
  PlatformContact,
} from './platformClient';

// Pulls data from the HiddenGem AI platform API and writes the SAME CSV files +
// manifest.json the dashboard already loads (mirroring the Google Drive sync in
// ./syncPeriod.ts). The client-side load/parse/analysis pipeline is untouched.
//
//   syncPlatformPeriod(from, to, label)  — one explicit period
//   syncAllPlatformPeriods(opts)         — backfill every month with data
//
// Coverage vs. the 4 dashboard inputs:
//   • Meta Ads — full (per-campaign spend/impressions/link clicks/leads/purchases/value)
//   • PMS      — direct bookings: guest/email/revenue/check-in (no coupon/listing/checkout/source)
//   • GHL      — contacts: id/name/phone/email/created/tags (name is one field; tags in `role`).
//                Contacts are all-time (not date-filtered), so they're fetched once and reused
//                across every month — the same GHL data backs every period for a client.
//   • Promo    — NOT on the platform; a manually-placed Promo codes.csv in the period's
//                shared/ dir is preserved and referenced (hybrid).

const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const MONTH_RE = /^(\d{4})-(\d{2})$/;

const MONTH_NAMES = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

const META_HEADERS = [
  'Account name', 'Campaign name', 'Amount spent', 'Link clicks',
  'Leads', 'Impressions', 'Purchases', 'Purchases conversion value',
];
const PMS_HEADERS = ['Guest', 'Email', 'Revenue', 'Check-in date'];
const GHL_HEADERS = ['Contact Id', 'First Name', 'Last Name', 'Phone', 'Email', 'Created', 'Tags'];

// ─── Result shapes ────────────────────────────────────────────────────────────

export interface PlatformSyncResult {
  periodId: string;
  label: string;
  from: string;
  to: string;
  clientsSynced: string[];
  clientsMissingPMS: string[];
  clientsMissingGHL: string[];
  log: string[];
  errors: string[];
}

export interface SyncAllOptions {
  startMonth?: string; // 'YYYY-MM' — earliest month to sync (inclusive); default: auto-discover
  maxMonths?: number; // hard cap on how far back to look (default 36)
  stopAfterEmpty?: number; // stop after N consecutive empty months when auto-discovering (default 3)
  refreshRecentMonths?: number; // always re-sync the newest N months (default 2)
  skipExisting?: boolean; // skip older months already present in manifest.json (default false)
  onLog?: (msg: string) => void;
}

export interface PlatformSyncAllResult {
  periodsSynced: Array<{ periodId: string; label: string; clients: number }>;
  periodsEmpty: string[];
  periodsSkipped: string[];
  totalClients: number;
  log: string[];
  errors: string[];
}

// ─── Internal types ───────────────────────────────────────────────────────────

interface ManifestPeriod {
  id: string;
  label: string;
  metaAds: string;
  promoCodes: string;
  clients: Array<{ name: string; pms: string; ghl: string }>;
}

interface RunCtx {
  cfg: PlatformConfig;
  publicDir: string;
  contactsCache: Map<string, PlatformContact[]>;
  contactsErrored: Set<string>;
  log: string[];
  errors: string[];
  emit: (msg: string) => void;
}

interface WritePeriodOutcome {
  period: ManifestPeriod | null;
  synced: string[];
  missingPMS: string[];
  missingGHL: string[];
}

// ─── Small helpers ────────────────────────────────────────────────────────────

function toPeriodId(label: string): string {
  return label.toLowerCase().replace(/\s+/g, '-');
}

function sanitizeDirName(name: string): string {
  return name.replace(/[<>:"/\\|?*\x00-\x1f]/g, '_').trim();
}

function csvCell(v: unknown): string {
  const s = v == null ? '' : String(v);
  return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

function toCSV(headers: string[], rows: unknown[][]): string {
  return [headers, ...rows].map((r) => r.map(csvCell).join(',')).join('\n') + '\n';
}

/** Split a single "First Last" name into the first/last columns the GHL parser expects. */
function splitName(full: string | null): { first: string; last: string } {
  const s = (full ?? '').trim();
  if (!s) return { first: '', last: '' };
  const parts = s.split(/\s+/);
  return { first: parts[0], last: parts.slice(1).join(' ') };
}

const pad2 = (n: number) => String(n).padStart(2, '0');

/** Inclusive from/to + label for a 1-based (year, month). */
function monthWindow(year: number, mon: number): { from: string; to: string; label: string } {
  const lastDay = new Date(Date.UTC(year, mon, 0)).getUTCDate(); // day 0 of next month = last day of this
  return {
    from: `${year}-${pad2(mon)}-01`,
    to: `${year}-${pad2(mon)}-${pad2(lastDay)}`,
    label: `${MONTH_NAMES[mon - 1]} ${year}`,
  };
}

/** Month windows from the current month backwards, optionally bounded by startMonth. */
function buildWindows(maxMonths: number, startMonth?: string): Array<{ from: string; to: string; label: string }> {
  const now = new Date();
  let y = now.getUTCFullYear();
  let m = now.getUTCMonth() + 1; // 1-12

  let startY = Number.NEGATIVE_INFINITY;
  let startM = 0;
  const mm = startMonth ? MONTH_RE.exec(startMonth) : null;
  if (mm) {
    startY = Number(mm[1]);
    startM = Number(mm[2]);
  }

  const out: Array<{ from: string; to: string; label: string }> = [];
  for (let i = 0; i < maxMonths; i++) {
    out.push(monthWindow(y, m));
    if (mm && y === startY && m === startM) break; // reached the requested earliest month
    m -= 1;
    if (m === 0) {
      m = 12;
      y -= 1;
    }
  }
  return out;
}

function makeCtx(cfg: PlatformConfig, onLog?: (msg: string) => void): RunCtx {
  const log: string[] = [];
  const errors: string[] = [];
  return {
    cfg,
    publicDir: path.join(process.cwd(), 'public'),
    contactsCache: new Map(),
    contactsErrored: new Set(),
    log,
    errors,
    emit: (msg: string) => {
      log.push(msg);
      onLog?.(msg);
    },
  };
}

async function fetchClients(ctx: RunCtx): Promise<Map<string, string>> {
  ctx.emit('Fetching client list...');
  const { clients } = await platformGet<{ clients: PlatformClient[] }>(ctx.cfg, '/api/v1/clients?all=1');
  ctx.emit(`Found ${clients.length} client(s).`);
  return new Map(clients.map((c) => [c.id, c.name]));
}

// Only clients with Meta ad data are materialized. The dashboard is ad-ROI
// focused and only shows clients with ad stats, so booking-only clients (and
// whole booking-only months) are hidden — per Shawal (Jul 2026), older months
// with no ad data should not appear.
function usableEntries(roi: RoiExportResponse): Array<[string, RoiExportTenant]> {
  // Guard against a 200 whose body lacks `tenants` (or is null) so a single
  // malformed month can't throw out of the whole backfill loop.
  return Object.entries(roi?.tenants ?? {}).filter(([, t]) => t.campaigns.length > 0);
}

/** Fetch a tenant's contacts once and cache them (contacts are all-time, not per-month). */
async function getContacts(ctx: RunCtx, tenantId: string): Promise<PlatformContact[]> {
  const cached = ctx.contactsCache.get(tenantId);
  if (cached) return cached;
  const { contacts } = await platformGet<{ contacts: PlatformContact[] }>(
    ctx.cfg,
    `/api/v1/clients/${tenantId}/contacts`,
  );
  const list = contacts ?? [];
  ctx.contactsCache.set(tenantId, list);
  return list;
}

/** Period ids already present in manifest.json (used to skip already-synced months). */
function readManifestIds(publicDir: string): Set<string> {
  const manifestPath = path.join(publicDir, 'data', 'manifest.json');
  if (!fs.existsSync(manifestPath)) return new Set();
  try {
    const m = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    return new Set<string>((m.periods ?? []).map((p: { id: string }) => p.id));
  } catch {
    return new Set();
  }
}

/** Sort key for a "Month YYYY" label → YYYYMM (unparseable labels sort last). */
function labelSortKey(label: string): number {
  const parts = label.trim().split(/\s+/);
  const month = MONTH_NAMES.findIndex((m) => m.toLowerCase() === (parts[0] ?? '').toLowerCase()) + 1;
  const year = parseInt(parts[1] ?? '', 10);
  if (!month || Number.isNaN(year)) return 0;
  return year * 100 + month;
}

/** Load, upsert, and rewrite manifest.json, ordering periods newest-first. */
function upsertPeriods(ctx: RunCtx, periods: ManifestPeriod[]): void {
  const manifestPath = path.join(ctx.publicDir, 'data', 'manifest.json');
  let manifest: { periods: ManifestPeriod[] } = { periods: [] };
  if (fs.existsSync(manifestPath)) {
    try {
      manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    } catch {
      ctx.emit('Warning: existing manifest.json unparseable — starting fresh.');
    }
  }
  const newIds = new Set(periods.map((p) => p.id));
  const kept = (manifest.periods ?? []).filter((p) => !newIds.has(p.id));
  // Sort by date, newest first — don't rely on insertion order, so backfilling
  // an older month never lands it ahead of a newer one (the dashboard renders
  // the manifest in array order and defaults to periods[0]).
  manifest.periods = [...periods, ...kept].sort((a, b) => labelSortKey(b.label) - labelSortKey(a.label));
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n', 'utf8');
  ctx.emit(`manifest.json updated — ${manifest.periods.length} period(s) total.`);
}

/** Write one period's Meta/PMS/GHL files from its roi-export tenants; returns its manifest entry. */
async function writePeriod(
  ctx: RunCtx,
  periodId: string,
  label: string,
  tenantEntries: Array<[string, RoiExportTenant]>,
  nameById: Map<string, string>,
): Promise<WritePeriodOutcome> {
  const periodDir = path.join(ctx.publicDir, 'data', 'periods', periodId);
  const sharedDir = path.join(periodDir, 'shared');
  const clientsBaseDir = path.join(periodDir, 'clients');
  fs.mkdirSync(sharedDir, { recursive: true });
  fs.mkdirSync(clientsBaseDir, { recursive: true });

  // Shared Meta Ads.csv (Account name = client name so aggregateFacebookStats groups right)
  const metaRows: unknown[][] = [];
  for (const [tid, t] of tenantEntries) {
    const clientName = nameById.get(tid) ?? tid;
    for (const c of t.campaigns) {
      metaRows.push([
        clientName,
        c.campaign_name ?? '',
        c.spend ?? 0,
        c.link_clicks ?? 0, // true link clicks (not Meta's "clicks (all)")
        c.leads ?? 0,
        c.impressions ?? 0,
        c.purchases ?? 0,
        c.revenue ?? 0, // null (untracked) collapses to 0 for the CSV
      ]);
    }
  }
  fs.writeFileSync(path.join(sharedDir, 'Meta Ads.csv'), toCSV(META_HEADERS, metaRows), 'utf8');
  const metaAdsPath = `/data/periods/${periodId}/shared/Meta Ads.csv`;

  const clients: ManifestPeriod['clients'] = [];
  const synced: string[] = [];
  const missingPMS: string[] = [];
  const missingGHL: string[] = [];

  for (const [tid, t] of tenantEntries) {
    const clientName = nameById.get(tid) ?? tid;
    const safe = sanitizeDirName(clientName);
    const clientDir = path.join(clientsBaseDir, safe);
    fs.mkdirSync(clientDir, { recursive: true });

    let pmsPath = '';
    let ghlPath = '';

    // PMS ← direct bookings
    if (t.direct_bookings.length > 0) {
      const pmsRows = t.direct_bookings.map((b) => [b.guest ?? '', b.email ?? '', b.revenue ?? 0, b.check_in ?? '']);
      fs.writeFileSync(path.join(clientDir, 'PMS data.csv'), toCSV(PMS_HEADERS, pmsRows), 'utf8');
      pmsPath = `/data/periods/${periodId}/clients/${safe}/PMS data.csv`;
    } else {
      missingPMS.push(clientName);
    }

    // GHL ← contacts (cached across months)
    let contacts: PlatformContact[] = [];
    try {
      contacts = await getContacts(ctx, tid);
    } catch (err) {
      if (!ctx.contactsErrored.has(tid)) {
        ctx.errors.push(`${clientName}: GHL fetch error: ${err}`);
        ctx.contactsErrored.add(tid);
      }
      ctx.contactsCache.set(tid, []); // don't retry this tenant every month
    }
    if (contacts.length > 0) {
      const ghlRows = contacts.map((c) => {
        const { first, last } = splitName(c.name);
        return [c.id ?? '', first, last, c.phone ?? '', c.email ?? '', c.created_at ?? '', c.role ?? ''];
      });
      fs.writeFileSync(path.join(clientDir, 'GHL data.csv'), toCSV(GHL_HEADERS, ghlRows), 'utf8');
      ghlPath = `/data/periods/${periodId}/clients/${safe}/GHL data.csv`;
    } else {
      missingGHL.push(clientName);
    }

    clients.push({ name: clientName, pms: pmsPath, ghl: ghlPath });
    synced.push(clientName);
  }

  // Promo codes aren't on the platform — preserve a manually-placed file (hybrid).
  let promoCodesPath = '';
  if (fs.existsSync(path.join(sharedDir, 'Promo codes.csv'))) {
    promoCodesPath = `/data/periods/${periodId}/shared/Promo codes.csv`;
  }

  ctx.emit(`  ${label}: ${synced.length} client(s), ${metaRows.length} campaign row(s).`);
  return {
    period: { id: periodId, label, metaAds: metaAdsPath, promoCodes: promoCodesPath, clients },
    synced,
    missingPMS,
    missingGHL,
  };
}

// ─── Public: single period ────────────────────────────────────────────────────

export async function syncPlatformPeriod(
  from: string,
  to: string,
  label: string,
  onLog?: (msg: string) => void,
): Promise<PlatformSyncResult> {
  if (!DATE_RE.test(from) || !DATE_RE.test(to) || from > to) {
    throw new Error('from and to are required as YYYY-MM-DD with from <= to');
  }
  if (!label.trim()) throw new Error('label is required');

  const cfg = getPlatformConfig();
  const ctx = makeCtx(cfg, onLog);
  const periodId = toPeriodId(label);

  ctx.emit(`Syncing "${label}" (${periodId}) from HiddenGem API — ${from} → ${to}`);
  ctx.emit(`Platform: ${cfg.baseUrl}`);

  const nameById = await fetchClients(ctx);
  ctx.emit('Fetching ROI export (Meta insights + direct bookings)...');
  const roi = await platformGet<RoiExportResponse>(cfg, `/api/v1/admin/roi-export?from=${from}&to=${to}`);
  const entries = usableEntries(roi);

  if (entries.length === 0) {
    ctx.emit('No ad data for this period — nothing written.');
    return {
      periodId, label, from, to,
      clientsSynced: [], clientsMissingPMS: [], clientsMissingGHL: [],
      log: ctx.log, errors: ctx.errors,
    };
  }

  const outcome = await writePeriod(ctx, periodId, label, entries, nameById);
  if (outcome.period) upsertPeriods(ctx, [outcome.period]);

  ctx.emit(
    `Done. ${outcome.synced.length} client(s) — ${outcome.missingPMS.length} without PMS, ${outcome.missingGHL.length} without GHL.`,
  );
  return {
    periodId, label, from, to,
    clientsSynced: outcome.synced,
    clientsMissingPMS: outcome.missingPMS,
    clientsMissingGHL: outcome.missingGHL,
    log: ctx.log,
    errors: ctx.errors,
  };
}

// ─── Public: backfill all months ──────────────────────────────────────────────

export async function syncAllPlatformPeriods(opts: SyncAllOptions = {}): Promise<PlatformSyncAllResult> {
  const maxMonths = opts.maxMonths ?? 36;
  const stopAfterEmpty = opts.stopAfterEmpty ?? 3;
  const refreshRecentMonths = opts.refreshRecentMonths ?? 2;
  const skipExisting = opts.skipExisting ?? false;

  const cfg = getPlatformConfig();
  const ctx = makeCtx(cfg, opts.onLog);

  ctx.emit(
    opts.startMonth
      ? `Backfilling months ${opts.startMonth} → now from HiddenGem API...`
      : `Backfilling all months from HiddenGem API (auto-discover, cap ${maxMonths} months)...`,
  );
  ctx.emit(`Platform: ${cfg.baseUrl}`);
  if (skipExisting) {
    ctx.emit(`Incremental: refreshing newest ${refreshRecentMonths} month(s), skipping already-synced older months.`);
  }

  const nameById = await fetchClients(ctx);
  const windows = buildWindows(maxMonths, opts.startMonth);
  const existingIds = skipExisting ? readManifestIds(ctx.publicDir) : new Set<string>();

  const newPeriods: ManifestPeriod[] = [];
  const periodsSynced: PlatformSyncAllResult['periodsSynced'] = [];
  const periodsEmpty: string[] = [];
  const periodsSkipped: string[] = [];
  let totalClients = 0;
  let consecutiveEmpty = 0;

  for (let idx = 0; idx < windows.length; idx++) {
    const w = windows[idx];
    const periodId = toPeriodId(w.label);

    // Incremental: skip older months already synced (but always refresh the newest few,
    // which are still accumulating bookings/insights). A skipped month has data, so it
    // resets the empty counter and never triggers the early-stop.
    if (skipExisting && idx >= refreshRecentMonths && existingIds.has(periodId)) {
      periodsSkipped.push(w.label);
      consecutiveEmpty = 0;
      ctx.emit(`— ${w.label} — already synced, skipping`);
      continue;
    }

    ctx.emit(`— ${w.label} (${w.from} → ${w.to}) —`);
    let roi: RoiExportResponse;
    try {
      roi = await platformGet<RoiExportResponse>(cfg, `/api/v1/admin/roi-export?from=${w.from}&to=${w.to}`);
    } catch (err) {
      ctx.errors.push(`${w.label}: roi-export error: ${err}`);
      ctx.emit(`  error: ${err}`);
      // A transient error is "unknown", not "empty" — reset so it can't bridge
      // surrounding empty months into a premature early-stop.
      consecutiveEmpty = 0;
      continue;
    }

    const entries = usableEntries(roi);
    if (entries.length === 0) {
      periodsEmpty.push(w.label);
      consecutiveEmpty += 1;
      ctx.emit('  no ad data — hidden');
      // Only auto-stop when discovering; an explicit startMonth syncs the full range.
      if (!opts.startMonth && consecutiveEmpty >= stopAfterEmpty) {
        ctx.emit(`Stopping — ${stopAfterEmpty} consecutive months with no ad data (assuming none older).`);
        break;
      }
      continue;
    }

    consecutiveEmpty = 0;
    const outcome = await writePeriod(ctx, periodId, w.label, entries, nameById);
    if (outcome.period) {
      newPeriods.push(outcome.period);
      periodsSynced.push({ periodId: outcome.period.id, label: w.label, clients: outcome.synced.length });
      totalClients += outcome.synced.length;
    }
  }

  if (newPeriods.length > 0) {
    upsertPeriods(ctx, newPeriods);
  } else if (periodsSkipped.length > 0) {
    ctx.emit('All months already synced — nothing to refresh.');
  } else {
    ctx.emit('No months with data found.');
  }

  ctx.emit(
    `Done. ${periodsSynced.length} month(s) synced, ${periodsSkipped.length} skipped, ${periodsEmpty.length} empty.`,
  );
  return { periodsSynced, periodsEmpty, periodsSkipped, totalClients, log: ctx.log, errors: ctx.errors };
}
