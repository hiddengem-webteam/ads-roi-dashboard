import { PMSRow, GHLRow, LeadAnalysis, LeadMatchEntry, Flag } from '@/types';
import { normalizeEmail, normalizeName, flagId } from '@/lib/utils';
import { isPlatformEmail } from '@/lib/accountMapping';

function buildGHLNameMap(rows: GHLRow[]): Map<string, GHLRow> {
  const map = new Map<string, GHLRow>();
  for (const row of rows) {
    const full = normalizeName(`${row.firstName} ${row.lastName}`).trim();
    if (full) map.set(full, row);
    // Also index by first name only for loose matching
    const first = normalizeName(row.firstName);
    if (first && !map.has(first)) map.set(first, row);
  }
  return map;
}

export function analyzeLeads(
  pmsRows: PMSRow[],
  ghlRows: GHLRow[],
  clientName: string,
  leadType: 'instagram' | 'facebook',
  hasEmailColumn: boolean,
): { analysis: LeadAnalysis; flags: Flag[] } {
  const flags: Flag[] = [];
  const matches: LeadMatchEntry[] = [];

  // Build lookup maps
  const emailMap = new Map<string, GHLRow>();
  for (const row of ghlRows) {
    if (row.email) emailMap.set(normalizeEmail(row.email), row);
  }

  const nameMap = hasEmailColumn ? null : buildGHLNameMap(ghlRows);

  let totalRevenue = 0;
  const matchedPMSEmails = new Set<string>();

  for (const pmsRow of pmsRows) {
    const pmsEmail = normalizeEmail(pmsRow.email);

    // Skip platform relay emails
    if (pmsEmail && isPlatformEmail(pmsEmail)) continue;

    let ghlRow: GHLRow | null = null;
    let nameOnlyMatch = false;

    if (pmsEmail) {
      ghlRow = emailMap.get(pmsEmail) ?? null;
    }

    if (!ghlRow && !hasEmailColumn && nameMap) {
      // Fallback: loose first-name match
      const guestNormalized = normalizeName(pmsRow.guest);
      ghlRow = nameMap.get(guestNormalized) ?? null;
      if (ghlRow) nameOnlyMatch = true;
    }

    if (!ghlRow) continue;

    // Deduplicate by PMS email
    const dedupeKey = pmsEmail || pmsRow.guest.toLowerCase();
    if (matchedPMSEmails.has(dedupeKey)) continue;
    matchedPMSEmails.add(dedupeKey);

    totalRevenue += pmsRow.revenue;

    const entry: LeadMatchEntry = {
      guestName: pmsRow.guest,
      pmsEmail: pmsRow.email,
      ghlFirstName: ghlRow.firstName,
      ghlLastName: ghlRow.lastName,
      ghlEmail: ghlRow.email,
      revenue: pmsRow.revenue,
      nameOnlyMatch,
    };

    matches.push(entry);

    if (nameOnlyMatch) {
      flags.push({
        id: flagId('name-only-match', clientName, pmsRow.guest),
        type: 'name-only-match',
        clientName,
        message: `Name-only ${leadType} match — verify manually`,
        details: `PMS guest: ${pmsRow.guest} | GHL: ${ghlRow.firstName} ${ghlRow.lastName} <${ghlRow.email}>`,
      });
    }
  }

  return {
    analysis: {
      matchCount: matches.length,
      totalRevenue,
      matches,
      hasNoEmail: !hasEmailColumn,
      totalGHLLeads: ghlRows.length,
    },
    flags,
  };
}

/** Produce tab-separated lead match list for sheet paste */
export function leadListToTabText(analysis: LeadAnalysis, label: string): string {
  const header = `Guest Name\tEmail\tAmount Paid`;
  const lines = analysis.matches.map(
    (m) => `${m.guestName}\t${m.pmsEmail || m.ghlEmail}\t${m.revenue.toFixed(2)}`,
  );
  return [label, header, ...lines].join('\n');
}
