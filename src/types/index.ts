// ─── Raw CSV Row Types ────────────────────────────────────────────────────────

export interface FacebookAdsRow {
  accountName: string;
  campaignName: string;
  amountSpent: number;
  linkClicks: number;
  leads: number;
  impressions: number;
  purchases: number;
  purchasesConversionValue: number;
}

export interface PromoCodeRow {
  client: string;
  discount: string;
  code: string;
  purpose: string;
  campaignType: string;
}

export interface PMSRow {
  guest: string;
  email: string;
  couponName: string;
  couponDiscount: number;
  revenue: number;
  checkIn: string;
  checkOut: string;
  listing: string;
  revenueColumnUsed: string;
  source: string;
}

export interface PMSSummary {
  totalRevenue: number;
  avgDirectBookingValue: number;
  directBookingCount: number;
  zeroRevenueCount: number;
  hasSourceColumn: boolean;
}

export interface GHLRow {
  contactId: string;
  firstName: string;
  lastName: string;
  phone: string;
  email: string;
  created: string;
  tags: string;
}

// ─── Campaign / Facebook Stats ────────────────────────────────────────────────

export type CampaignType = 'Followers' | 'Retargeting' | 'New Leads';

export interface CampaignStats {
  type: CampaignType;
  spend: number;
  impressions: number;
  linkClicks: number;
  leads: number;
  purchases: number;
  purchasesConversionValue: number;
}

export interface ClientFacebookStats {
  clientName: string;
  accountName: string;
  followers?: CampaignStats;
  retargeting?: CampaignStats;
  newLeads?: CampaignStats;
}

// ─── PMS Analysis ─────────────────────────────────────────────────────────────

export type ConfidenceLevel = 'high' | 'medium' | 'low' | 'unverifiable';

export interface PromoGuestEntry {
  name: string;
  email: string;
  revenue: number;
  confidence: ConfidenceLevel;
  confidenceReason: string;
  isZeroRevenue?: boolean;
}

export interface PromoCodeResult {
  code: string;
  discount: string;
  purpose: string;
  campaignType: string;
  uses: number;
  revenue: number;
  guests: PromoGuestEntry[];
  unrecognized?: boolean;
}

export interface PromoCodeAnalysis {
  codes: PromoCodeResult[];
  totalUses: number;
  totalRevenue: number;
  unrecognizedCodes: string[];
  missingFromPromoSheet: boolean;
  netIncomeWarning: boolean;
}

export interface LeadMatchEntry {
  guestName: string;
  pmsEmail: string;
  ghlFirstName: string;
  ghlLastName: string;
  ghlEmail: string;
  revenue: number;
  nameOnlyMatch: boolean;
}

export interface LeadAnalysis {
  matchCount: number;
  totalRevenue: number;
  matches: LeadMatchEntry[];
  hasNoEmail: boolean;
  totalGHLLeads: number;
}

export interface ClientPMSAnalysis {
  clientName: string;
  promoCode: PromoCodeAnalysis;
  instagram: LeadAnalysis;
  facebook: LeadAnalysis;
  summary: PMSSummary;
}

// ─── Flags ────────────────────────────────────────────────────────────────────

export type FlagType =
  | 'unrecognized-code'
  | 'missing-from-promo-sheet'
  | 'net-income-warning'
  | 'name-only-match'
  | 'platform-email'
  | 'no-pms-data'
  | 'missing-ghl';

export interface Flag {
  id: string;
  type: FlagType;
  clientName: string;
  message: string;
  details?: string;
}

// ─── Application State ────────────────────────────────────────────────────────

export interface UploadedFiles {
  metaAds: File | null;
  promoCodes: File | null;
  pmsFiles: Record<string, File>;
  ghlFiles: Record<string, File>;
}

export interface ProcessedData {
  clients: Record<string, ClientData>;
  flags: Flag[];
  lastProcessed: Date;
}

export interface ClientData {
  name: string;
  facebookStats: ClientFacebookStats | null;
  pmsAnalysis: ClientPMSAnalysis | null;
  hasPMS: boolean;
  hasGHL: boolean;
}
