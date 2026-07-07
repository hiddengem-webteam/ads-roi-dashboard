import {
  PMSRow,
  PromoCodeRow,
  PromoCodeAnalysis,
  PromoCodeResult,
  PromoGuestEntry,
  Flag,
  ConfidenceLevel,
} from '@/types';
import { normalizeEmail, flagId } from '@/lib/utils';

// ─── Code classification ──────────────────────────────────────────────────────

/** Parse discount field into flat dollar or percentage */
function parseCodeDiscount(discountStr: string): { type: 'flat' | 'percent'; value: number } | null {
  if (!discountStr) return null;
  const clean = discountStr.replace(/\s/g, '').toLowerCase();
  if (clean.includes('%')) {
    const val = parseFloat(clean.replace(/[^0-9.]/g, ''));
    return isNaN(val) ? null : { type: 'percent', value: val };
  }
  const val = parseFloat(clean.replace(/[^0-9.]/g, ''));
  return isNaN(val) ? null : { type: 'flat', value: val };
}

/** Returns true if a promo row's discount matches the observed discount amount */
function matchesDiscountAmount(promo: PromoCodeRow, absDiscount: number, revenue: number): boolean {
  const parsed = parseCodeDiscount(promo.discount);
  if (!parsed) return false;
  if (parsed.type === 'flat') {
    return Math.abs(parsed.value - absDiscount) < 1;
  }
  // Percentage: expected discount ≈ (pct/100) * revenue, within $2
  if (revenue > 0) {
    const expected = (parsed.value / 100) * revenue;
    return Math.abs(expected - absDiscount) < 2;
  }
  return false;
}

/** Classify a promo code as welcome-type (Followers) or vip-type (Retargeting) */
function isWelcomeType(promo: PromoCodeRow): boolean {
  const ct = promo.campaignType.toLowerCase();
  if (ct.includes('follower')) return true;
  // Name pattern fallback
  return promo.code.toUpperCase().startsWith('WELCOME');
}

function isVIPType(promo: PromoCodeRow): boolean {
  const ct = promo.campaignType.toLowerCase();
  if (ct.includes('retarget')) return true;
  const code = promo.code.toUpperCase();
  return code.startsWith('VIP') || (!code.startsWith('WELCOME'));
}

/** Known platform / relay email patterns to exclude from promo counts */
const PLATFORM_EMAIL_PATTERNS = [
  'hipcamp.com',
  'relay.firefox.com',
  'noreply.',
  'support@',
  'admin@',
  'operations@',
];

function isPlatformEmail(email: string): boolean {
  if (!email) return false;
  const lower = email.toLowerCase();
  return PLATFORM_EMAIL_PATTERNS.some((p) => lower.includes(p));
}

/** Apple relay emails: count in totals but cannot GHL-match */
function isAppleRelayEmail(email: string): boolean {
  return email.toLowerCase().includes('privaterelay.appleid.com');
}

// ─── Attribution decision tree ────────────────────────────────────────────────

interface Attribution {
  code: string;
  confidence: ConfidenceLevel;
  reason: string;
}

function attributeCode(
  pmsRow: PMSRow,
  clientPromos: PromoCodeRow[],
  igEmailSet: Set<string>,
  hasCouponColumn: boolean,
): Attribution | null {
  // ── Branch 1: Explicit coupon column ──────────────────────────────────────
  if (hasCouponColumn) {
    const code = pmsRow.couponName?.trim().toUpperCase();
    if (!code) return null;

    const known = clientPromos.find((p) => p.code === code);
    return {
      code,
      confidence: 'high',
      reason: known ? 'Explicit code in PMS' : 'Explicit code in PMS (not in promo sheet)',
    };
  }

  // ── Branch 2: Discount amount only ────────────────────────────────────────
  const absDiscount = Math.abs(pmsRow.couponDiscount);
  if (!absDiscount) return null;

  const email = normalizeEmail(pmsRow.email);
  const isApple = isAppleRelayEmail(pmsRow.email);
  const isIG = !isApple && !!email && igEmailSet.has(email);

  // Find all client promo codes whose discount value matches
  const matching = clientPromos.filter((p) =>
    matchesDiscountAmount(p, absDiscount, pmsRow.revenue),
  );

  // No match in promo sheet — try inferring a VIP-pattern code from unknown codes
  if (matching.length === 0) {
    return {
      code: `UNKNOWN($${absDiscount})`,
      confidence: 'unverifiable',
      reason: `Discount $${absDiscount.toFixed(2)} not matched to any promo sheet code`,
    };
  }

  // Exactly one code matches — unambiguous amount, but still need IG to raise confidence
  if (matching.length === 1) {
    if (isApple) {
      return {
        code: matching[0].code,
        confidence: 'unverifiable',
        reason: 'Apple relay email — cannot verify via GHL',
      };
    }
    if (!email) {
      return {
        code: matching[0].code,
        confidence: 'low',
        reason: 'Discount amount match, no email to confirm',
      };
    }
    return {
      code: matching[0].code,
      confidence: isIG ? 'medium' : 'low',
      reason: isIG
        ? 'Discount amount match + IG email confirmed'
        : 'Discount amount match only',
    };
  }

  // Multiple codes match the same discount (e.g. WELCOME100 + VIP100 both = $100)
  // Use IG email to split WELCOME vs VIP
  const welcomeCodes = matching.filter(isWelcomeType);
  const vipCodes = matching.filter(isVIPType);

  if (isApple || !email) {
    // Cannot split — pick WELCOME as default but mark unverifiable
    const fallback = welcomeCodes[0] ?? vipCodes[0] ?? matching[0];
    return {
      code: fallback.code,
      confidence: 'unverifiable',
      reason: isApple
        ? 'Apple relay — cannot split WELCOME vs VIP via GHL'
        : 'No email — cannot split WELCOME vs VIP',
    };
  }

  if (isIG && welcomeCodes.length > 0) {
    return {
      code: welcomeCodes[0].code,
      confidence: 'medium',
      reason: 'IG email match → attributed to WELCOME code',
    };
  }
  if (!isIG && vipCodes.length > 0) {
    return {
      code: vipCodes[0].code,
      confidence: 'medium',
      reason: 'Non-IG email → attributed to VIP code',
    };
  }

  // Fallback: return first match
  return {
    code: matching[0].code,
    confidence: 'low',
    reason: 'Discount match, ambiguous attribution',
  };
}

// ─── Main analysis function ───────────────────────────────────────────────────

export function analyzePromoCodes(
  pmsRows: PMSRow[],
  clientPromos: PromoCodeRow[],
  clientName: string,
  hasCouponColumn: boolean,
  igEmailSet: Set<string>,
): { analysis: PromoCodeAnalysis; flags: Flag[] } {
  const flags: Flag[] = [];
  const knownCodes = new Set(clientPromos.map((p) => p.code.toUpperCase()));
  const codeMap = new Map<string, PromoCodeRow>(
    clientPromos.map((p) => [p.code.toUpperCase(), p]),
  );

  const results = new Map<string, PromoCodeResult>();
  const unrecognizedCodes = new Set<string>();

  // Pre-populate all known codes (including WELCOMEBACK10 at 0 uses)
  for (const promo of clientPromos) {
    const code = promo.code.toUpperCase();
    if (!results.has(code)) {
      results.set(code, {
        code,
        discount: promo.discount,
        purpose: promo.purpose,
        campaignType: promo.campaignType,
        uses: 0,
        revenue: 0,
        guests: [],
      });
    }
  }

  for (const row of pmsRows) {
    // Exclude platform emails entirely (not Apple relay — those are counted)
    if (row.email && isPlatformEmail(row.email) && !isAppleRelayEmail(row.email)) {
      flags.push({
        id: flagId('platform-email', clientName, row.guest),
        type: 'platform-email',
        clientName,
        message: `Platform email excluded from promo count`,
        details: `Guest: ${row.guest} | Email: ${row.email}`,
      });
      continue;
    }

    const attribution = attributeCode(row, clientPromos, igEmailSet, hasCouponColumn);
    if (!attribution) continue;

    const code = attribution.code.toUpperCase();

    // Track unrecognized codes
    if (!knownCodes.has(code) && !code.startsWith('UNKNOWN')) {
      unrecognizedCodes.add(code);
      if (!results.has(code)) {
        results.set(code, {
          code,
          discount: '',
          purpose: '',
          campaignType: '',
          uses: 0,
          revenue: 0,
          guests: [],
          unrecognized: true,
        });
      }
    }

    if (!results.has(code)) continue; // UNKNOWN($x) entries — skip accumulation

    const entry = results.get(code)!;
    entry.uses += 1;
    entry.revenue += row.revenue;

    const guestEntry: PromoGuestEntry = {
      name: row.guest,
      email: normalizeEmail(row.email),
      revenue: row.revenue,
      confidence: attribution.confidence,
      confidenceReason: attribution.reason,
      isZeroRevenue: row.revenue === 0,
    };
    entry.guests.push(guestEntry);
  }

  // Flags for unrecognized codes
  for (const code of unrecognizedCodes) {
    flags.push({
      id: flagId('unrecognized-code', clientName, code),
      type: 'unrecognized-code',
      clientName,
      message: `Unrecognized promo code in PMS: ${code}`,
      details: `Add ${code} to the promo sheet for ${clientName}`,
    });
  }

  if (clientPromos.length === 0) {
    flags.push({
      id: flagId('missing-from-promo-sheet', clientName),
      type: 'missing-from-promo-sheet',
      clientName,
      message: `${clientName} has no entries in the promo codes sheet`,
      details: 'Add this client to the promo codes sheet',
    });
  }

  const codesArray = Array.from(results.values());
  const totalUses = codesArray.reduce((s, c) => s + c.uses, 0);
  const totalRevenue = codesArray.reduce((s, c) => s + c.revenue, 0);

  return {
    analysis: {
      codes: codesArray,
      totalUses,
      totalRevenue,
      unrecognizedCodes: Array.from(unrecognizedCodes),
      missingFromPromoSheet: clientPromos.length === 0,
      netIncomeWarning: false,
    },
    flags,
  };
}

/** Produce tab-separated promo list for sheet paste */
export function promoListToTabText(codes: PromoCodeResult[]): string {
  const header = 'Guest Name\tEmail\tCode\tAmount Paid';
  const lines = codes.flatMap((c) =>
    c.guests.map((g) => `${g.name}\t${g.email}\t${c.code}\t${g.revenue.toFixed(2)}`),
  );
  return [header, ...lines].join('\n');
}
