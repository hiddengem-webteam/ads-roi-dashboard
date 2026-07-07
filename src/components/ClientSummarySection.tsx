'use client';

import { ClientFacebookStats, PMSSummary } from '@/types';
import { formatCurrency } from '@/lib/utils';

interface CampaignRevenue {
  followers: number;
  retargeting: number;
  newLeads: number;
}

interface ClientSummarySectionProps {
  facebookStats: ClientFacebookStats | null;
  pmsSummary: PMSSummary | null;
  campaignRevenue: CampaignRevenue;
}

function SummaryCard({
  label,
  value,
  sub,
  placeholder,
}: {
  label: string;
  value?: string;
  sub?: string;
  placeholder?: string;
}) {
  return (
    <div className="flex-1 bg-white rounded-2xl border border-gray-100 shadow-[0_1px_4px_rgba(0,0,0,0.06)] px-6 py-5">
      <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">{label}</p>
      {value ? (
        <>
          <p className="text-3xl font-bold text-gray-900 tracking-tight">{value}</p>
          {sub && <p className="text-xs text-gray-400 mt-1">{sub}</p>}
        </>
      ) : (
        <p className="text-2xl font-bold text-gray-300">{placeholder ?? '—'}</p>
      )}
    </div>
  );
}

export default function ClientSummarySection({ facebookStats, pmsSummary, campaignRevenue }: ClientSummarySectionProps) {
  const totalSpend =
    (facebookStats?.followers?.spend ?? 0) +
    (facebookStats?.retargeting?.spend ?? 0) +
    (facebookStats?.newLeads?.spend ?? 0);

  const totalRevenue = campaignRevenue.followers + campaignRevenue.retargeting + campaignRevenue.newLeads;
  const blendedRoas = totalSpend > 0 && totalRevenue > 0 ? totalRevenue / totalSpend : null;

  const hasSpend = totalSpend > 0;
  const hasAvg = pmsSummary && pmsSummary.avgDirectBookingValue > 0;

  return (
    <div className="flex gap-4">
      <SummaryCard
        label="Overall Spend"
        value={hasSpend ? formatCurrency(totalSpend) : undefined}
        sub={hasSpend ? 'All campaign types combined' : undefined}
        placeholder="No ad data"
      />
      <SummaryCard
        label="Avg Direct Booking Value"
        value={hasAvg ? formatCurrency(pmsSummary.avgDirectBookingValue) : undefined}
        sub={
          hasAvg
            ? pmsSummary.zeroRevenueCount > 0
              ? `Based on ${pmsSummary.directBookingCount} bookings · ${pmsSummary.zeroRevenueCount} $0 entr${pmsSummary.zeroRevenueCount === 1 ? 'y' : 'ies'} excluded`
              : `Based on ${pmsSummary.directBookingCount} bookings`
            : undefined
        }
        placeholder="No PMS data"
      />
      <SummaryCard
        label="Blended ROAS"
        value={blendedRoas !== null ? `${blendedRoas.toFixed(2)}x` : undefined}
        sub={blendedRoas !== null ? `${formatCurrency(totalRevenue)} revenue ÷ ${formatCurrency(totalSpend)} spend` : undefined}
        placeholder="No data"
      />
    </div>
  );
}
