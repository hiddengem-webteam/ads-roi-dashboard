export interface ParsedGHLFilename {
  clientName: string | null;
  type: 'ig' | 'fb' | 'combined';
}

const MONTH_NAMES =
  'january|february|march|april|may|june|july|august|september|october|november|december';

/** Strip GHL-specific suffixes and detect platform type from a CSV filename. */
export function parseGHLFilename(filename: string): ParsedGHLFilename {
  // Remove extension
  let name = filename.replace(/\.csv$/i, '').trim();

  // Generic export — no clear client name
  if (/^export_/i.test(name)) {
    return { clientName: null, type: 'combined' };
  }

  // Detect platform type
  let type: 'ig' | 'fb' | 'combined' = 'combined';
  if (
    /\bIG\b/i.test(name) ||
    /\binstagram\b/i.test(name) ||
    /\bIG\s*leads?\b/i.test(name) ||
    /\bInstagram\s*leads?\b/i.test(name)
  ) {
    type = 'ig';
  } else if (
    /\bFB\b/i.test(name) ||
    /\bFacebook\b/i.test(name) ||
    /\bFb\s*leads?\b/i.test(name) ||
    /\bFacebook\s*leads?\b/i.test(name) ||
    /\bMeta\b/i.test(name)
  ) {
    type = 'fb';
  }

  // Strip platform keywords
  name = name
    .replace(/\bIG\s*leads?\b/gi, '')
    .replace(/\bInstagram\s*leads?\b/gi, '')
    .replace(/\bIG\b/gi, '')
    .replace(/\bFb\s*leads?\b/gi, '')
    .replace(/\bFacebook\s*leads?\b/gi, '')
    .replace(/\bFB\b/gi, '')
    .replace(/\bMeta\b/gi, '')
    .trim();

  // Strip month/year suffixes  (e.g. "April 2026", "Apr 2026", "April", "2026")
  name = name
    .replace(new RegExp(`\\b(${MONTH_NAMES})\\b`, 'gi'), '')
    .replace(/\b20\d{2}\b/g, '')
    .trim();

  // Strip trailing/leading separators, dashes, underscores
  name = name.replace(/^[\s_\-–]+|[\s_\-–]+$/g, '').trim();

  // If nothing meaningful remains, treat as generic
  if (!name || name.length < 2) {
    return { clientName: null, type };
  }

  return { clientName: name, type };
}

/** Merge multiple CSV strings into one, de-duplicating headers. */
export function mergeCSVFiles(csvContents: string[]): string {
  const lines: string[] = [];
  let headerWritten = false;

  for (const csv of csvContents) {
    const rows = csv.split('\n');
    if (rows.length === 0) continue;

    const header = rows[0];
    if (!headerWritten) {
      lines.push(header);
      headerWritten = true;
    }

    // Skip header row of subsequent files
    for (let i = 1; i < rows.length; i++) {
      const row = rows[i].trim();
      if (row) lines.push(rows[i]);
    }
  }

  return lines.join('\n');
}
