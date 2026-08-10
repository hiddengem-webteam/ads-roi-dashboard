// Exports every value displayed on /july (summary cards, per-campaign Facebook
// stats, PMS/promo/lead analysis) as a clean, flat JSON per client — for other
// tools/dashboards to consume. Raw numbers, not formatted display strings.
//
// Usage: npx tsx scripts/export-july-full.mts

import fs from 'fs';
import path from 'path';
import { ProcessedData, ClientData, CampaignStats, CampaignType } from '../src/types';
import { computeCampaignRevenue, CampaignRevenue } from '../src/lib/analysis/campaignRevenue';

const ROOT = path.resolve(import.meta.dirname, '..');

function round2(n: number): number {
  return Math.round(n * 100) / 100;
}

interface FacebookCampaignExport {
  spend: number;
  impressions: number;
  linkClicks: number;
  leads: number | null; // New Leads only
  costPerLead: number | null; // New Leads only
  instagramTagLeads: number | null; // Followers only — total GHL leads tagged Instagram
  totalBookingsAttributed: number;
  costPerBooking: number | null;
  campaignAvgBookingValue: number | null;
  pctOfBookingValue: number | null;
  bookingRevenue: number;
  roas: number | null;
  followersDeduped: number | null; // Followers only
  retargetingUsesMetaConversionValue: boolean | null; // Retargeting only
}

function buildCampaignExport(
  type: CampaignType,
  s: CampaignStats,
  bookingRevenue: number,
  campaignRevenue: CampaignRevenue,
  instagramTotalGHLLeads: number,
  facebookMatchCount: number,
): FacebookCampaignExport {
  const attributedBookings =
    type === 'Followers' ? campaignRevenue.followersUses
    : type === 'Retargeting' ? s.purchases
    : facebookMatchCount;

  const costPerBooking = attributedBookings > 0 && s.spend > 0 ? s.spend / attributedBookings : null;
  const campaignAvgBookingValue = attributedBookings > 0 && bookingRevenue > 0 ? bookingRevenue / attributedBookings : null;
  const pctOfBookingValue = costPerBooking !== null && campaignAvgBookingValue !== null
    ? round2((costPerBooking / campaignAvgBookingValue) * 100)
    : null;
  const roas = s.spend > 0 && bookingRevenue > 0 ? round2(bookingRevenue / s.spend) : null;

  return {
    spend: round2(s.spend),
    impressions: s.impressions,
    linkClicks: s.linkClicks,
    leads: type === 'New Leads' ? s.leads : null,
    costPerLead: type === 'New Leads' && s.leads > 0 ? round2(s.spend / s.leads) : null,
    instagramTagLeads: type === 'Followers' ? instagramTotalGHLLeads : null,
    totalBookingsAttributed: attributedBookings,
    costPerBooking: costPerBooking !== null ? round2(costPerBooking) : null,
    campaignAvgBookingValue: campaignAvgBookingValue !== null ? round2(campaignAvgBookingValue) : null,
    pctOfBookingValue,
    bookingRevenue: round2(bookingRevenue),
    roas,
    followersDeduped: type === 'Followers' ? campaignRevenue.followersDeduped : null,
    retargetingUsesMetaConversionValue: type === 'Retargeting' ? campaignRevenue.retargetingUsesConversionValue : null,
  };
}

function buildClientExport(client: ClientData) {
  const fb = client.facebookStats;
  const pms = client.pmsAnalysis;
  const campaignRevenue = computeCampaignRevenue(client);

  const totalSpend =
    (fb?.followers?.spend ?? 0) + (fb?.retargeting?.spend ?? 0) + (fb?.newLeads?.spend ?? 0);

  const directBookingRevenue = pms?.summary.totalRevenue ?? 0;
  const bookingCount = pms?.summary.directBookingCount ?? 0;
  const avgDirectBookingValue = pms?.summary.avgDirectBookingValue ?? 0;

  const metaAttributedRevenue = campaignRevenue.followers + campaignRevenue.retargeting + campaignRevenue.newLeads;
  const metaAttributedBookings =
    campaignRevenue.followersUses + (fb?.retargeting?.purchases ?? 0) + (pms?.facebook.matchCount ?? 0);
  const costPerMetaBooking = totalSpend > 0 && metaAttributedBookings > 0 ? totalSpend / metaAttributedBookings : null;
  const pctOfBookingValue = costPerMetaBooking !== null && avgDirectBookingValue > 0
    ? round2((costPerMetaBooking / avgDirectBookingValue) * 100)
    : null;
  const roas = totalSpend > 0 && metaAttributedRevenue > 0 ? round2(metaAttributedRevenue / totalSpend) : null;

  const instagramTotalGHLLeads = pms?.instagram.totalGHLLeads ?? 0;
  const facebookTotalGHLLeads = pms?.facebook.totalGHLLeads ?? 0;

  const buckets = [fb?.followers, fb?.retargeting, fb?.newLeads];
  const metaAdsLeadsTotal = buckets.reduce((s, b) => s + (b?.leads ?? 0), 0);
  const metaAdsAttributedBookingsTotal = buckets.reduce((s, b) => s + (b?.purchases ?? 0), 0);
  const metaAdsAttributedRevenueTotal = buckets.reduce((s, b) => s + (b?.purchasesConversionValue ?? 0), 0);

  const facebookCampaigns: Record<string, FacebookCampaignExport | null> = {
    followers: fb?.followers
      ? buildCampaignExport('Followers', fb.followers, campaignRevenue.followers, campaignRevenue, instagramTotalGHLLeads, pms?.facebook.matchCount ?? 0)
      : null,
    retargeting: fb?.retargeting
      ? buildCampaignExport('Retargeting', fb.retargeting, campaignRevenue.retargeting, campaignRevenue, instagramTotalGHLLeads, pms?.facebook.matchCount ?? 0)
      : null,
    newLeads: fb?.newLeads
      ? buildCampaignExport('New Leads', fb.newLeads, campaignRevenue.newLeads, campaignRevenue, instagramTotalGHLLeads, pms?.facebook.matchCount ?? 0)
      : null,
  };

  return {
    clientName: client.name,
    hasFacebookAdsData: !!fb,
    hasPMSData: !!pms,
    hasGHLData: client.hasGHL,

    summary: {
      totalDirectBookings: bookingCount,
      totalDirectBookingRevenue: round2(directBookingRevenue),
      avgDirectBookingValue: round2(avgDirectBookingValue),
      zeroRevenueBookingCount: pms?.summary.zeroRevenueCount ?? 0,
      overallMetaAdSpend: round2(totalSpend),
      totalBookingsAttributedToMeta: metaAttributedBookings,
      costPerMetaAttributedBooking: costPerMetaBooking !== null ? round2(costPerMetaBooking) : null,
      pctOfBookingValue,
      directBookingRevenueAttributedToMeta: round2(metaAttributedRevenue),
      roas,
      metaLeadsFromGHL: facebookTotalGHLLeads,
      instagramLeadsFromGHL: instagramTotalGHLLeads,
    },

    facebookCampaigns,

    pmsAnalysis: pms ? {
      promoCode: {
        totalUses: pms.promoCode.codes.reduce((s, c) => s + c.uses, 0),
        totalRevenue: round2(pms.promoCode.codes.reduce((s, c) => s + c.revenue, 0)),
        codesActiveCount: pms.promoCode.codes.filter((c) => c.uses > 0).length,
        codesTotalCount: pms.promoCode.codes.length,
        codes: pms.promoCode.codes.map((c) => ({
          code: c.code,
          discount: c.discount,
          purpose: c.purpose,
          campaignType: c.campaignType,
          uses: c.uses,
          revenue: round2(c.revenue),
          unrecognized: c.unrecognized ?? false,
          guests: c.guests.map((g) => ({
            name: g.name,
            email: g.email,
            revenue: round2(g.revenue),
            confidence: g.confidence,
            confidenceReason: g.confidenceReason,
            isZeroRevenue: g.isZeroRevenue ?? false,
          })),
        })),
        unrecognizedCodes: pms.promoCode.unrecognizedCodes,
        missingFromPromoSheet: pms.promoCode.missingFromPromoSheet,
        netIncomeWarning: pms.promoCode.netIncomeWarning,
      },
      instagramLeadAnalysis: {
        emailMatches: pms.instagram.matchCount,
        totalGHLLeadsTagged: pms.instagram.totalGHLLeads,
        totalRevenue: round2(pms.instagram.totalRevenue),
        hasNoEmailColumn: pms.instagram.hasNoEmail,
        matches: pms.instagram.matches.map((m) => ({
          guestName: m.guestName,
          pmsEmail: m.pmsEmail,
          ghlFirstName: m.ghlFirstName,
          ghlLastName: m.ghlLastName,
          ghlEmail: m.ghlEmail,
          revenue: round2(m.revenue),
          nameOnlyMatch: m.nameOnlyMatch,
        })),
      },
      facebookMetaLeadAnalysis: {
        metaAdsManagerLeads: metaAdsLeadsTotal,
        metaAdsManagerAttributedBookings: metaAdsAttributedBookingsTotal,
        metaAdsManagerAttributedRevenue: round2(metaAdsAttributedRevenueTotal),
        hasMetaAdAccount: !!fb,
        verifiedEmailMatches: pms.facebook.matchCount,
        totalGHLLeadsTagged: pms.facebook.totalGHLLeads,
        verifiedMatchRevenue: round2(pms.facebook.totalRevenue),
        hasNoEmailColumn: pms.facebook.hasNoEmail,
        matches: pms.facebook.matches.map((m) => ({
          guestName: m.guestName,
          pmsEmail: m.pmsEmail,
          ghlFirstName: m.ghlFirstName,
          ghlLastName: m.ghlLastName,
          ghlEmail: m.ghlEmail,
          revenue: round2(m.revenue),
          nameOnlyMatch: m.nameOnlyMatch,
        })),
      },
    } : null,
  };
}

async function main() {
  const snapshotPath = path.join(ROOT, 'public', 'data', 'snapshots', 'july-2026.json');
  const snapshot: { period: { id: string; label: string }; data: ProcessedData } = JSON.parse(
    fs.readFileSync(snapshotPath, 'utf8'),
  );

  const clients = Object.values(snapshot.data.clients).sort((a, b) => a.name.localeCompare(b.name));
  const exportData = {
    period: snapshot.period.label,
    periodId: snapshot.period.id,
    generatedFrom: 'public/data/snapshots/july-2026.json',
    totalClients: clients.length,
    clients: clients.map(buildClientExport),
  };

  const outPath = path.join(ROOT, 'public', 'data', 'snapshots', 'july-2026-full-export.json');
  fs.writeFileSync(outPath, JSON.stringify(exportData, null, 2), 'utf8');
  console.log(`Wrote ${outPath} — ${clients.length} clients`);
}

main().catch((err) => {
  console.error('Export failed:', err);
  process.exit(1);
});
