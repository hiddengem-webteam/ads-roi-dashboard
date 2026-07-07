import fs from 'fs';
import path from 'path';
import { getAuth, getDriveClient, getSheetsClient } from './driveClient';
import { matchClientNames } from './clientMatcher';
import { parseGHLFilename, mergeCSVFiles } from './ghlUtils';

export interface SyncResult {
  periodId: string;
  label: string;
  clientsSynced: string[];
  clientsMissingGHL: string[];
  log: string[];
  errors: string[];
}

// ─── Internal helpers ─────────────────────────────────────────────────────────

function toPeriodId(label: string): string {
  return label.toLowerCase().replace(/\s+/g, '-');
}

function sanitizeDirName(name: string): string {
  return name.replace(/[<>:"/\\|?*\x00-\x1f]/g, '_').trim();
}

function arrayToCSV(rows: string[][]): string {
  return rows
    .map((row) =>
      row
        .map((cell) => {
          const s = cell == null ? '' : String(cell);
          // Escape if contains comma, quote, or newline
          if (s.includes(',') || s.includes('"') || s.includes('\n') || s.includes('\r')) {
            return '"' + s.replace(/"/g, '""') + '"';
          }
          return s;
        })
        .join(','),
    )
    .join('\n');
}

// ─── Drive helpers ────────────────────────────────────────────────────────────

type DriveFile = { id: string; name: string; mimeType: string };

async function listFolder(
  drive: ReturnType<typeof getDriveClient>,
  folderId: string,
): Promise<DriveFile[]> {
  const files: DriveFile[] = [];
  let pageToken: string | undefined;

  do {
    const res = await drive.files.list({
      q: `'${folderId}' in parents and trashed = false`,
      fields: 'nextPageToken, files(id, name, mimeType)',
      pageSize: 200,
      pageToken,
      supportsAllDrives: true,
      includeItemsFromAllDrives: true,
    });
    const items = res.data.files ?? [];
    for (const f of items) {
      if (f.id && f.name && f.mimeType) {
        files.push({ id: f.id, name: f.name, mimeType: f.mimeType });
      }
    }
    pageToken = res.data.nextPageToken ?? undefined;
  } while (pageToken);

  return files;
}

async function downloadCSV(
  drive: ReturnType<typeof getDriveClient>,
  fileId: string,
): Promise<string> {
  const res = await drive.files.get(
    { fileId, alt: 'media', supportsAllDrives: true },
    { responseType: 'text' },
  );
  return res.data as string;
}

// ─── Main orchestration ───────────────────────────────────────────────────────

export async function syncPeriod(
  monthFolderId: string,
  label: string,
  onLog?: (msg: string) => void,
): Promise<SyncResult> {
  const log: string[] = [];
  const errors: string[] = [];
  const clientsSynced: string[] = [];
  const clientsMissingGHL: string[] = [];

  function emit(msg: string) {
    log.push(msg);
    onLog?.(msg);
  }

  const periodId = toPeriodId(label);
  const publicDir = path.join(process.cwd(), 'public');
  const periodDir = path.join(publicDir, 'data', 'periods', periodId);
  const sharedDir = path.join(periodDir, 'shared');
  const clientsBaseDir = path.join(periodDir, 'clients');

  fs.mkdirSync(sharedDir, { recursive: true });
  fs.mkdirSync(clientsBaseDir, { recursive: true });

  emit(`Syncing period: ${label} (${periodId})`);

  const auth = getAuth();
  const drive = getDriveClient(auth);
  const sheets = getSheetsClient(auth);

  // 1. List month folder contents
  emit('Listing month folder...');
  const monthContents = await listFolder(drive, monthFolderId);

  // Find subfolders by keyword
  function findFolder(keyword: string): DriveFile | undefined {
    return monthContents.find(
      (f) =>
        f.mimeType === 'application/vnd.google-apps.folder' &&
        f.name.toLowerCase().includes(keyword.toLowerCase()),
    );
  }

  const pmsFolder = findFolder('direct booking');
  const ghlFolder = findFolder('ghl');
  const metaAdsFolder = findFolder('meta ads');
  const promoCodesFolder = findFolder('promo');

  emit(
    `Folders found — PMS: ${pmsFolder?.name ?? 'none'}, GHL: ${ghlFolder?.name ?? 'none'}, Meta: ${metaAdsFolder?.name ?? 'none'}, Promo: ${promoCodesFolder?.name ?? 'none'}`,
  );

  // ── 2. Meta Ads ──────────────────────────────────────────────────────────────
  const manifestClients: Array<{ name: string; pms: string; ghl: string }> = [];
  let metaAdsCsvPath = '';
  let promoCodesCsvPath = '';

  if (metaAdsFolder) {
    emit('Downloading Meta Ads CSV...');
    try {
      const metaFiles = await listFolder(drive, metaAdsFolder.id);
      const csvFile = metaFiles.find((f) => f.name.toLowerCase().endsWith('.csv'));
      if (csvFile) {
        const content = await downloadCSV(drive, csvFile.id);
        const dest = path.join(sharedDir, 'Meta Ads.csv');
        fs.writeFileSync(dest, content, 'utf8');
        metaAdsCsvPath = `/data/periods/${periodId}/shared/Meta Ads.csv`;
        emit(`Meta Ads saved: ${csvFile.name}`);
      } else {
        emit('No CSV found in Meta Ads folder.');
      }
    } catch (err) {
      const msg = `Meta Ads error: ${err}`;
      errors.push(msg);
      emit(msg);
    }
  }

  // ── 3. Promo Codes ───────────────────────────────────────────────────────────
  if (promoCodesFolder) {
    emit('Downloading Promo Codes CSV...');
    try {
      const promoFiles = await listFolder(drive, promoCodesFolder.id);
      const csvFile = promoFiles.find((f) => f.name.toLowerCase().endsWith('.csv'));
      if (csvFile) {
        const content = await downloadCSV(drive, csvFile.id);
        const dest = path.join(sharedDir, 'Promo codes.csv');
        fs.writeFileSync(dest, content, 'utf8');
        promoCodesCsvPath = `/data/periods/${periodId}/shared/Promo codes.csv`;
        emit(`Promo Codes saved: ${csvFile.name}`);
      } else {
        emit('No CSV found in Promo Codes folder.');
      }
    } catch (err) {
      const msg = `Promo Codes error: ${err}`;
      errors.push(msg);
      emit(msg);
    }
  }

  // ── 4. PMS (Google Sheets) ───────────────────────────────────────────────────
  const pmsDataByTab: Record<string, string> = {}; // tabName → CSV string
  const SKIP_TABS = new Set(['summary', 'template', 'instructions', 'index', 'overview']);

  if (pmsFolder) {
    emit('Processing PMS Google Sheets...');
    try {
      const pmsFiles = await listFolder(drive, pmsFolder.id);
      const sheetFiles = pmsFiles.filter(
        (f) => f.mimeType === 'application/vnd.google-apps.spreadsheet',
      );
      emit(`Found ${sheetFiles.length} spreadsheet(s) in PMS folder.`);

      for (const sheetFile of sheetFiles) {
        emit(`  Reading sheet: ${sheetFile.name}`);
        try {
          const meta = await sheets.spreadsheets.get({
            spreadsheetId: sheetFile.id,
            fields: 'sheets.properties.title',
            includeGridData: false,
          });
          const tabs = (meta.data.sheets ?? []).map((s) => s.properties?.title ?? '');

          for (const tab of tabs) {
            if (!tab) continue;
            if (SKIP_TABS.has(tab.toLowerCase())) {
              emit(`    Skipping tab: ${tab}`);
              continue;
            }

            try {
              const valRes = await sheets.spreadsheets.values.get({
                spreadsheetId: sheetFile.id,
                range: `'${tab}'`,
              });
              const values = valRes.data.values as string[][] | null | undefined;
              if (!values || values.length < 2) {
                emit(`    Skipping tab "${tab}" — fewer than 2 rows`);
                continue;
              }
              pmsDataByTab[tab] = arrayToCSV(values);
              emit(`    Tab "${tab}" — ${values.length} rows`);
            } catch (tabErr) {
              const msg = `    Error reading tab "${tab}": ${tabErr}`;
              errors.push(msg);
              emit(msg);
            }
          }
        } catch (sheetErr) {
          const msg = `  Error reading sheet "${sheetFile.name}": ${sheetErr}`;
          errors.push(msg);
          emit(msg);
        }
      }
    } catch (err) {
      const msg = `PMS folder error: ${err}`;
      errors.push(msg);
      emit(msg);
    }
  }

  // ── 5. GHL CSVs ──────────────────────────────────────────────────────────────
  const ghlContentsByClient: Record<string, string[]> = {}; // clientName → [csv, ...]

  if (ghlFolder) {
    emit('Processing GHL CSVs...');
    try {
      const ghlFiles = await listFolder(drive, ghlFolder.id);
      const csvFiles = ghlFiles.filter((f) => f.name.toLowerCase().endsWith('.csv'));
      emit(`Found ${csvFiles.length} CSV file(s) in GHL folder.`);

      for (const csvFile of csvFiles) {
        const parsed = parseGHLFilename(csvFile.name);
        if (parsed.clientName === null) {
          emit(`  Skipping generic file: ${csvFile.name}`);
          continue;
        }
        emit(`  GHL file: ${csvFile.name} → client: "${parsed.clientName}", type: ${parsed.type}`);
        try {
          const content = await downloadCSV(drive, csvFile.id);
          if (!ghlContentsByClient[parsed.clientName]) {
            ghlContentsByClient[parsed.clientName] = [];
          }
          ghlContentsByClient[parsed.clientName].push(content);
        } catch (dlErr) {
          const msg = `  Error downloading ${csvFile.name}: ${dlErr}`;
          errors.push(msg);
          emit(msg);
        }
      }
    } catch (err) {
      const msg = `GHL folder error: ${err}`;
      errors.push(msg);
      emit(msg);
    }
  }

  // ── 6. Match PMS tabs to GHL clients ─────────────────────────────────────────
  const pmsTabNames = Object.keys(pmsDataByTab);
  const ghlClientNames = Object.keys(ghlContentsByClient);
  const matchMap = matchClientNames(pmsTabNames, ghlClientNames);

  emit(`Matching ${pmsTabNames.length} PMS tab(s) to ${ghlClientNames.length} GHL client(s)...`);

  // ── 7. Write per-client files ─────────────────────────────────────────────────
  for (const tabName of pmsTabNames) {
    const safeName = sanitizeDirName(tabName);
    const clientDir = path.join(clientsBaseDir, safeName);
    fs.mkdirSync(clientDir, { recursive: true });

    // Write PMS
    const pmsDest = path.join(clientDir, 'PMS data.csv');
    fs.writeFileSync(pmsDest, pmsDataByTab[tabName], 'utf8');

    const ghlMatchName = matchMap.get(tabName) ?? null;
    let ghlPath = '';

    if (ghlMatchName && ghlContentsByClient[ghlMatchName]) {
      const merged = mergeCSVFiles(ghlContentsByClient[ghlMatchName]);
      const ghlDest = path.join(clientDir, 'GHL data.csv');
      fs.writeFileSync(ghlDest, merged, 'utf8');
      ghlPath = `/data/periods/${periodId}/clients/${safeName}/GHL data.csv`;
      emit(`  Client "${tabName}" — PMS saved, GHL matched to "${ghlMatchName}"`);
      clientsSynced.push(tabName);
    } else {
      emit(`  Client "${tabName}" — PMS saved, no GHL match found`);
      clientsMissingGHL.push(tabName);
      clientsSynced.push(tabName);
    }

    manifestClients.push({
      name: tabName,
      pms: `/data/periods/${periodId}/clients/${safeName}/PMS data.csv`,
      ghl: ghlPath,
    });
  }

  // ── 8. Update manifest.json ───────────────────────────────────────────────────
  const manifestPath = path.join(publicDir, 'data', 'manifest.json');
  let manifest: {
    periods: Array<{
      id: string;
      label: string;
      metaAds: string;
      promoCodes: string;
      clients: Array<{ name: string; pms: string; ghl: string }>;
    }>;
  } = { periods: [] };

  if (fs.existsSync(manifestPath)) {
    try {
      manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    } catch {
      emit('Warning: could not parse existing manifest.json — starting fresh.');
    }
  }

  // Remove existing entry with same id
  manifest.periods = manifest.periods.filter((p) => p.id !== periodId);

  // Prepend new entry
  manifest.periods.unshift({
    id: periodId,
    label,
    metaAds: metaAdsCsvPath,
    promoCodes: promoCodesCsvPath,
    clients: manifestClients,
  });

  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n', 'utf8');
  emit(`manifest.json updated — ${manifest.periods.length} period(s) total.`);

  emit(
    `Done. Synced ${clientsSynced.length} client(s), ${clientsMissingGHL.length} missing GHL.`,
  );

  return { periodId, label, clientsSynced, clientsMissingGHL, log, errors };
}
