-- Direct bookings per client over the last 28 days, for the pixel check's
-- Purchase-capture comparison (added 2026-10-30).
--
-- Run against the HiddenGem AI Supabase project (ahpzvyhrnvzetpygujws) through
-- the Supabase connector. Save the result rows as pms_direct_28d.json next to
-- write_report.py. Rules mirror pms_mtd.sql in the client-benchmark skill:
-- bookings by booked_at, revenue-status allowlist, direct = platform not an OTA,
-- shared-PMS tenants narrowed to their own properties.
with params as (
  select (now() - interval '28 days') as d28, (now() - interval '7 days') as d7
),
tn as (
  select t.id, t.name, t.pms_included_property_ids as ids, t.pms_property_filter as flt,
         (select string_agg(pc.provider, ',') from pms_connections pc where pc.tenant_id = t.id and pc.is_active) as provider,
         (select max(pc.last_sync_at) from pms_connections pc where pc.tenant_id = t.id and pc.is_active) as last_sync
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
  select tn.name, tn.provider, tn.last_sync, b.booked_at, greatest(coalesce(b.total_revenue,0),0) as rev,
    coalesce(nullif(btrim(b.platform),''),'None') as plat,
    -- manual, owner, phone and walk-in entries never fire a pixel; 'online' excludes them (2026-10-30)
    (lower(coalesce(b.platform,'')) similar to '%(manual|owner|phone|walk)%') as is_manual,
    (b.platform is null or btrim(b.platform) = '' or (
      lower(btrim(b.platform)) not in ('google','booking') and
      lower(b.platform) not similar to '%(airbnb|vrbo|homeaway|vacationrentals|booking.com|bookingcom|booking_dot_com|expedia|hotels.com|tripadvisor|flipkey|agoda|marriott|str-import|uploaded_|google_vacation_rentals)%'
    )) as is_direct
  from tn
  join pms_bookings b on b.tenant_id = tn.id
  join props pr on pr.tenant_id = tn.id and pr.property_id = b.property_id
  cross join params s
  where lower(b.status) in ('confirmed','checked_in','checked_out','closed','booked','reserved')
    and b.booked_at >= s.d28
),
plat as (
  select name, string_agg(plat || ' ' || c, ', ' order by c desc) as direct_platforms
  from (select name, plat, count(*) c from bk where is_direct group by name, plat) x
  group by name
)
select bk.name, max(bk.provider) as provider, max(bk.last_sync)::date as last_sync,
  count(*) filter (where is_direct) as direct28_bk,
  count(*) filter (where is_direct and not is_manual) as online28_bk,
  round(coalesce(sum(rev) filter (where is_direct),0)) as direct28_rev,
  count(*) filter (where is_direct and booked_at >= s.d7) as direct7_bk,
  count(*) filter (where is_direct and not is_manual and booked_at >= s.d7) as online7_bk,
  count(*) as all28_bk,
  max(plat.direct_platforms) as direct_platforms
from bk cross join params s left join plat on plat.name = bk.name
group by bk.name
order by bk.name;
