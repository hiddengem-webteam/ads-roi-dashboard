import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat('en-US').format(value);
}

export function normalizeEmail(email: string): string {
  return email.trim().toLowerCase();
}

export function normalizeName(name: string): string {
  return name.trim().toLowerCase().replace(/\s+/g, ' ');
}

/** Copy tab-separated text to clipboard for sheet paste */
export async function copyToClipboard(text: string): Promise<void> {
  await navigator.clipboard.writeText(text);
}

/** Generate unique flag ID */
export function flagId(type: string, client: string, extra?: string): string {
  return `${type}-${client}-${extra ?? ''}`.replace(/\s+/g, '-');
}

/** Normalize a header for fuzzy matching: lowercase + replace underscores with spaces */
function normalizeHeader(h: string): string {
  return h.toLowerCase().replace(/_/g, ' ').trim();
}

/** Detect revenue column from PMS row keys */
export const REVENUE_COLUMN_CANDIDATES = [
  'Total paid',
  'TOTAL PAYOUT',
  'Grand Total',
  'Total price',
  'Total Price',
  'TotalAmount',
  'Total Amount',
  'total_amount',
  'Total',
  'NET INCOME',
  'Gross',
  'Reservation Total',
  'revenue',
  'rentalRevenue',
  'Revenue',
  'REVENUE',
  'total_revenue',
  'Income',
  'income',
  'Amount',
  'Payout',
];

export function detectRevenueColumn(headers: string[]): { column: string; isNetIncome: boolean } | null {
  for (const candidate of REVENUE_COLUMN_CANDIDATES) {
    if (headers.includes(candidate)) {
      return { column: candidate, isNetIncome: candidate === 'NET INCOME' };
    }
  }
  // Case-insensitive fallback
  for (const candidate of REVENUE_COLUMN_CANDIDATES) {
    const found = headers.find((h) => h.toLowerCase() === candidate.toLowerCase());
    if (found) return { column: found, isNetIncome: found.toUpperCase() === 'NET INCOME' };
  }
  // Normalized fallback: underscore → space, case-insensitive
  for (const candidate of REVENUE_COLUMN_CANDIDATES) {
    const norm = normalizeHeader(candidate);
    const found = headers.find((h) => normalizeHeader(h) === norm);
    if (found) return { column: found, isNetIncome: normalizeHeader(found) === 'net income' };
  }
  return null;
}

export const COUPON_COLUMN_CANDIDATES = [
  'Coupon name',
  'COUPON CODE',
  'Discount Code',
  'coupon',
  'Coupon',
  'promo_code',
  'PromoCode',
  'coupon_code',
  'Coupon Name',
  'coupon name',
  'discount_code',
  'Promo Code',
  'PromotionCode',
  'Promotion Code',
  'promotion_code',
  'PromoCode',
  'Voucher',
  'voucher',
];

export function detectCouponColumn(headers: string[]): string | null {
  for (const candidate of COUPON_COLUMN_CANDIDATES) {
    if (headers.includes(candidate)) return candidate;
  }
  for (const candidate of COUPON_COLUMN_CANDIDATES) {
    const found = headers.find((h) => h.toLowerCase() === candidate.toLowerCase());
    if (found) return found;
  }
  // Normalized fallback
  for (const candidate of COUPON_COLUMN_CANDIDATES) {
    const norm = normalizeHeader(candidate);
    const found = headers.find((h) => normalizeHeader(h) === norm);
    if (found) return found;
  }
  // Also detect any column named simply 'code' (e.g. Endless Stays uses 'CODE')
  const codeCol = headers.find((h) => h.toLowerCase() === 'code');
  if (codeCol) return codeCol;
  return null;
}

export const EMAIL_COLUMN_CANDIDATES = [
  'Email',
  'email',
  'EMAIL',
  'Guest Email',
  'guest_email',
  'Email Address',
  'email_address',
];

export function detectEmailColumn(headers: string[]): string | null {
  for (const candidate of EMAIL_COLUMN_CANDIDATES) {
    if (headers.includes(candidate)) return candidate;
  }
  for (const candidate of EMAIL_COLUMN_CANDIDATES) {
    const found = headers.find((h) => h.toLowerCase() === candidate.toLowerCase());
    if (found) return found;
  }
  // Normalized fallback (handles guest_email → guest email → email match)
  for (const candidate of EMAIL_COLUMN_CANDIDATES) {
    const norm = normalizeHeader(candidate);
    const found = headers.find((h) => normalizeHeader(h) === norm);
    if (found) return found;
  }
  // Any header containing 'email'
  const emailCol = headers.find((h) => h.toLowerCase().includes('email'));
  return emailCol ?? null;
}

export const GUEST_COLUMN_CANDIDATES = [
  'Guest',
  'guest',
  'Guest name',
  'Guest Name',
  'Name',
  'name',
  'guest_name',
  'Full Name',
  'full_name',
  'Customer',
  'customer',
];

export function detectGuestColumn(headers: string[]): string | null {
  for (const candidate of GUEST_COLUMN_CANDIDATES) {
    if (headers.includes(candidate)) return candidate;
  }
  for (const candidate of GUEST_COLUMN_CANDIDATES) {
    const found = headers.find((h) => h.toLowerCase() === candidate.toLowerCase());
    if (found) return found;
  }
  // Normalized fallback
  for (const candidate of GUEST_COLUMN_CANDIDATES) {
    const norm = normalizeHeader(candidate);
    const found = headers.find((h) => normalizeHeader(h) === norm);
    if (found) return found;
  }
  return null;
}

export function parseNumber(val: unknown): number {
  if (typeof val === 'number') return isNaN(val) ? 0 : val;
  if (!val) return 0;
  const str = String(val).replace(/[$,\s]/g, '');
  const n = parseFloat(str);
  return isNaN(n) ? 0 : n;
}
