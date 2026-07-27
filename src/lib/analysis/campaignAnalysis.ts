import { FacebookAdsRow, CampaignType, CampaignStats, ClientFacebookStats } from '@/types';
import { resolveClientName, isExcludedAccount } from '@/lib/accountMapping';

// Client-run "launch boom" campaigns are excluded from agency ROI (per Shawal,
// Jul 2026): the "LB " / "LB-" prefix marks Launch Boom, and the word "launch"
// catches client launch campaigns (Launch Blitz, Launch Special, etc.).
// Matched on a word boundary so "relaunch"/"launchpad" aren't swept up.
function isExcludedCampaign(lower: string): boolean {
  return lower.startsWith('lb ') || lower.startsWith('lb-') || /\blaunch\b/.test(lower);
}

// Bucket a Meta campaign by name, or null to leave it out of ROI.
// Keyword rules confirmed with Shawal (Jul 2026): the agency names campaigns by
// objective/funnel stage, so we key off those words.
//
// Precedence matters when a name matches multiple buckets: purchase-intent
// (Retargeting) and lead-gen (New Leads) win over the broad awareness keywords
// (Followers), so e.g. "BOF Video Retargeting" is Retargeting, not Followers.
export function classifyCampaign(campaignName: string): CampaignType | null {
  const lower = campaignName.toLowerCase();

  if (isExcludedCampaign(lower)) return null;

  // Retargeting — warm audience / purchase-conversion
  if (
    lower.includes('retarget') || /\brt\b/.test(lower) ||
    lower.includes('purchase') || lower.includes('sales') ||
    /\bmof\b/.test(lower) || /\bbof\b/.test(lower)
  ) return 'Retargeting';

  // New Leads — cold prospecting / lead-gen
  if (lower.includes('leads') || lower.includes('new lead')) return 'New Leads';

  // Followers — awareness / engagement / follower growth (lowest precedence)
  if (
    lower.includes('discovery') || lower.includes('follower') || lower.includes('giveaway') ||
    lower.includes('video') || lower.includes('awareness') || lower.includes('engagement') ||
    lower.includes('boosted') || lower.includes('instagram post') ||
    lower.includes('pre-booking') || lower.includes('pre booking') || /\btof\b/.test(lower)
  ) return 'Followers';

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
    if (isExcludedAccount(clientName)) continue; // account removed from reporting
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
