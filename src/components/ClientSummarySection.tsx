'use client';

import { ClientFacebookStats, PMSSummary } from '@/types';
import { formatCurrency } from '@/lib/utils';

interface ClientSummarySectionProps {
  facebookStats: ClientFacebookStats | null;
  pmsSummary: PMSSummary | null;
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

export default function ClientSummarySection({ facebookStats, pmsSummary }: ClientSummarySectionProps) {
  const totalSpend =
    (facebookStats?.followers?.spend ?? 0) +
    (facebookStats?.retargeting?.spend ?? 0) +
    (facebookStats?.newLeads?.spend ?? 0);

  // Direct booking revenue = the platform's PMS direct-booking total. OTA
  // bookings (Airbnb/VRBO/Booking.com/…) are already excluded upstream by
  // roi-export, so every booking here is a direct booking.
  const directBookingRevenue = pmsSummary?.totalRevenue ?? 0;
  const hasSpend = totalSpend > 0;
  const hasRevenue = !!pmsSummary && directBookingRevenue > 0;

  // Blended ROAS = total direct booking revenue ÷ ad spend (the platform's blended_roas).
  const blendedRoas = hasSpend && hasRevenue ? directBookingRevenue / totalSpend : null;

  let revenueSub: string | undefined;
  if (hasRevenue && pmsSummary) {
    const n = pmsSummary.directBookingCount;
    revenueSub =
      `${n} direct booking${n !== 1 ? 's' : ''} · ${formatCurrency(pmsSummary.avgDirectBookingValue)} avg` +
      (pmsSummary.zeroRevenueCount > 0 ? ` · ${pmsSummary.zeroRevenueCount} $0 excluded` : '');
  }

  return (
    <div className="flex gap-4">
      <SummaryCard
        label="Overall Spend"
        value={hasSpend ? formatCurrency(totalSpend) : undefined}
        sub={hasSpend ? 'All campaign types combined' : undefined}
        placeholder="No ad data"
      />
      <SummaryCard
        label="Direct Booking Revenue"
        value={hasRevenue ? formatCurrency(directBookingRevenue) : undefined}
        sub={revenueSub}
        placeholder="No PMS data"
      />
      <SummaryCard
        label="Blended ROAS"
        value={blendedRoas !== null ? `${blendedRoas.toFixed(2)}x` : undefined}
        sub={blendedRoas !== null ? `${formatCurrency(directBookingRevenue)} direct booking revenue ÷ ${formatCurrency(totalSpend)} spend` : undefined}
        placeholder="No data"
      />
    </div>
  );
}
