import { ClientData } from '@/types';

export interface CampaignRevenue {
  followers: number;
  followersUses: number;
  followersDeduped: number;
  retargeting: number;
  retargetingUsesConversionValue: boolean;
  newLeads: number;
}

/** Revenue (and attributed booking counts) per Meta campaign type, for one client. */
export function computeCampaignRevenue(client: ClientData | null | undefined): CampaignRevenue {
  const codes = client?.pmsAnalysis?.promoCode.codes ?? [];

  // Build set of PMS emails already attributed to New Leads (FB lead matches).
  // When both campaigns are running, a guest matched in FB leads takes priority
  // over any promo code they also used — so we exclude them from Followers.
  const fbLeadEmailSet = new Set<string>();
  for (const match of (client?.pmsAnalysis?.facebook.matches ?? [])) {
    if (match.pmsEmail) fbLeadEmailSet.add(match.pmsEmail.toLowerCase().trim());
  }

  let followers = 0;
  let followersUses = 0;
  let followersDeduped = 0; // guests moved to New Leads
  for (const code of codes) {
    const ct = code.campaignType.toLowerCase();
    if (ct.includes('follower')) {
      for (const guest of code.guests) {
        if (guest.isZeroRevenue) continue;
        const email = guest.email?.toLowerCase().trim();
        if (email && fbLeadEmailSet.has(email)) {
          followersDeduped++;
          continue; // already attributed to New Leads
        }
        followers += guest.revenue;
        followersUses++;
      }
    }
  }

  // Retargeting: Meta's own purchase conversion value when it's reporting one
  // (Flohom and other clients with Meta pixel purchase tracking wired up);
  // otherwise fall back to FB purchase events × avg direct booking value.
  const avgBookingValue = client?.pmsAnalysis?.summary.avgDirectBookingValue ?? 0;
  const retargetingPurchases = client?.facebookStats?.retargeting?.purchases ?? 0;
  const retargetingConversionValue = client?.facebookStats?.retargeting?.purchasesConversionValue ?? 0;
  const retargetingUsesConversionValue = retargetingConversionValue > 0;
  const retargeting = retargetingUsesConversionValue
    ? retargetingConversionValue
    : retargetingPurchases * avgBookingValue;

  // New Leads: revenue from matched Facebook leads in PMS
  const newLeads = client?.pmsAnalysis?.facebook.totalRevenue ?? 0;

  return { followers, followersUses, followersDeduped, retargeting, retargetingUsesConversionValue, newLeads };
}
