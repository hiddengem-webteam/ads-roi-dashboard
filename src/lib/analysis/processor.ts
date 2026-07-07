import { ProcessedData, ClientData, Flag } from '@/types';

// Words stripped when normalizing names for fuzzy matching
const NOISE_WORDS = /\b(updated|new|ads|ad account|account|direct|v2|v3|2\.0|3\.0|resort|cabins|cabin|retreat|rentals|rental|stays|lodge|lodging|glamping|farms|farm|ranch|villas|villa|inn|springs|lake|falls|hills|mountain|river|creek|woods|forest|park|beach|bay|coast|island|heights|estates|house|home|homes|bnbs|bnb)\b/gi;

function normalizeName(name: string): string {
  return name
    .toLowerCase()
    .replace(NOISE_WORDS, ' ')
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function levenshtein(a: string, b: string): number {
  const m = a.length, n = b.length;
  const dp: number[][] = Array.from({ length: m + 1 }, (_, i) => [i, ...Array(n).fill(0)]);
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++)
    for (let j = 1; j <= n; j++)
      dp[i][j] = a[i-1] === b[j-1] ? dp[i-1][j-1] : 1 + Math.min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]);
  return dp[m][n];
}

/** Strip all whitespace for compound-word comparison (e.g. "Homebase" ↔ "Home Base BNBs") */
function stripSpaces(s: string): string {
  return s.toLowerCase().replace(/\s+/g, '');
}

/**
 * Try to map a manifest client name to a known FB canonical name.
 * Falls back to the original name if no confident match is found.
 */
function resolveToFBName(manifestName: string, fbNames: string[]): string {
  if (!fbNames.length) return manifestName;
  // 1. Exact match
  if (fbNames.includes(manifestName)) return manifestName;
  // 2. Case-insensitive exact
  const ci = fbNames.find(f => f.toLowerCase() === manifestName.toLowerCase());
  if (ci) return ci;
  // 3. One contains the other (case-insensitive)
  const mLower = manifestName.toLowerCase();
  const contains = fbNames.find(f => {
    const fLower = f.toLowerCase();
    return fLower.includes(mLower) || mLower.includes(fLower);
  });
  if (contains) return contains;
  // 4. Compound-word match: strip all spaces and compare
  //    Handles "Homebase" ↔ "Home Base BNBs", "Stayon30a" ↔ "Stay on 30a"
  const mStripped = stripSpaces(manifestName);
  const compoundMatch = fbNames.find(f => {
    const fStripped = stripSpaces(f);
    return fStripped.startsWith(mStripped) || mStripped.startsWith(fStripped) ||
      fStripped.includes(mStripped) || mStripped.includes(fStripped);
  });
  if (compoundMatch) return compoundMatch;
  // 5. Normalized name comparison (strips noise words like "Updated", "Ads", etc.)
  const mNorm = normalizeName(manifestName);
  if (!mNorm) return manifestName;
  const exactNorm = fbNames.find(f => normalizeName(f) === mNorm);
  if (exactNorm) return exactNorm;
  // 6. Levenshtein on normalized names (allow up to 3 edits)
  let best: string | null = null;
  let bestDist = 4;
  for (const f of fbNames) {
    const fNorm = normalizeName(f);
    if (!fNorm) continue;
    const dist = levenshtein(mNorm, fNorm);
    if (dist < bestDist) { bestDist = dist; best = f; }
  }
  return best ?? manifestName;
}

/** Remap file keys from manifest names to FB canonical names where possible */
function remapClientKeys(
  files: Record<string, File>,
  fbNames: string[],
): Record<string, File> {
  const result: Record<string, File> = {};
  for (const [manifestName, file] of Object.entries(files)) {
    const resolved = resolveToFBName(manifestName, fbNames);
    result[resolved] = file;
  }
  return result;
}
import { parseFacebookAds } from '@/lib/parsers/facebookAds';
import { parsePromoCodes, groupPromosByClient, findClientPromos } from '@/lib/parsers/promoCodes';
import { parsePMSData } from '@/lib/parsers/pmsData';
import { parseGHLLeads, filterByTag } from '@/lib/parsers/ghlLeads';
import { aggregateFacebookStats } from '@/lib/analysis/campaignAnalysis';
import { analyzePromoCodes } from '@/lib/analysis/promoAnalysis';
import { analyzeLeads } from '@/lib/analysis/leadAnalysis';
import { flagId } from '@/lib/utils';

export interface UploadedFilesMap {
  metaAds: File | null;
  promoCodes: File | null;
  pmsFiles: Record<string, File>; // clientName → file
  ghlFiles: Record<string, File>; // clientName → file
}

export async function processAllData(files: UploadedFilesMap): Promise<ProcessedData> {
  const allFlags: Flag[] = [];
  const clients: Record<string, ClientData> = {};

  // 1. Parse Meta Ads
  let fbStats: Record<string, import('@/types').ClientFacebookStats> = {};
  if (files.metaAds) {
    const rows = await parseFacebookAds(files.metaAds);
    fbStats = aggregateFacebookStats(rows);
    for (const [name, stats] of Object.entries(fbStats)) {
      if (!clients[name]) clients[name] = { name, facebookStats: null, pmsAnalysis: null, hasPMS: false, hasGHL: false };
      clients[name].facebookStats = stats;
    }
  }

  // 2. Parse Promo Codes
  let promosByClient: Record<string, import('@/types').PromoCodeRow[]> = {};
  if (files.promoCodes) {
    const promoRows = await parsePromoCodes(files.promoCodes);
    promosByClient = groupPromosByClient(promoRows);
  }

  // 3. Remap PMS/GHL file keys to canonical FB names using fuzzy matching.
  //    This handles cases where Google Sheets tab names differ slightly from
  //    the FB account canonical names (e.g. "Endless Stays Updated" → "Endless Stays").
  const fbClientNames = Object.keys(clients); // populated from FB data in step 1
  files.pmsFiles = remapClientKeys(files.pmsFiles, fbClientNames);
  files.ghlFiles = remapClientKeys(files.ghlFiles, fbClientNames);

  // 4. Parse PMS + GHL per client
  const pmsClientNames = Object.keys(files.pmsFiles);
  const ghlClientNames = Object.keys(files.ghlFiles);
  const allPmsGhlClients = new Set([...pmsClientNames, ...ghlClientNames]);

  for (const clientName of allPmsGhlClients) {
    if (!clients[clientName]) {
      clients[clientName] = { name: clientName, facebookStats: null, pmsAnalysis: null, hasPMS: false, hasGHL: false };
    }

    const pmsFile = files.pmsFiles[clientName];
    const ghlFile = files.ghlFiles[clientName];

    clients[clientName].hasPMS = !!pmsFile;
    clients[clientName].hasGHL = !!ghlFile;

    if (!pmsFile && !ghlFile) continue;

    const clientPromos = findClientPromos(clientName, promosByClient);

    // Parse PMS
    let pmsRows: import('@/types').PMSRow[] = [];
    let isNetIncome = false;
    let hasCouponColumn = false;
    let hasEmailColumn = false;
    let hasSourceColumn = false;

    if (pmsFile) {
      try {
        const pmsResult = await parsePMSData(pmsFile);
        pmsRows = pmsResult.rows;
        isNetIncome = pmsResult.isNetIncome;
        hasCouponColumn = pmsResult.hasCouponColumn;
        hasEmailColumn = pmsResult.hasEmailColumn;
        hasSourceColumn = pmsResult.hasSourceColumn;

        if (isNetIncome) {
          allFlags.push({
            id: flagId('net-income-warning', clientName),
            type: 'net-income-warning',
            clientName,
            message: `${clientName}: Revenue column is NET INCOME — verify totals`,
            details: 'PMS uses NET INCOME instead of gross revenue. Numbers may reflect payouts, not total booking value.',
          });
        }

        if (!hasEmailColumn) {
          allFlags.push({
            id: flagId('name-only-match', clientName, 'no-email'),
            type: 'name-only-match',
            clientName,
            message: `${clientName}: PMS has no email column — GHL matching uses name only`,
            details: 'Matches flagged for manual verification',
          });
        }
      } catch (err) {
        allFlags.push({
          id: flagId('no-pms-data', clientName),
          type: 'no-pms-data',
          clientName,
          message: `${clientName}: PMS parse error`,
          details: String(err),
        });
      }
    }

    // Flag missing GHL when PMS exists but no GHL provided
    if (pmsFile && !ghlFile) {
      allFlags.push({
        id: flagId('missing-ghl', clientName),
        type: 'missing-ghl',
        clientName,
        message: `${clientName}: No GHL data file — lead matching unavailable`,
        details:
          'Upload a GHL export for this client to enable Instagram and Facebook lead analysis.',
      });
    }

    // Parse GHL
    let ghlRows: import('@/types').GHLRow[] = [];
    if (ghlFile) {
      try {
        ghlRows = await parseGHLLeads(ghlFile);
      } catch {
        allFlags.push({
          id: flagId('no-pms-data', clientName, 'ghl'),
          type: 'no-pms-data',
          clientName,
          message: `${clientName}: GHL parse error`,
          details: 'Could not parse GHL file',
        });
      }
    }

    // Filter GHL by tag and build IG email set for promo attribution (WELCOME vs VIP split)
    const igGHL = filterByTag(ghlRows, 'instagram');
    const igEmailSet = new Set<string>();
    for (const row of igGHL) {
      if (row.email) igEmailSet.add(row.email.toLowerCase().trim());
    }

    // Promo analysis — uses IG email set to split WELCOME vs VIP codes
    const { analysis: promoAnalysis, flags: promoFlags } = analyzePromoCodes(
      pmsRows,
      clientPromos,
      clientName,
      hasCouponColumn,
      igEmailSet,
    );
    promoAnalysis.netIncomeWarning = isNetIncome;
    allFlags.push(...promoFlags);

    const { analysis: igAnalysis, flags: igFlags } = analyzeLeads(
      pmsRows,
      igGHL,
      clientName,
      'instagram',
      hasEmailColumn,
    );
    allFlags.push(...igFlags);

    // Facebook leads
    const fbLeadGHL = filterByTag(ghlRows, 'facebook');
    const { analysis: fbAnalysis, flags: fbFlags } = analyzeLeads(
      pmsRows,
      fbLeadGHL,
      clientName,
      'facebook',
      hasEmailColumn,
    );
    allFlags.push(...fbFlags);

    // PMS summary — the uploaded PMS file is already direct booking data
    const paidRows = pmsRows.filter((r) => r.revenue > 0);
    const zeroRows = pmsRows.filter((r) => r.revenue === 0);
    const totalRevenue = paidRows.reduce((s, r) => s + r.revenue, 0);
    const bookingCount = paidRows.length;

    clients[clientName].pmsAnalysis = {
      clientName,
      promoCode: promoAnalysis,
      instagram: igAnalysis,
      facebook: fbAnalysis,
      summary: {
        totalRevenue,
        avgDirectBookingValue: bookingCount > 0 ? totalRevenue / bookingCount : 0,
        directBookingCount: bookingCount,
        zeroRevenueCount: zeroRows.length,
        hasSourceColumn,
      },
    };
  }

  // Deduplicate flags by id
  const seenIds = new Set<string>();
  const dedupedFlags = allFlags.filter((f) => {
    if (seenIds.has(f.id)) return false;
    seenIds.add(f.id);
    return true;
  });

  return {
    clients,
    flags: dedupedFlags,
    lastProcessed: new Date(),
  };
}

/** Auto-detect client name from filename (e.g. "Flohom PMS data.csv" → "FLOHOM") */
export function detectClientNameFromFilename(filename: string): string {
  return filename
    .replace(/\.(csv|xlsx?)$/i, '')
    .replace(/\s*(PMS data|GHL data|pms|ghl)\s*/gi, '')
    .trim();
}

/** Auto-detect file type from filename */
export type DetectedFileType = 'meta-ads' | 'promo-codes' | 'pms' | 'ghl' | 'unknown';
export function detectFileType(filename: string): DetectedFileType {
  const lower = filename.toLowerCase();
  if (lower.includes('meta ads') || lower.includes('meta_ads') || lower.includes('facebook ads')) return 'meta-ads';
  if (lower.includes('promo') || lower.includes('promo code')) return 'promo-codes';
  if (lower.includes('pms') || lower.includes('pms data')) return 'pms';
  if (lower.includes('ghl') || lower.includes('ghl data')) return 'ghl';
  return 'unknown';
}
