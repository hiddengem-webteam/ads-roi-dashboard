import Papa from 'papaparse';
import { GHLRow } from '@/types';

interface RawGHLRow {
  'Contact Id': string;
  'First Name': string;
  'Last Name': string;
  Phone: string;
  Email: string;
  'Business Name'?: string;
  Created: string;
  'Last Activity'?: string;
  Tags: string;
  [key: string]: string | undefined;
}

export async function parseGHLLeads(file: File): Promise<GHLRow[]> {
  return new Promise((resolve, reject) => {
    Papa.parse<RawGHLRow>(file, {
      header: true,
      skipEmptyLines: true,
      transformHeader: (h) => h.trim().replace(/^﻿/, ''),
      complete: (results) => {
        const rows: GHLRow[] = results.data.map((raw) => ({
          contactId: (raw['Contact Id'] ?? '').trim(),
          firstName: (raw['First Name'] ?? '').trim(),
          lastName: (raw['Last Name'] ?? '').trim(),
          phone: (raw['Phone'] ?? '').trim(),
          email: (raw['Email'] ?? '').trim(),
          created: (raw['Created'] ?? '').trim(),
          tags: (raw['Tags'] ?? '').trim(),
        }));
        resolve(rows);
      },
      error: reject,
    });
  });
}

export function filterByTag(rows: GHLRow[], tag: 'instagram' | 'facebook'): GHLRow[] {
  const patterns =
    tag === 'instagram'
      ? ['instagram lead', 'ig lead']
      : ['facebook lead', 'meta ads lead', 'fb lead'];

  return rows.filter((r) => {
    const tagLower = r.tags.toLowerCase();
    return patterns.some((p) => tagLower.includes(p));
  });
}

/** Build a set of normalized emails from GHL rows */
export function buildGHLEmailSet(rows: GHLRow[]): Map<string, GHLRow> {
  const map = new Map<string, GHLRow>();
  for (const row of rows) {
    if (row.email) {
      map.set(row.email.toLowerCase().trim(), row);
    }
  }
  return map;
}
