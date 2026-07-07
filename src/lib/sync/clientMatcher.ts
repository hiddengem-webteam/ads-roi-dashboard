const STOP_WORDS = new Set([
  'ads', 'ad', 'account', 'retreat', 'resort', 'cabins', 'lodge',
  'escapes', 'rentals', 'stays', 'glamping',
]);

export function normalize(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter((w) => w.length > 0 && !STOP_WORDS.has(w))
    .join(' ')
    .trim();
}

function levenshtein(a: string, b: string): number {
  const m = a.length;
  const n = b.length;
  const dp: number[][] = Array.from({ length: m + 1 }, (_, i) =>
    Array.from({ length: n + 1 }, (_, j) => (i === 0 ? j : j === 0 ? i : 0)),
  );
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (a[i - 1] === b[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1];
      } else {
        dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }
  return dp[m][n];
}

/**
 * Match PMS tab names to GHL client names.
 * Returns a Map<pmsName, ghlName | null>.
 * Strategy: exact normalized → contains → Levenshtein ≤ 3
 */
export function matchClientNames(
  pmsNames: string[],
  ghlNames: string[],
): Map<string, string | null> {
  const result = new Map<string, string | null>();
  const normGhl = ghlNames.map((n) => ({ original: n, norm: normalize(n) }));

  for (const pmsName of pmsNames) {
    const normPms = normalize(pmsName);

    // 1. Exact match
    const exact = normGhl.find((g) => g.norm === normPms);
    if (exact) {
      result.set(pmsName, exact.original);
      continue;
    }

    // 2. Contains match (either direction)
    const contains = normGhl.find(
      (g) => g.norm.includes(normPms) || normPms.includes(g.norm),
    );
    if (contains) {
      result.set(pmsName, contains.original);
      continue;
    }

    // 3. Levenshtein ≤ 3
    let bestMatch: string | null = null;
    let bestDist = Infinity;
    for (const g of normGhl) {
      const dist = levenshtein(normPms, g.norm);
      if (dist <= 3 && dist < bestDist) {
        bestDist = dist;
        bestMatch = g.original;
      }
    }
    result.set(pmsName, bestMatch);
  }

  return result;
}
