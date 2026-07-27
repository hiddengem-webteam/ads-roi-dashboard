// Server-side client for the HiddenGem AI platform API.
//
// Auth: the platform's middleware maps `Authorization: Bearer <CRON_SECRET>`
// onto a trusted dashboard session (it sets the X-Dashboard-Session header the
// routes check), so a single agency-wide secret unlocks the read endpoints we
// need — /clients, /admin/roi-export, /clients/[id]/contacts.
//
// SERVER-ONLY. The secret must never reach the browser bundle; only import this
// from route handlers / server code, never from a 'use client' component.

export interface PlatformConfig {
  baseUrl: string;
  secret: string;
}

export function getPlatformConfig(): PlatformConfig {
  const baseUrl = (process.env.HG_PLATFORM_URL ?? '').replace(/\/+$/, '');
  const secret = process.env.HG_CRON_SECRET ?? '';
  if (!baseUrl) throw new Error('HG_PLATFORM_URL env var is not set (see .env.example)');
  if (!secret) throw new Error('HG_CRON_SECRET env var is not set (see .env.example)');
  return { baseUrl, secret };
}

export async function platformGet<T>(cfg: PlatformConfig, pathAndQuery: string): Promise<T> {
  const res = await fetch(`${cfg.baseUrl}${pathAndQuery}`, {
    headers: { Authorization: `Bearer ${cfg.secret}` },
    cache: 'no-store', // server-to-server sync reads must never be cached
  });
  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(
      `GET ${pathAndQuery} → ${res.status} ${res.statusText}${body ? `: ${body.slice(0, 200)}` : ''}`,
    );
  }
  return res.json() as Promise<T>;
}

// ─── Response shapes (ground-truthed against the platform route handlers) ──────

/** GET /api/v1/clients?all=1 */
export interface PlatformClient {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
}

/** One campaign row inside GET /api/v1/admin/roi-export */
export interface RoiExportCampaign {
  tenant_id: string;
  campaign_name: string | null;
  objective: string | null;
  status: string | null;
  spend: number;
  impressions: number;
  clicks: number; // Meta "clicks (all)" — NOT link clicks; use link_clicks below
  link_clicks: number;
  landing_page_views: number;
  page_likes_follows: number;
  leads: number;
  purchases: number;
  revenue: number | null; // null = pixel value-tracking absent for the whole window
}

export interface RoiExportBooking {
  check_in: string | null;
  revenue: number;
  guest: string | null;
  email: string | null;
}

export interface RoiExportTenant {
  campaigns: RoiExportCampaign[];
  direct_booking_revenue: number;
  direct_booking_count: number;
  ig_bio_leads: number;
  direct_bookings: RoiExportBooking[];
}

/** GET /api/v1/admin/roi-export?from&to */
export interface RoiExportResponse {
  from: string;
  to: string;
  tenants: Record<string, RoiExportTenant>; // keyed by tenant_id
}

/** GET /api/v1/clients/[id]/contacts */
export interface PlatformContact {
  id: string;
  name: string | null; // first + last collapsed into one field
  role: string | null; // GHL tags, comma-joined (e.g. "instagram lead, customer")
  email: string | null;
  phone: string | null;
  created_at: string | null;
  updated_at: string | null;
}
