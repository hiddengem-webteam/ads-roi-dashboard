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
  { key: 'followers', label: 'Followers', color: 'text-blue-600 bg-blue-50 border-blue-100' },
  { key: 'retargeting', label: 'Retargeting', color: 'text-amber-600 bg-amber-50 border-amber-100' },
  { key: 'newLeads', label: 'New Leads', color: 'text-emerald-600 bg-emerald-50 border-emerald-100' },
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
  instagramLeads,
  facebookLeads,
  avgDirectBookingValue,
}: {
  s: CampaignStats;
  bookingRevenue: number;
  followersUses?: number;
  followersDeduped?: number;
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
  const pctOfBookingValue =
    costPerBooking !== null && avgDirectBookingValue && avgDirectBookingValue > 0
      ? (costPerBooking / avgDirectBookingValue) * 100
      : null;

  const bookingRevenueSub =
    s.type === 'Retargeting' && s.purchases > 0 && avgDirectBookingValue
      ? `${formatNumber(s.purchases)} FB events × ${formatCurrency(avgDirectBookingValue)} avg booking value`
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

      {/* Row 2: Booking attribution */}
      <div className="grid grid-cols-3 gap-3">
        <StatCard
          label="Total Bookings"
          value={attributedBookings > 0 ? formatNumber(attributedBookings) : '—'}
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
          sub={pctOfBookingValue !== null ? 'Cost per booking ÷ avg booking value' : undefined}
        />
      </div>

      {/* Row 3: Revenue */}
      <div className="grid grid-cols-3 gap-3">
        <StatCard
          label="Booking Revenue"
          value={bookingRevenue > 0 ? formatCurrency(bookingRevenue) : '—'}
          sub={bookingRevenueSub}
        />
        <StatCard label="ROAS" value={roas} sub={roas !== '—' ? 'Revenue ÷ Spend' : undefined} />
      </div>
      {s.type === 'Followers' && instagramLeads && instagramLeads.matchCount > 0 && (
        <p className="text-xs text-gray-400">
          <span className="font-medium text-gray-600">{instagramLeads.matchCount} email match{instagramLeads.matchCount !== 1 ? 'es' : ''}</span>
          {' '}from Instagram leads · {formatCurrency(instagramLeads.totalRevenue)} revenue
        </p>
      )}
      {s.type === 'Followers' && (followersDeduped ?? 0) > 0 && (
        <p className="text-xs text-amber-600">
          <span className="font-medium">{followersDeduped} booking{followersDeduped !== 1 ? 's' : ''} moved to New Leads</span>
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
      <div className="text-sm text-gray-400 italic px-1">No Facebook campaigns found for this client.</div>
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
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-4">
          Facebook Campaign Stats
        </p>
        {/* Tabs */}
        <div className="flex gap-2 border-b border-gray-100 -mx-6 px-6">
          {available.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`pb-3 text-sm font-medium transition-colors border-b-2 -mb-px px-1 ${
                activeTab === tab.key
                  ? 'border-gray-900 text-gray-900'
                  : 'border-transparent text-gray-400 hover:text-gray-600'
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
            instagramLeads={activeTab === 'followers' ? instagramLeads : null}
            facebookLeads={activeTab === 'newLeads' ? facebookLeads : null}
            avgDirectBookingValue={avgDirectBookingValue}
          />
        )}
      </CardContent>
    </Card>
  );
}
