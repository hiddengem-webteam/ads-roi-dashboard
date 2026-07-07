import Papa from 'papaparse';
import { PromoCodeRow } from '@/types';

interface RawPromoRow {
  Client: string;
  Discount: string;
  Code: string;
  Purpose: string;
  'Campaign Type': string;
  [key: string]: string;
}

export async function parsePromoCodes(file: File): Promise<PromoCodeRow[]> {
  return new Promise((resolve, reject) => {
    Papa.parse<RawPromoRow>(file, {
      header: true,
      skipEmptyLines: false,
      transformHeader: (h) => h.trim().replace(/^﻿/, ''),
      complete: (results) => {
        const rows: PromoCodeRow[] = [];
        let currentClient = '';

        for (const raw of results.data) {
          // Forward-fill client name
          const rawClient = (raw['Client'] ?? '').trim();
          if (rawClient) currentClient = rawClient;

          const code = (raw['Code'] ?? '').trim();
          // Skip completely empty rows (no code, no discount)
          if (!code && !(raw['Discount'] ?? '').trim()) continue;
          if (!code) continue;

          rows.push({
            client: currentClient,
            discount: (raw['Discount'] ?? '').trim(),
            code: code.toUpperCase(),
            purpose: (raw['Purpose'] ?? '').trim(),
            campaignType: (raw['Campaign Type'] ?? '').trim(),
          });
        }

        resolve(rows);
      },
      error: reject,
    });
  });
}

/** Group promo codes by client name (case-insensitive key) */
export function groupPromosByClient(rows: PromoCodeRow[]): Record<string, PromoCodeRow[]> {
  const map: Record<string, PromoCodeRow[]> = {};
  for (const row of rows) {
    const key = row.client.toLowerCase();
    if (!map[key]) map[key] = [];
    map[key].push(row);
  }
  return map;
}

/** Find promo rows for a given client by fuzzy-matching client name */
export function findClientPromos(client: string, byClient: Record<string, PromoCodeRow[]>): PromoCodeRow[] {
  const needle = client.toLowerCase().trim();
  // Exact match first
  if (byClient[needle]) return byClient[needle];
  // Partial match
  for (const [key, rows] of Object.entries(byClient)) {
    if (key.includes(needle) || needle.includes(key)) return rows;
  }
  return [];
}
