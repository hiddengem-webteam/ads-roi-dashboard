// Exports exactly what /july-client-reporting-sheet displays per client —
// the Client Performance Tracking sheet's revenue + New Leads figures,
// combined with the snapshot-derived Meta metrics (with attribution capped
// at the sheet revenue, matching ClientReportingSummarySection).
//
// Usage: npx tsx scripts/export-july-client-reporting.mts

import fs from 'fs';
import path from 'path';
import { ProcessedData, CampaignStats } from '../src/types';
import { computeCampaignRevenue } from '../src/lib/analysis/campaignRevenue';
import { CLIENT_REPORTING_SHEET } from '../src/components/july/clientReportingSheetData';

const ROOT = path.resolve(import.meta.dirname, '..');

function round2(n: number): number {
  return Math.round(n * 100) / 100;
}

// Per-campaign-type breakdown matching the dashboard's Facebook Campaign
// Stats tabs: same attribution logic (Followers via promo codes, Retargeting
// via Meta purchase events, New Leads via lead-email matches).
function campaignBlock(
  stats: CampaignStats | null | undefined,
  attributedBookings: number,
  bookingRevenue: number,
  opts: { includeLeads?: boolean; instagramTagLeads?: number } = {},
) {
  if (!stats || (stats.spend === 0 && stats.impressions === 0)) return null;
  const costPerBooking = stats.spend > 0 && attributedBookings > 0 ? stats.spend / attributedBookings : null;
  // Avg booking value within THIS campaign's attributed bookings — the
  // denominator of the campaign tab's "% of Booking Value" card.
  const campaignAvgBookingValue = attributedBookings > 0 && bookingRevenue > 0
    ? bookingRevenue / attributedBookings
    : null;
  const pctOfBookingValue = costPerBooking !== null && campaignAvgBookingValue !== null
    ? round2((costPerBooking / campaignAvgBookingValue) * 100)
    : null;
  return {
    spend: round2(stats.spend),
    impressions: stats.impressions,
    linkClicks: stats.linkClicks,
    ...(opts.includeLeads ? {
      leads: stats.leads,
      costPerLead: stats.leads > 0 && stats.spend > 0 ? round2(stats.spend / stats.leads) : null,
    } : {}),
    ...(opts.instagramTagLeads !== undefined ? { instagramTagLeads: opts.instagramTagLeads } : {}),
    totalBookings: attributedBookings,
    costPerBooking: costPerBooking !== null ? round2(costPerBooking) : null,
    campaignAvgBookingValue: campaignAvgBookingValue !== null ? round2(campaignAvgBookingValue) : null,
    pctOfBookingValue,
    bookingRevenue: round2(bookingRevenue),
    roas: stats.spend > 0 && bookingRevenue > 0 ? round2(bookingRevenue / stats.spend) : null,
  };
}

async function main() {
  const snapshot: { period: { id: string; label: string }; data: ProcessedData } = JSON.parse(
    fs.readFileSync(path.join(ROOT, 'public', 'data', 'snapshots', 'july-2026.json'), 'utf8'),
  );

  const clients = Object.values(snapshot.data.clients).sort((a, b) => a.name.localeCompare(b.name));

  const exportClients = clients.map((client) => {
    const fig = CLIENT_REPORTING_SHEET[client.name];
    const fb = client.facebookStats;
    const pms = client.pmsAnalysis;
    const cr = computeCampaignRevenue(client);

    const totalSpend = (fb?.followers?.spend ?? 0) + (fb?.retargeting?.spend ?? 0) + (fb?.newLeads?.spend ?? 0);
    const bookingCount = pms?.summary.directBookingCount ?? 0;
    const snapshotRevenue = pms?.summary.totalRevenue ?? 0;

    const displayRevenue = fig ? fig.directBookingRevenue : snapshotRevenue;

    const metaAttributedRevenueRaw = cr.followers + cr.retargeting + cr.newLeads;
    const metaAttributedRevenue = displayRevenue > 0
      ? Math.min(metaAttributedRevenueRaw, displayRevenue)
      : metaAttributedRevenueRaw;

    const metaAttributedBookingsRaw =
      cr.followersUses + (fb?.retargeting?.purchases ?? 0) + (pms?.facebook.matchCount ?? 0);
    const metaAttributedBookings = bookingCount > 0
      ? Math.min(metaAttributedBookingsRaw, bookingCount)
      : metaAttributedBookingsRaw;

    const costPerMetaBooking = totalSpend > 0 && metaAttributedBookings > 0 ? totalSpend / metaAttributedBookings : null;
    const avgDirectBookingValue = pms?.summary.avgDirectBookingValue ?? 0;
    const pctOfBookingValue = costPerMetaBooking !== null && avgDirectBookingValue > 0
      ? round2((costPerMetaBooking / avgDirectBookingValue) * 100)
      : null;
    const roas = totalSpend > 0 && metaAttributedRevenue > 0 ? round2(metaAttributedRevenue / totalSpend) : null;

    return {
      clientName: client.name,
      revenueSource: fig ? 'client-reporting-sheet' : 'dashboard-snapshot (not listed in reporting sheet)',
      totalDirectBookings: bookingCount,
      totalDirectBookingRevenue: round2(displayRevenue),
      totalLeads: fig ? fig.newLeads : null,
      overallMetaAdSpend: round2(totalSpend),
      totalBookingsAttributedToMeta: metaAttributedBookings,
      costPerMetaAttributedBooking: costPerMetaBooking !== null ? round2(costPerMetaBooking) : null,
      avgDirectBookingValue: avgDirectBookingValue > 0 ? round2(avgDirectBookingValue) : null,
      pctOfBookingValue,
      directBookingRevenueAttributedToMeta: round2(metaAttributedRevenue),
      metaAttributedRevenueCappedAtTotal: metaAttributedRevenueRaw > metaAttributedRevenue,
      roas,
      campaigns: {
        followers: campaignBlock(fb?.followers, cr.followersUses, cr.followers, {
          instagramTagLeads: pms?.instagram.totalGHLLeads ?? 0,
        }),
        retargeting: campaignBlock(fb?.retargeting, fb?.retargeting?.purchases ?? 0, cr.retargeting),
        newLeads: campaignBlock(fb?.newLeads, pms?.facebook.matchCount ?? 0, cr.newLeads, { includeLeads: true }),
      },
    };
  });

  const out = {
    period: snapshot.period.label,
    periodId: snapshot.period.id,
    generatedFrom: '/july-client-reporting-sheet (revenue + leads from the Client Performance Tracking sheet; Meta metrics from the July snapshot)',
    totalClients: exportClients.length,
    totals: {
      totalDirectBookingRevenue: round2(exportClients.reduce((s, c) => s + c.totalDirectBookingRevenue, 0)),
      totalLeads: exportClients.reduce((s, c) => s + (c.totalLeads ?? 0), 0),
    },
    clients: exportClients,
  };

  const outPath = path.join(ROOT, 'public', 'data', 'snapshots', 'july-2026-client-reporting-export.json');
  fs.writeFileSync(outPath, JSON.stringify(out, null, 2), 'utf8');
  console.log(`Wrote ${outPath} — ${exportClients.length} clients`);
}

main().catch((err) => {
  console.error('Export failed:', err);
  process.exit(1);
});
