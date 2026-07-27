'use client';

import { useState } from 'react';
import { ClientPMSAnalysis, ClientFacebookStats, PromoCodeResult, LeadMatchEntry, ConfidenceLevel } from '@/types';
import { formatCurrency, formatNumber } from '@/lib/utils';
import { promoListToTabText } from '@/lib/analysis/promoAnalysis';
import { leadListToTabText } from '@/lib/analysis/leadAnalysis';
import { Card, CardContent, StatCard } from './ui/Card';
import { CopyButton } from './ui/CopyButton';
import { AlertTriangle, Info, ChevronDown } from 'lucide-react';

const CONFIDENCE_CONFIG: Record<ConfidenceLevel, { dot: string; label: string; title: string }> = {
  high:        { dot: 'bg-emerald-500', label: 'High',        title: 'Explicit code name in PMS' },
  medium:      { dot: 'bg-amber-400',   label: 'Medium',      title: 'Attributed by discount amount + IG email' },
  low:         { dot: 'bg-orange-400',  label: 'Low',         title: 'Attributed by discount amount only' },
  unverifiable:{ dot: 'bg-red-400',     label: 'Unverifiable',title: 'Name-only match or Apple relay email' },
};

function ConfidenceDot({ level, reason }: { level: ConfidenceLevel; reason: string }) {
  const cfg = CONFIDENCE_CONFIG[level];
  return (
    <span
      title={`${cfg.label}: ${reason}`}
      className={`inline-block w-2 h-2 rounded-full flex-shrink-0 ${cfg.dot}`}
    />
  );
}

interface PMSAnalysisSectionProps {
  analysis: ClientPMSAnalysis;
  facebookStats?: ClientFacebookStats | null;
}

function SectionLabel({ number, title }: { number: number; title: string }) {
  return (
    <div className="flex items-center gap-3 mb-5">
      <span className="w-6 h-6 rounded-full bg-gray-900 text-white text-xs font-bold flex items-center justify-center flex-shrink-0">
        {number}
      </span>
      <h3 className="text-sm font-semibold text-gray-700">{title}</h3>
    </div>
  );
}

function PromoCodeTable({ codes }: { codes: PromoCodeResult[] }) {
  const guests = codes.flatMap((c) => c.guests.map((g) => ({ ...g, code: c.code })));
  if (guests.length === 0) return <EmptyState message="No promo code bookings found." />;

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-100">
      <table className="min-w-full text-sm">
        <thead>
          <tr className="bg-gray-50 border-b border-gray-100">
            <Th></Th>
            <Th>Guest Name</Th>
            <Th>Email</Th>
            <Th>Code</Th>
            <Th right>Amount Paid</Th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-50">
          {guests.map((g, i) => (
            <tr
              key={i}
              className={`hover:bg-gray-50/60 transition-colors ${g.isZeroRevenue ? 'opacity-50' : ''}`}
            >
              <Td>
                <ConfidenceDot level={g.confidence} reason={g.confidenceReason} />
              </Td>
              <Td>{g.name || '—'}</Td>
              <Td muted>{g.email || '—'}</Td>
              <Td>
                <span className="font-mono text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-md">
                  {g.code}
                </span>
              </Td>
              <Td right bold>
                {g.isZeroRevenue ? <span className="text-gray-400 text-xs">$0 — cancelled?</span> : formatCurrency(g.revenue)}
              </Td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function LeadTable({ matches }: { matches: LeadMatchEntry[] }) {
  if (matches.length === 0) return <EmptyState message="No matching leads found." />;

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-100">
      <table className="min-w-full text-sm">
        <thead>
          <tr className="bg-gray-50 border-b border-gray-100">
            <Th>Guest Name</Th>
            <Th>Email</Th>
            <Th right>Amount Paid</Th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-50">
          {matches.map((m, i) => (
            <tr key={i} className={`hover:bg-gray-50/60 transition-colors ${m.nameOnlyMatch ? 'bg-amber-50/40' : ''}`}>
              <Td>
                {m.guestName || '—'}
                {m.nameOnlyMatch && (
                  <span className="ml-2 text-[10px] font-medium text-amber-600 bg-amber-100 px-1.5 py-0.5 rounded">
                    name only
                  </span>
                )}
              </Td>
              <Td muted>{m.pmsEmail || m.ghlEmail || '—'}</Td>
              <Td right bold>{formatCurrency(m.revenue)}</Td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function CollapsibleList({
  label,
  count,
  copyButton,
  children,
}: {
  label: string;
  count: number;
  copyButton: React.ReactNode;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(false);
  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <div
          role="button"
          tabIndex={0}
          onClick={() => setOpen((v) => !v)}
          onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && setOpen((v) => !v)}
          className="flex items-center gap-2 cursor-pointer select-none"
        >
          <span className="text-xs font-semibold text-gray-400 uppercase tracking-widest">{label}</span>
          <span className="text-xs text-gray-400 font-normal">({count})</span>
          <ChevronDown
            className={`w-4 h-4 text-gray-400 transition-transform duration-200 ${open ? 'rotate-180' : ''}`}
          />
        </div>
        {open && copyButton}
      </div>
      {open && children}
    </div>
  );
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="rounded-xl border border-dashed border-gray-200 px-6 py-8 text-center">
      <p className="text-sm text-gray-400">{message}</p>
    </div>
  );
}

function Th({ children, right }: { children?: React.ReactNode; right?: boolean }) {
  return (
    <th
      className={`px-4 py-3 text-[11px] font-semibold text-gray-400 uppercase tracking-wider ${
        right ? 'text-right' : 'text-left'
      }`}
    >
      {children}
    </th>
  );
}

function Td({
  children,
  muted,
  right,
  bold,
}: {
  children: React.ReactNode;
  muted?: boolean;
  right?: boolean;
  bold?: boolean;
}) {
  return (
    <td
      className={`px-4 py-3 ${muted ? 'text-gray-400' : 'text-gray-700'} ${right ? 'text-right' : ''} ${
        bold ? 'font-semibold text-gray-900' : ''
      }`}
    >
      {children}
    </td>
  );
}

export default function PMSAnalysisSection({ analysis, facebookStats }: PMSAnalysisSectionProps) {
  const { promoCode, instagram, facebook } = analysis;

  // Facebook/Meta metrics come from the Meta Ads connection (Ads Manager data,
  // synced per campaign per day) — period-correct, unlike the all-time GHL tag
  // counts. Summed across the three campaign buckets.
  const buckets = [facebookStats?.followers, facebookStats?.retargeting, facebookStats?.newLeads];
  const metaLeads = buckets.reduce((s, b) => s + (b?.leads ?? 0), 0);
  const metaPurchases = buckets.reduce((s, b) => s + (b?.purchases ?? 0), 0);
  const metaValue = buckets.reduce((s, b) => s + (b?.purchasesConversionValue ?? 0), 0);
  const hasMeta = !!facebookStats;
  const totalPromoUses = promoCode.codes.reduce((s, c) => s + c.uses, 0);
  const totalPromoRev = promoCode.codes.reduce((s, c) => s + c.revenue, 0);
  const activeCodeCount = promoCode.codes.filter((c) => c.uses > 0).length;
  // Promo codes aren't available from the platform — hide the section entirely
  // when there's nothing to show rather than render an empty card.
  const showPromo = promoCode.codes.length > 0;

  return (
    <div className="space-y-4">
      {/* Promo Code Analysis */}
      {showPromo && (
      <Card>
        <CardContent>
          <SectionLabel number={1} title="Promo Code Analysis" />

          {promoCode.netIncomeWarning && (
            <div className="flex items-center gap-2 text-xs text-amber-700 bg-amber-50 border border-amber-100 rounded-lg px-3 py-2 mb-4">
              <AlertTriangle className="w-3.5 h-3.5 flex-shrink-0" />
              Revenue shown as NET INCOME — verify totals
            </div>
          )}

          <div className="grid grid-cols-3 gap-3 mb-5">
            <StatCard label="Total Uses" value={totalPromoUses} />
            <StatCard label="Total Revenue" value={formatCurrency(totalPromoRev)} />
            <StatCard label="Codes Active" value={`${activeCodeCount} of ${promoCode.codes.length}`} />
          </div>

          {/* Per-code summary pills */}
          {promoCode.codes.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-5">
              {promoCode.codes.map((c) => (
                <span
                  key={c.code}
                  className={`text-xs px-3 py-1.5 rounded-lg font-mono font-medium border ${
                    c.uses > 0
                      ? 'bg-gray-900 text-white border-gray-900'
                      : 'bg-gray-50 text-gray-400 border-gray-200'
                  }`}
                >
                  {c.code}
                  <span className="ml-2 opacity-60">
                    {c.uses} {c.uses === 1 ? 'use' : 'uses'} · {formatCurrency(c.revenue)}
                  </span>
                </span>
              ))}
            </div>
          )}

          {promoCode.unrecognizedCodes.length > 0 && (
            <div className="flex items-start gap-2 text-xs bg-red-50 border border-red-100 rounded-lg px-3 py-2 mb-4">
              <Info className="w-3.5 h-3.5 text-red-500 flex-shrink-0 mt-0.5" />
              <span className="text-red-700">
                <strong>Unrecognized codes:</strong> {promoCode.unrecognizedCodes.join(', ')}
              </span>
            </div>
          )}

          <CollapsibleList
            label="Promo Code List"
            count={promoCode.codes.flatMap((c) => c.guests).length}
            copyButton={<CopyButton getText={() => promoListToTabText(promoCode.codes)} label="Copy list" />}
          >
            <PromoCodeTable codes={promoCode.codes} />
          </CollapsibleList>

          {/* Confidence legend */}
          <div className="flex flex-wrap gap-4 mt-3 pt-3 border-t border-gray-100">
            {(Object.entries(CONFIDENCE_CONFIG) as [ConfidenceLevel, typeof CONFIDENCE_CONFIG[ConfidenceLevel]][]).map(([level, cfg]) => (
              <span key={level} className="flex items-center gap-1.5 text-xs text-gray-400">
                <span className={`w-2 h-2 rounded-full ${cfg.dot}`} />
                {cfg.label} — {cfg.title}
              </span>
            ))}
          </div>

          {promoCode.missingFromPromoSheet && (
            <p className="mt-3 text-xs text-amber-600">
              * This client has no entries in the promo codes sheet
            </p>
          )}
        </CardContent>
      </Card>
      )}

      {/* Instagram Lead Analysis */}
      <Card>
        <CardContent>
          <SectionLabel number={showPromo ? 2 : 1} title="Instagram Lead Analysis" />

          <div className="grid grid-cols-2 gap-3 mb-5">
            <StatCard
              label="Email Matches"
              value={instagram.totalGHLLeads > 0 ? instagram.matchCount : '—'}
              sub={
                instagram.totalGHLLeads > 0
                  ? `of ${instagram.totalGHLLeads} Instagram-tagged leads checked against direct bookings`
                  : 'No Instagram-tagged leads in GHL'
              }
            />
            <StatCard
              label="Total Revenue"
              value={
                instagram.matchCount > 0
                  ? formatCurrency(instagram.totalRevenue)
                  : instagram.totalGHLLeads > 0 ? formatCurrency(0) : '—'
              }
              sub={instagram.matchCount === 0 && instagram.totalGHLLeads > 0 ? 'No matched leads booked this period' : undefined}
            />
          </div>

          {instagram.hasNoEmail && (
            <div className="flex items-center gap-2 text-xs text-amber-700 bg-amber-50 border border-amber-100 rounded-lg px-3 py-2 mb-4">
              <AlertTriangle className="w-3.5 h-3.5 flex-shrink-0" />
              PMS has no email column — matches via name only
            </div>
          )}

          <CollapsibleList
            label="Instagram List"
            count={instagram.matchCount}
            copyButton={<CopyButton getText={() => leadListToTabText(instagram, 'INSTAGRAM LEADS')} label="Copy list" />}
          >
            <LeadTable matches={instagram.matches} />
          </CollapsibleList>
        </CardContent>
      </Card>

      {/* 3. Facebook Lead Analysis */}
      <Card>
        <CardContent>
          <SectionLabel number={showPromo ? 3 : 2} title="Facebook / Meta Lead Analysis" />

          {/* Primary: Meta Ads connection (Ads Manager numbers for this period) */}
          <div className="grid grid-cols-3 gap-3 mb-5">
            <StatCard
              label="Leads"
              value={hasMeta ? formatNumber(metaLeads) : '—'}
              sub={hasMeta ? 'Meta Ads Manager · this period' : 'No Meta ad account connected'}
            />
            <StatCard
              label="Attributed Bookings"
              value={hasMeta ? formatNumber(metaPurchases) : '—'}
              sub={hasMeta ? 'Meta pixel purchase events' : undefined}
            />
            <StatCard
              label="Attributed Revenue"
              value={hasMeta ? formatCurrency(metaValue) : '—'}
              sub={
                hasMeta
                  ? metaValue > 0
                    ? 'Meta pixel purchase value'
                    : 'No pixel purchase value tracked this period'
                  : undefined
              }
            />
          </div>

          {facebook.hasNoEmail && (
            <div className="flex items-center gap-2 text-xs text-amber-700 bg-amber-50 border border-amber-100 rounded-lg px-3 py-2 mb-4">
              <AlertTriangle className="w-3.5 h-3.5 flex-shrink-0" />
              PMS has no email column — matches via name only
            </div>
          )}

          {/* Secondary: GHL email verification against direct bookings */}
          {facebook.matchCount > 0 && (
            <p className="text-xs text-gray-400 mb-3">
              <span className="font-medium text-gray-600">
                {facebook.matchCount} verified email match{facebook.matchCount !== 1 ? 'es' : ''}
              </span>
              {' '}from Meta-tagged GHL leads · {formatCurrency(facebook.totalRevenue)} direct booking revenue
            </p>
          )}
          <CollapsibleList
            label="Verified guest matches (GHL)"
            count={facebook.matchCount}
            copyButton={<CopyButton getText={() => leadListToTabText(facebook, 'FACEBOOK LEADS')} label="Copy list" />}
          >
            <LeadTable matches={facebook.matches} />
          </CollapsibleList>
        </CardContent>
      </Card>
    </div>
  );
}
