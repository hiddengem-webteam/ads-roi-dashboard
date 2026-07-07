import Papa from 'papaparse';
import { FacebookAdsRow } from '@/types';
import { parseNumber } from '@/lib/utils';

interface RawFBAdsRow {
  'Account name': string;
  'Campaign name': string;
  'Amount spent': string;
  'Link clicks': string;
  Leads: string;
  Impressions: string;
  Purchases: string;
  'Purchases conversion value': string;
  [key: string]: string;
}

export async function parseFacebookAds(file: File): Promise<FacebookAdsRow[]> {
  return new Promise((resolve, reject) => {
    Papa.parse<RawFBAdsRow>(file, {
      header: true,
      skipEmptyLines: true,
      transformHeader: (h) => h.trim().replace(/^﻿/, ''),
      complete: (results) => {
        const rows: FacebookAdsRow[] = [];
        for (const raw of results.data) {
          const accountName = (raw['Account name'] ?? '').trim();
          const campaignName = (raw['Campaign name'] ?? '').trim();
          // Skip totals row (empty account name)
          if (!accountName) continue;
          rows.push({
            accountName,
            campaignName,
            amountSpent: parseNumber(raw['Amount spent']),
            linkClicks: parseNumber(raw['Link clicks']),
            leads: parseNumber(raw['Leads']),
            impressions: parseNumber(raw['Impressions']),
            purchases: parseNumber(raw['Purchases']),
            purchasesConversionValue: parseNumber(raw['Purchases conversion value']),
          });
        }
        resolve(rows);
      },
      error: reject,
    });
  });
}
