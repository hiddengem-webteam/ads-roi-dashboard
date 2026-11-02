-- Month-to-date direct revenue and promo-code use per client, for the
-- "This month" strip in the client benchmark review.
--
-- Run against the HiddenGem AI Supabase project (ahpzvyhrnvzetpygujws)
-- through the Supabase connector, with {RUN_DATE} replaced by the run date
-- (YYYY-MM-DD). Save the result rows as pms_mtd.json next to generate_report.py.
--
-- Rules mirror the platform (src/lib/pms in the hiddengem-ai repo):
--   * bookings by booked_at, revenue-status allowlist, negatives floored at 0
--   * direct = platform not matching an OTA pattern (airbnb, vrbo, booking.com ...)
--   * tenants that share a PMS account are narrowed to their own properties
--     (pms_included_property_ids, else pms_property_filter)
-- "Previous span" is the same day range in the previous month (1st to the
-- run date's day-of-month), so the trend compares like with like.
-- Since 2026-10-30 the query also returns the last 30 days (d30_start to the
-- run date) of direct revenue and promo-code bookings, with revenue per code,
-- for the Discovery bucket row (giveaway + lead spend scored on promo-code ROAS,
-- Meta Ads Strategy 2026-10-28).
-- Promo codes: Guesty stores the code on the booking (_discounts[].code);
-- Hostaway stores only a coupon id (counted, no names); Hospitable and
-- Cloudbeds store nothing.
with params as (
  select date '{RUN_DATE}' as run_date,
         date_trunc('month', date '{RUN_DATE}')::date as m_start,
         (date_trunc('month', date '{RUN_DATE}') - interval '1 month')::date as p_start,
         (date '{RUN_DATE}' - 30) as d30
),
spans as (
  select run_date, m_start, p_start, d30, (p_start + (run_date - m_start))::date as p_end from params
),
tn as (
  select t.id, t.name, t.pms_included_property_ids as ids, t.pms_property_filter as flt,
         (select string_agg(pc.provider, ',') from pms_connections pc where pc.tenant_id = t.id and pc.is_active) as provider
  from tenants t where t.is_active
),
props as (
  select tn.id as tenant_id, p.id as property_id
  from tn join pms_properties p on p.tenant_id = tn.id
  where (tn.ids is not null and array_length(tn.ids,1) > 0 and p.id::text = any(tn.ids))
     or ((tn.ids is null or array_length(tn.ids,1) = 0) and tn.flt is not null and p.is_active and p.name ilike '%' || tn.flt || '%')
     or ((tn.ids is null or array_length(tn.ids,1) = 0) and tn.flt is null)
),
bk as (
  select tn.name, tn.provider, b.booked_at::date as booked, greatest(coalesce(b.total_revenue,0),0) as rev,
    (b.platform is null or btrim(b.platform) = '' or (
      lower(btrim(b.platform)) not in ('google','booking') and
      lower(b.platform) not similar to '%(airbnb|vrbo|homeaway|vacationrentals|booking.com|bookingcom|booking_dot_com|expedia|hotels.com|tripadvisor|flipkey|agoda|marriott|str-import|uploaded_|google_vacation_rentals)%'
    )) as is_direct,
    coalesce(
      (select string_agg(upper(btrim(d->>'code')), '|')
         from jsonb_array_elements(case when jsonb_typeof(b.raw_data->'_discounts') = 'array' then b.raw_data->'_discounts' else '[]'::jsonb end) d
        where coalesce(d->>'code','') <> ''),
      case when b.raw_data->>'reservationCouponId' is not null then 'COUPON (name not stored)' end
    ) as codes
  from tn
  join pms_bookings b on b.tenant_id = tn.id
  join props pr on pr.tenant_id = tn.id and pr.property_id = b.property_id
  cross join spans s
  where lower(b.status) in ('confirmed','checked_in','checked_out','closed','booked','reserved')
    and b.booked_at >= least(s.p_start, s.d30) and b.booked_at < s.run_date + 1
),
code_counts as (
  select bk.name, c as code, count(*) as n
  from bk cross join spans s, unnest(string_to_array(bk.codes, '|')) as c
  where bk.is_direct and bk.booked >= s.m_start and bk.codes is not null
  group by 1, 2
),
code30 as (
  select bk.name, c as code, count(*) as n, round(sum(bk.rev)) as rev
  from bk cross join spans s, unnest(string_to_array(bk.codes, '|')) as c
  where bk.is_direct and bk.booked >= s.d30 and bk.codes is not null
  group by 1, 2
),
agg as (
  select bk.name, max(bk.provider) as provider,
    round(coalesce(sum(rev) filter (where is_direct and booked >= s.m_start), 0)) as mtd_rev,
    count(*) filter (where is_direct and booked >= s.m_start) as mtd_bk,
    round(coalesce(sum(rev) filter (where is_direct and booked >= s.p_start and booked <= s.p_end), 0)) as prev_rev,
    count(*) filter (where is_direct and booked >= s.p_start and booked <= s.p_end) as prev_bk,
    count(*) filter (where is_direct and booked >= s.m_start and codes is not null) as promo_uses,
    count(*) filter (where is_direct and booked >= s.d30 and codes is not null) as promo30_bk,
    round(coalesce(sum(rev) filter (where is_direct and booked >= s.d30 and codes is not null), 0)) as promo30_rev,
    round(coalesce(sum(rev) filter (where is_direct and booked >= s.d30), 0)) as direct30_rev,
    count(*) filter (where is_direct and booked >= s.d30) as direct30_bk
  from bk cross join spans s
  group by bk.name
)
select a.name, a.provider,
  s.m_start as month_start, s.run_date, s.p_start as prev_start, s.p_end as prev_end, s.d30 as d30_start,
  a.mtd_rev, a.mtd_bk, a.prev_rev, a.prev_bk,
  case when a.prev_rev > 0 then round((a.mtd_rev - a.prev_rev) / a.prev_rev * 100) end as vs_prev_pct,
  a.promo_uses,
  (select string_agg(code || ' ×' || n, ', ' order by n desc, code) from code_counts cc where cc.name = a.name) as promo_codes,
  case when a.provider ilike '%guesty%' then 'codes'
       when a.provider ilike '%hostaway%' then 'count only'
       else 'unavailable' end as promo_source,
  a.promo30_bk, a.promo30_rev, a.direct30_rev, a.direct30_bk,
  (select string_agg(code || '|' || n || '|' || rev, ';' order by rev desc, code) from code30 c where c.name = a.name) as promo30_codes
from agg a cross join spans s
order by a.name;
