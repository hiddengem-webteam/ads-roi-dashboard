import { FacebookAdsRow, CampaignType, CampaignStats, ClientFacebookStats } from '@/types';
import { resolveClientName } from '@/lib/accountMapping';

export function classifyCampaign(campaignName: string): CampaignType | null {
  const lower = campaignName.toLowerCase();
  if (lower.includes('discovery') || lower.includes('follower') || lower.includes('giveaway')) return 'Followers';
  if (lower.includes('retarget') || lower.includes('retargeting') || /\brt\b/.test(lower)) return 'Retargeting';
  if (lower.includes('leads') || lower.includes('new lead')) return 'New Leads';
  return null;
}

function emptyCampaignStats(type: CampaignType): CampaignStats {
  return { type, spend: 0, impressions: 0, linkClicks: 0, leads: 0, purchases: 0, purchasesConversionValue: 0 };
}

function addRow(stats: CampaignStats, row: FacebookAdsRow): void {
  stats.spend += row.amountSpent;
  stats.impressions += row.impressions;
  stats.linkClicks += row.linkClicks;
  stats.leads += row.leads;
  stats.purchases += row.purchases;
  stats.purchasesConversionValue += row.purchasesConversionValue;
}

export function aggregateFacebookStats(rows: FacebookAdsRow[]): Record<string, ClientFacebookStats> {
  const byClient: Record<string, ClientFacebookStats> = {};

  for (const row of rows) {
    const clientName = resolveClientName(row.accountName);
    const campaignType = classifyCampaign(row.campaignName);
    if (!campaignType) continue;

    if (!byClient[clientName]) {
      byClient[clientName] = {
        clientName,
        accountName: row.accountName,
        followers: undefined,
        retargeting: undefined,
        newLeads: undefined,
      };
    }

    const client = byClient[clientName];

    if (campaignType === 'Followers') {
      if (!client.followers) client.followers = emptyCampaignStats('Followers');
      addRow(client.followers, row);
    } else if (campaignType === 'Retargeting') {
      if (!client.retargeting) client.retargeting = emptyCampaignStats('Retargeting');
      addRow(client.retargeting, row);
    } else if (campaignType === 'New Leads') {
      if (!client.newLeads) client.newLeads = emptyCampaignStats('New Leads');
      addRow(client.newLeads, row);
    }
  }

  return byClient;
}

/** Produce tab-separated row for pasting into Google Sheets */
export function statsToTabRow(stats: CampaignStats): string {
  return [
    stats.type,
    stats.spend.toFixed(2),
    stats.impressions,
    stats.linkClicks,
    stats.leads,
    stats.purchases,
    stats.purchasesConversionValue.toFixed(2),
  ].join('\t');
}
