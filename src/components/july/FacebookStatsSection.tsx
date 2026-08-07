'use client';

import { useState } from 'react';
import { ClientFacebookStats, CampaignStats, LeadAnalysis } from '@/types';
import { formatCurrency, formatNumber } from '@/lib/utils';
import { statsToTabRow } from '@/lib/analysis/campaignAnalysis';
import { Card, CardContent, StatCard } from './ui/Card';
import { CopyButton } from './ui/CopyButton';

interface CampaignRevenue {
  followers: number;
  followersUses: number;
  followersDeduped: number;
  retargeting: number;
  retargetingUsesConversionValue: boolean;
  newLeads: number;
}

interface FacebookStatsSectionProps {
  stats: ClientFacebookStats;
  campaignRevenue: CampaignRevenue;
  instagramLeads?: LeadAnalysis | null;
  facebookLeads?: LeadAnalysis | null;
  avgDirectBookingValue?: number;
}

const CAMPAIGN_TABS = [
  { key: 'followers', label: 'Followers' },
  { key: 'retargeting', label: 'Retargeting' },
  { key: 'newLeads', label: 'New Leads' },
] as const;

function formatRoas(revenue: number, spend: number): string {
  if (spend <= 0 || revenue <= 0) return '—';
  return `${(revenue / spend).toFixed(2)}x`;
}

function CampaignPanel({
  s,
  bookingRevenue,
  followersUses,
  followersDeduped,
  retargetingUsesConversionValue,
  instagramLeads,
  facebookLeads,
  avgDirectBookingValue,
}: {
  s: CampaignStats;
  bookingRevenue: number;
  followersUses?: number;
  followersDeduped?: number;
  retargetingUsesConversionValue?: boolean;
  instagramLeads?: LeadAnalysis | null;
  facebookLeads?: LeadAnalysis | null;
  avgDirectBookingValue?: number;
}) {
  const roas = formatRoas(bookingRevenue, s.spend);

  // Attributed booking count per campaign type
  const attributedBookings =
    s.type === 'Followers' ? (followersUses ?? 0)
    : s.type === 'Retargeting' ? s.purchases
    : (facebookLeads?.matchCount ?? 0);

  const costPerBooking = attributedBookings > 0 && s.spend > 0 ? s.spend / attributedBookings : null;

  // Campaign-specific avg booking value, derived from this campaign's own
  // Booking Revenue ÷ its attributed bookings — not the client-wide PMS
  // average — so the % stays consistent with the Booking Revenue shown above.
  const campaignAvgBookingValue = attributedBookings > 0 && bookingRevenue > 0 ? bookingRevenue / attributedBookings : null;
  const pctOfBookingValue =
    costPerBooking !== null && campaignAvgBookingValue !== null
      ? (costPerBooking / campaignAvgBookingValue) * 100
      : null;

  // Booking attribution comes from promo codes (Followers), FB purchase events
  // (Retargeting) or matched leads (New Leads). When none is available, hide the
  // tiles instead of showing empty "—" placeholders.
  const hasBookingData = attributedBookings > 0 || bookingRevenue > 0;

  const bookingRevenueSub =
    s.type === 'Retargeting' && retargetingUsesConversionValue
      ? 'Facebook Ads Manager purchase conversion value'
      : s.type === 'Retargeting' && s.purchases > 0 && avgDirectBookingValue
      ? `${formatNumber(s.purchases)} FB events × ${formatCurrency(avgDirectBookingValue)} avg booking value (no conversion value reported)`
      : s.type === 'Followers'
      ? `${followersUses ?? 0} booking${(followersUses ?? 0) !== 1 ? 's' : ''} · From promo code attribution`
      : s.type === 'New Leads' && facebookLeads
      ? `${facebookLeads.matchCount} matched Facebook lead${facebookLeads.matchCount !== 1 ? 's' : ''} from PMS`
      : undefined;

  const totalBookingsSub =
    s.type === 'Followers' ? 'Promo code attributions'
    : s.type === 'Retargeting' ? 'Facebook Ads Manager purchase events'
    : 'Matched Facebook leads from PMS';

  return (
    <div className="space-y-3">
      {/* Row 1: Ad delivery */}
      <div className="grid grid-cols-3 gap-3">
        <StatCard label="Spend" value={formatCurrency(s.spend)} sub="Facebook Ads Manager" />
        <StatCard label="Impressions" value={formatNumber(s.impressions)} sub="Facebook Ads Manager" />
        <StatCard label="Link Clicks" value={formatNumber(s.linkClicks)} sub="Facebook Ads Manager" />
      </div>

      {/* Row 1b: Instagram GHL leads — Followers only */}
      {s.type === 'Followers' && instagramLeads && (
        <div className="grid grid-cols-3 gap-3">
          <StatCard
            label="Instagram Tag Leads"
            value={instagramLeads.totalGHLLeads > 0 ? formatNumber(instagramLeads.totalGHLLeads) : '—'}
            sub="Total leads with Instagram tag in GHL"
          />
        </div>
      )}

      {/* Row 1c: Leads + CPL — New Leads campaigns only */}
      {s.type === 'New Leads' && (
        <div className="grid grid-cols-3 gap-3">
          <StatCard
            label="Leads"
            value={s.leads > 0 ? formatNumber(s.leads) : '—'}
            sub="Facebook lead form submissions"
          />
          <StatCard
            label="Cost Per Lead"
            value={s.leads > 0 ? formatCurrency(s.spend / s.leads) : '—'}
            sub={s.leads > 0 ? `${formatCurrency(s.spend)} ÷ ${formatNumber(s.leads)} leads` : undefined}
          />
        </div>
      )}

      {/* Rows 2 & 3: Booking attribution + revenue — only when we have attribution data */}
      {hasBookingData && (
        <>
          <div className="grid grid-cols-3 gap-3">
            <StatCard
              label="Total Bookings"
              value={formatNumber(attributedBookings)}
              sub={totalBookingsSub}
            />
            <StatCard
              label="Cost Per Booking"
              value={costPerBooking !== null ? formatCurrency(costPerBooking) : '—'}
              sub={costPerBooking !== null ? `${formatCurrency(s.spend)} ÷ ${attributedBookings} booking${attributedBookings !== 1 ? 's' : ''}` : undefined}
            />
            <StatCard
              label="% of Booking Value"
              value={pctOfBookingValue !== null ? `${pctOfBookingValue.toFixed(1)}%` : '—'}
              sub={pctOfBookingValue !== null ? `Cost per booking ÷ ${formatCurrency(campaignAvgBookingValue!)} avg booking value (this campaign)` : undefined}
            />
          </div>

          <div className="grid grid-cols-3 gap-3">
            <StatCard
              label="Booking Revenue"
              value={bookingRevenue > 0 ? formatCurrency(bookingRevenue) : '—'}
              sub={bookingRevenueSub}
            />
            <StatCard label="ROAS" value={roas} sub={roas !== '—' ? 'Revenue ÷ Spend' : undefined} />
          </div>
        </>
      )}
      {s.type === 'Followers' && instagramLeads && instagramLeads.matchCount > 0 && (
        <p className="text-[12px] text-[var(--muted-soft)]">
          <span className="font-semibold text-[var(--muted)]">{instagramLeads.matchCount} email match{instagramLeads.matchCount !== 1 ? 'es' : ''}</span>
          {' '}from Instagram leads · {formatCurrency(instagramLeads.totalRevenue)} revenue
        </p>
      )}
      {s.type === 'Followers' && (followersDeduped ?? 0) > 0 && (
        <p className="text-[12px] text-[var(--warning-ink)]">
          <span className="font-semibold">{followersDeduped} booking{followersDeduped !== 1 ? 's' : ''} moved to New Leads</span>
          {' '}— guest{followersDeduped !== 1 ? 's' : ''} matched in both promo codes and Facebook lead ads; attributed to New Leads campaign
        </p>
      )}
      <div className="flex justify-end">
        <CopyButton getText={() => statsToTabRow(s)} label="Copy row" />
      </div>
    </div>
  );
}

export default function FacebookStatsSection({ stats, campaignRevenue, instagramLeads, facebookLeads, avgDirectBookingValue }: FacebookStatsSectionProps) {
  const available = CAMPAIGN_TABS.filter((t) => stats[t.key]);
  const [activeTab, setActiveTab] = useState(available[0]?.key ?? 'followers');

  if (available.length === 0) {
    return (
      <div className="text-[13px] text-[var(--muted-soft)] italic px-1">No Facebook campaigns found for this client.</div>
    );
  }

  const activeStats = stats[activeTab as keyof ClientFacebookStats] as CampaignStats | undefined;
  const activeRevenue =
    activeTab === 'followers' ? campaignRevenue.followers
    : activeTab === 'retargeting' ? campaignRevenue.retargeting
    : campaignRevenue.newLeads;

  return (
    <Card>
      {/* Section label */}
      <div className="px-6 pt-5 pb-0">
        <p className="text-[12px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em] mb-4">
          Facebook Campaign Stats
        </p>
        {/* Tabs */}
        <div className="flex gap-2 border-b border-[var(--border)] -mx-6 px-6">
          {available.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`pb-3 text-[13px] font-semibold transition-colors duration-150 border-b-2 -mb-px px-1 ${
                activeTab === tab.key
                  ? 'border-[var(--brand)] text-[var(--foreground)]'
                  : 'border-transparent text-[var(--muted-soft)] hover:text-[var(--muted)]'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>
      <CardContent className="pt-5">
        {activeStats && (
          <CampaignPanel
            s={activeStats}
            bookingRevenue={activeRevenue}
            followersUses={campaignRevenue.followersUses}
            followersDeduped={campaignRevenue.followersDeduped}
            retargetingUsesConversionValue={campaignRevenue.retargetingUsesConversionValue}
            instagramLeads={activeTab === 'followers' ? instagramLeads : null}
            facebookLeads={activeTab === 'newLeads' ? facebookLeads : null}
            avgDirectBookingValue={avgDirectBookingValue}
          />
        )}
      </CardContent>
    </Card>
  );
}
