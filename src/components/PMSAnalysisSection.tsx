'use client';

import { useState } from 'react';
import { ClientPMSAnalysis, ClientFacebookStats, PromoCodeResult, ConfidenceLevel } from '@/types';
import { formatCurrency, formatNumber } from '@/lib/utils';
import { promoListToTabText } from '@/lib/analysis/promoAnalysis';
 
import { Card, CardContent, StatCard } from './ui/Card';
import { CopyButton } from './ui/CopyButton';
import { AlertTriangle, Info, ChevronDown } from 'lucide-react';

const CONFIDENCE_CONFIG: Record<ConfidenceLevel, { dot: string; label: string; title: string }> = {
  high:        { dot: 'bg-[var(--success)]',    label: 'High',        title: 'Explicit code name in PMS' },
  medium:      { dot: 'bg-[var(--warning)]',    label: 'Medium',      title: 'Attributed by discount amount + IG email' },
  low:         { dot: 'bg-[var(--muted-soft)]', label: 'Low',         title: 'Attributed by discount amount only' },
  unverifiable:{ dot: 'bg-[var(--danger)]',     label: 'Unverifiable',title: 'Name-only match or Apple relay email' },
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

export interface EmailMatchRow {
  guest: string;
  email: string;
  bookings: number;
  revenue: number;
  via: string;
  source?: 'instagram' | 'facebook';
}
export interface EmailMatchGroup {
  matchedEmails: number;
  bookings: number;
  revenue: number;
  instagram?: number;
  facebook?: number;
  matches: EmailMatchRow[];
}
export interface ClientEmailMatches {
  ads: EmailMatchGroup;
  organic: EmailMatchGroup;
}

interface PMSAnalysisSectionProps {
  /** Live GHL email-match analysis (sync-ghl-email-matches.mts); null = not synced */
  emailMatches?: ClientEmailMatches | null;
  analysis: ClientPMSAnalysis;
  facebookStats?: ClientFacebookStats | null;
}

function SectionLabel({ number, title }: { number: number; title: string }) {
  return (
    <div className="flex items-center gap-3 mb-5">
      <span className="w-6 h-6 rounded-full bg-[var(--brand)] text-white text-[12px] font-bold flex items-center justify-center flex-shrink-0">
        {number}
      </span>
      <h3 className="text-[16px] font-bold text-[var(--foreground)] tracking-[-0.01em]">{title}</h3>
    </div>
  );
}

function PromoCodeTable({ codes }: { codes: PromoCodeResult[] }) {
  const guests = codes.flatMap((c) => c.guests.map((g) => ({ ...g, code: c.code })));
  if (guests.length === 0) return <EmptyState message="No promo code bookings found." />;

  return (
    <div className="overflow-x-auto rounded-[12px] border border-[var(--border)]">
      <table className="min-w-full text-[13px]">
        <thead>
          <tr className="bg-[var(--fill-gray)] border-b border-[var(--border)]">
            <Th></Th>
            <Th>Guest Name</Th>
            <Th>Email</Th>
            <Th>Code</Th>
            <Th right>Amount Paid</Th>
          </tr>
        </thead>
        <tbody className="divide-y divide-[var(--divider)]">
          {guests.map((g, i) => (
            <tr
              key={i}
              className={`bg-white hover:bg-[var(--fill-cool)] transition-colors duration-150 ${g.isZeroRevenue ? 'opacity-50' : ''}`}
            >
              <Td>
                <ConfidenceDot level={g.confidence} reason={g.confidenceReason} />
              </Td>
              <Td>{g.name || '—'}</Td>
              <Td muted>{g.email || '—'}</Td>
              <Td>
                <span className="font-mono text-[11px] bg-[var(--fill-gray)] text-[var(--foreground)] px-2 py-1 rounded-[6px]">
                  {g.code}
                </span>
              </Td>
              <Td right bold>
                {g.isZeroRevenue ? <span className="text-[var(--muted-soft)] text-[12px] font-normal">$0 — cancelled?</span> : formatCurrency(g.revenue)}
              </Td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}


function EmailMatchTable({ matches, showSource }: { matches: EmailMatchRow[]; showSource?: boolean }) {
  if (matches.length === 0) return <EmptyState message="No matched lead emails." />;
  return (
    <div className="overflow-x-auto rounded-[12px] border border-[var(--border)]">
      <table className="min-w-full text-[13px]">
        <thead>
          <tr className="bg-[var(--fill-gray)] border-b border-[var(--border)]">
            <Th>Guest</Th>
            <Th>Email</Th>
            {showSource && <Th>Source</Th>}
            <Th>Matched Via</Th>
            <Th right>Bookings</Th>
            <Th right>Revenue</Th>
          </tr>
        </thead>
        <tbody className="divide-y divide-[var(--divider)]">
          {matches.map((m, i) => (
            <tr key={i} className="bg-white hover:bg-[var(--fill-cool)] transition-colors duration-150">
              <Td>{m.guest || '—'}</Td>
              <Td muted>{m.email}</Td>
              {showSource && (
                <Td>
                  <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-[6px] ${m.source === 'instagram' ? 'bg-[rgba(124,77,243,.1)] text-[var(--ai-purple)]' : 'bg-[var(--fill-blue)] text-[var(--brand)]'}`}>
                    {m.source === 'instagram' ? 'Instagram' : 'Facebook'}
                  </span>
                </Td>
              )}
              <Td muted>{m.via}</Td>
              <Td right>{m.bookings}</Td>
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
          <span className="text-[12px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em]">{label}</span>
          <span className="text-[12px] text-[var(--muted-soft)] font-normal">({count})</span>
          <ChevronDown
            className={`w-4 h-4 text-[var(--muted-soft)] transition-transform duration-200 ${open ? 'rotate-180' : ''}`}
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
    <div className="rounded-[12px] border border-dashed border-[var(--border-strong)] px-6 py-8 text-center">
      <p className="text-[13px] text-[var(--muted-soft)]">{message}</p>
    </div>
  );
}

function Th({ children, right }: { children?: React.ReactNode; right?: boolean }) {
  return (
    <th
      className={`px-4 py-3 text-[11px] font-semibold text-[var(--muted)] uppercase tracking-[0.04em] ${
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
      className={`px-4 py-3 ${muted ? 'text-[var(--muted-soft)]' : 'text-[var(--foreground)]'} ${right ? 'text-right july-tabular' : ''} ${
        bold ? 'font-semibold text-[var(--foreground)]' : ''
      }`}
    >
      {children}
    </td>
  );
}

export default function PMSAnalysisSection({ analysis, emailMatches }: PMSAnalysisSectionProps) {
  const { promoCode } = analysis;

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
            <div className="flex items-center gap-2 text-[12px] text-[var(--warning-ink)] bg-[rgba(255,159,10,.1)] border border-[rgba(255,159,10,.25)] rounded-[10px] px-3 py-2 mb-4">
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
                  className={`text-[12px] px-3 py-1.5 rounded-[10px] font-mono font-medium border ${
                    c.uses > 0
                      ? 'bg-[var(--brand)] text-white border-[var(--brand)]'
                      : 'bg-[var(--fill-gray)] text-[var(--muted-soft)] border-[var(--border)]'
                  }`}
                >
                  {c.code}
                  <span className="ml-2 opacity-70">
                    {c.uses} {c.uses === 1 ? 'use' : 'uses'} · {formatCurrency(c.revenue)}
                  </span>
                </span>
              ))}
            </div>
          )}

          {promoCode.unrecognizedCodes.length > 0 && (
            <div className="flex items-start gap-2 text-[12px] bg-[rgba(220,38,38,.06)] border border-[rgba(220,38,38,.18)] rounded-[10px] px-3 py-2 mb-4">
              <Info className="w-3.5 h-3.5 text-[var(--danger)] flex-shrink-0 mt-0.5" />
              <span className="text-[var(--danger)]">
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
          <div className="flex flex-wrap gap-4 mt-3 pt-3 border-t border-[var(--border)]">
            {(Object.entries(CONFIDENCE_CONFIG) as [ConfidenceLevel, typeof CONFIDENCE_CONFIG[ConfidenceLevel]][]).map(([level, cfg]) => (
              <span key={level} className="flex items-center gap-1.5 text-[12px] text-[var(--muted-soft)]">
                <span className={`w-2 h-2 rounded-full ${cfg.dot}`} />
                {cfg.label} — {cfg.title}
              </span>
            ))}
          </div>

          {promoCode.missingFromPromoSheet && (
            <p className="mt-3 text-[12px] text-[var(--warning-ink)]">
              * This client has no entries in the promo codes sheet
            </p>
          )}
        </CardContent>
      </Card>
      )}

      {/* Ads Email Analysis — PMS booking emails matched to GHL contacts whose
          lead tag or attribution says Meta ADS (hybrid logic; see
          scripts/sync-ghl-email-matches.mts) */}
      <Card>
        <CardContent>
          <SectionLabel number={showPromo ? 2 : 1} title="Ads Email Analysis" />
          {emailMatches ? (
            <>
              <div className="grid grid-cols-3 gap-3 mb-5">
                <StatCard
                  label="Matched Emails"
                  value={formatNumber(emailMatches.ads.matchedEmails)}
                  sub="Booking emails matched to Meta-ads leads in GHL"
                />
                <StatCard
                  label="Attributed Bookings"
                  value={formatNumber(emailMatches.ads.bookings)}
                  sub="Bookings by those guests this period"
                />
                <StatCard
                  label="Attributed Revenue"
                  value={formatCurrency(emailMatches.ads.revenue)}
                  sub="Revenue from the matched emails"
                />
              </div>
              <CollapsibleList
                label="Matched emails"
                count={emailMatches.ads.matchedEmails}
                copyButton={<CopyButton getText={() => emailMatches.ads.matches.map((m) => `${m.guest}\t${m.email}\t${m.revenue}`).join('\n')} label="Copy list" />}
              >
                <EmailMatchTable matches={emailMatches.ads.matches} />
              </CollapsibleList>
            </>
          ) : (
            <EmptyState message="No GHL email-match data — run the sync (npm run sync:ghl-emails)." />
          )}
        </CardContent>
      </Card>

      {/* Organic Lead Email Analysis — same matching, tags/attribution point to
          organic Instagram or Facebook */}
      <Card>
        <CardContent>
          <SectionLabel number={showPromo ? 3 : 2} title="Organic Lead Email Analysis" />
          {emailMatches ? (
            <>
              <div className="grid grid-cols-3 gap-3 mb-5">
                <StatCard
                  label="Matched Emails"
                  value={formatNumber(emailMatches.organic.matchedEmails)}
                  sub={`Instagram ${emailMatches.organic.instagram ?? 0} · Facebook ${emailMatches.organic.facebook ?? 0}`}
                />
                <StatCard
                  label="Attributed Bookings"
                  value={formatNumber(emailMatches.organic.bookings)}
                  sub="Bookings by those guests this period"
                />
                <StatCard
                  label="Attributed Revenue"
                  value={formatCurrency(emailMatches.organic.revenue)}
                  sub="Revenue from the matched emails"
                />
              </div>
              <CollapsibleList
                label="Matched emails"
                count={emailMatches.organic.matchedEmails}
                copyButton={<CopyButton getText={() => emailMatches.organic.matches.map((m) => `${m.guest}\t${m.email}\t${m.source}\t${m.revenue}`).join('\n')} label="Copy list" />}
              >
                <EmailMatchTable matches={emailMatches.organic.matches} showSource />
              </CollapsibleList>
            </>
          ) : (
            <EmptyState message="No GHL email-match data — run the sync (npm run sync:ghl-emails)." />
          )}
        </CardContent>
      </Card>
    </div>
  );
}