import type { ClientData } from '@/types';
import type { FinalizedPeriod } from '@/lib/analysis/finalizedPeriods';
import { computeCampaignRevenue } from '@/lib/analysis/campaignRevenue';

/**
 * One client's headline figures for one month, computed the same way the
 * finalized client view's summary cards compute them
 * (FinalizedReportingSummarySection): sheet revenue when the month is signed
 * off and the sheet cell is filled, otherwise the snapshot's PMS total; a
 * campaign bucket only contributes when it ran (had spend); attributed revenue
 * and bookings are capped at the displayed totals. Keep the two in step.
 */
export interface ClientMonthMetrics {
  periodId: string;
  label: string;
  spend: number;
  /** Direct booking revenue shown for the month (sheet or snapshot). */
  directRevenue: number;
  revenueSource: 'sheet' | 'snapshot' | null;
  bookings: number;
  attributedRevenue: number;
  attributedRevenueRaw: number;
  attributedBookings: number;
  costPerAttributedBooking: number | null;
  /** spend ÷ attributed revenue, as a percentage */
  pctOfBookingValue: number | null;
  roas: number | null;
  /** New leads from the client reporting sheet; null when the month has no sheet figures. */
  leads: number | null;
}

export function computeClientMonthMetrics(client: ClientData | null | undefined, period: FinalizedPeriod): ClientMonthMetrics | null {
  if (!client || (!client.facebookStats && !client.pmsAnalysis)) return null;
  const fb = client.facebookStats;
  const pms = client.pmsAnalysis?.summary ?? null;
  const campaignRevenue = computeCampaignRevenue(client);
  const sheetFigures = period.sheet?.[client.name];

  const spend = (fb?.followers?.spend ?? 0) + (fb?.retargeting?.spend ?? 0) + (fb?.newLeads?.spend ?? 0);

  const snapshotRevenue = pms?.totalRevenue ?? 0;
  const hasSnapshotRevenue = !!pms && snapshotRevenue > 0;
  const sheetRevenue = sheetFigures && sheetFigures.directBookingRevenue > 0 ? sheetFigures.directBookingRevenue : null;
  const directRevenue = sheetRevenue ?? snapshotRevenue;
  const revenueSource: ClientMonthMetrics['revenueSource'] = sheetRevenue !== null ? 'sheet' : hasSnapshotRevenue ? 'snapshot' : null;
  const capRevenue = revenueSource ? directRevenue : 0;

  const followersRan = (fb?.followers?.spend ?? 0) > 0;
  const retargetingRan = (fb?.retargeting?.spend ?? 0) > 0;
  const newLeadsRan = (fb?.newLeads?.spend ?? 0) > 0;
  const attributedRevenueRaw =
    (followersRan ? campaignRevenue.followers : 0) +
    (retargetingRan ? campaignRevenue.retargeting : 0) +
    (newLeadsRan ? campaignRevenue.newLeads : 0);
  const attributedRevenue = capRevenue > 0 ? Math.min(attributedRevenueRaw, capRevenue) : attributedRevenueRaw;

  const bookings = pms?.directBookingCount ?? 0;
  const attributedBookingsRaw =
    (followersRan ? campaignRevenue.followersUses : 0) +
    (retargetingRan ? fb?.retargeting?.purchases ?? 0 : 0) +
    (newLeadsRan ? client.pmsAnalysis?.facebook.matchCount ?? 0 : 0);
  const attributedBookings = bookings > 0 ? Math.min(attributedBookingsRaw, bookings) : attributedBookingsRaw;

  return {
    periodId: period.id,
    label: period.label,
    spend,
    directRevenue,
    revenueSource,
    bookings,
    attributedRevenue,
    attributedRevenueRaw,
    attributedBookings,
    costPerAttributedBooking: spend > 0 && attributedBookings > 0 ? spend / attributedBookings : null,
    pctOfBookingValue: spend > 0 && attributedRevenue > 0 ? (spend / attributedRevenue) * 100 : null,
    roas: spend > 0 && attributedRevenue > 0 ? attributedRevenue / spend : null,
    leads: sheetFigures ? sheetFigures.newLeads : null,
  };
}
