import Papa from 'papaparse';
import { PMSRow } from '@/types';
import {
  parseNumber,
  detectRevenueColumn,
  detectCouponColumn,
  detectEmailColumn,
  detectGuestColumn,
} from '@/lib/utils';

export interface PMSParseResult {
  rows: PMSRow[];
  headers: string[];
  revenueColumn: string;
  isNetIncome: boolean;
  hasCouponColumn: boolean;
  hasEmailColumn: boolean;
  hasSourceColumn: boolean;
}

/**
 * Detects a "Promo Code Usage" side table embedded in the same sheet as booking data.
 * Pattern: a column header like "Promo Code Usage", followed by a sub-header row
 * (Name | Surname | Promo Code) and then rows of promo code users.
 * Returns a map of normalized guest full name → promo code.
 */
function buildSideTableCodeMap(
  rawRows: Record<string, string>[],
  headers: string[],
): Map<string, string> {
  const map = new Map<string, string>();

  // Find a header column that looks like a promo code side-table marker
  const markerCol = headers.find((h) => {
    const norm = h.toLowerCase().replace(/\s+/g, '');
    return norm.includes('promocodeusage') || norm.includes('promocodes');
  });
  if (!markerCol) return map;

  // Scan rows to find the sub-header row (where markerCol value is "Name" / "First Name")
  let firstNameIdx = -1;
  let surnameIdx = -1;
  let promoCodeIdx = -1;
  let dataStartIdx = -1;

  for (let i = 0; i < rawRows.length; i++) {
    const raw = rawRows[i];
    const markerVal = (raw[markerCol] ?? '').trim().toLowerCase();
    const extra = ((raw as Record<string, unknown>)['__parsed_extra'] as string[] | undefined) ?? [];
    const allCols = [markerVal, ...extra.map((v) => (v ?? '').trim().toLowerCase())];

    if (markerVal === 'name' || markerVal === 'first name' || markerVal === 'first') {
      firstNameIdx = allCols.findIndex((v) => v === 'name' || v === 'first name' || v === 'first');
      surnameIdx = allCols.findIndex((v) => v === 'surname' || v === 'last name' || v === 'last');
      promoCodeIdx = allCols.findIndex((v) => v.includes('promo') || v === 'code');
      dataStartIdx = i + 1;
      break;
    }
  }

  if (promoCodeIdx === -1 || dataStartIdx === -1) return map;

  for (let i = dataStartIdx; i < rawRows.length; i++) {
    const raw = rawRows[i];
    const extra = ((raw as Record<string, unknown>)['__parsed_extra'] as string[] | undefined) ?? [];
    const allVals = [(raw[markerCol] ?? '').trim(), ...extra.map((v) => (v ?? '').trim())];

    const code = allVals[promoCodeIdx]?.trim();
    if (!code) continue;

    const firstName = firstNameIdx >= 0 ? (allVals[firstNameIdx] ?? '') : '';
    const surname = surnameIdx >= 0 ? (allVals[surnameIdx] ?? '') : '';
    const fullName = `${firstName} ${surname}`.trim().toLowerCase().replace(/\s+/g, ' ');
    if (fullName) map.set(fullName, code);
  }

  return map;
}

export async function parsePMSData(file: File): Promise<PMSParseResult> {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      transformHeader: (h) => h.trim().replace(/^﻿/, ''),
      complete: (results) => {
        const rawRows = results.data as Record<string, string>[];
        if (!rawRows.length) {
          resolve({
            rows: [],
            headers: [],
            revenueColumn: '',
            isNetIncome: false,
            hasCouponColumn: false,
            hasEmailColumn: false,
            hasSourceColumn: false,
          });
          return;
        }

        // Use meta.fields (the actual header row) instead of Object.keys(rawRows[0]),
        // because the first data row may have fewer columns than the header (e.g. no coupon code),
        // which would cause Object.keys to miss columns like 'COUPON CODE'.
        const headers: string[] = results.meta.fields ?? Object.keys(rawRows[0]);

        // Detect HTML content — file is not a proper CSV export
        const firstVal = Object.values(rawRows[0] ?? {})[0] as string ?? '';
        if (firstVal.startsWith('<') || firstVal.startsWith('**') || firstVal.includes('<a href')) {
          reject(new Error(`File appears to contain HTML or non-CSV content. Please export a plain CSV from your booking system.`));
          return;
        }

        const revResult = detectRevenueColumn(headers);
        if (!revResult) {
          reject(new Error(`Could not detect revenue column. Headers found: ${headers.join(', ')} — export may be in an unsupported format.`));
          return;
        }

        const couponCol = detectCouponColumn(headers);
        const emailCol = detectEmailColumn(headers);
        const guestCol = detectGuestColumn(headers);

        // Handle split First Name / Last Name columns when no single guest column found.
        // Handles both spaced ("First Name") and snake_case ("guest_first_name") variants.
        const firstNameCol = !guestCol
          ? headers.find((h) => {
              const l = h.toLowerCase().replace(/[_\s]/g, '');
              return l === 'firstname' || l === 'guestfirstname' || l === 'first';
            }) ?? null
          : null;
        const lastNameCol = !guestCol && firstNameCol
          ? headers.find((h) => {
              const l = h.toLowerCase().replace(/[_\s]/g, '');
              return l === 'lastname' || l === 'guestlastname' || l === 'surname' || l === 'last';
            }) ?? null
          : null;

        const discountCandidates = ['Coupon discount', 'coupon_discount', 'guest_discount', 'PromotionsTotal', 'Promotions Total', 'promotions_total', 'Discount Amount', 'discount', 'Discount'];
        const discountCol = discountCandidates.find((c) => headers.includes(c)) ??
          headers.find((h) => h.toLowerCase().replace(/_/g,' ').includes('discount') || h.toLowerCase().includes('promotionstotal') || h.toLowerCase().includes('promotions total')) ?? null;

        const checkInCandidates = ['Check-in date', 'Check In', 'Checkin', 'check_in', 'Arrival', 'check-in', 'booking_date', 'Booking Date', 'Reservation Date', 'DateCreated', 'Date Created', 'date_created', 'Booked'];
        const checkInCol = checkInCandidates.find((c) => headers.includes(c)) ??
          headers.find((h) => checkInCandidates.some((c) => h.toLowerCase() === c.toLowerCase())) ??
          headers.find((h) => {
            const l = h.toLowerCase().replace(/_/g,' ');
            // 'booked' covers "Booked on"/"Booked at"/"Date Booked"/"Booked Date"; 'creation date'
            // covers "Creation Date" (reversed word order from "Date Created"); 'reservation date'
            // catches case variants like "Reservation date" that the exact-match tier above misses.
            return (l.includes('check') && l.includes('in')) || l.includes('booking date') || l.includes('date created') || l.includes('creation date') || l.includes('booked') || l.includes('reservation date');
          }) ?? null;

        const checkOutCandidates = ['Check-out date', 'Check Out', 'Checkout', 'check_out', 'Departure', 'check-out'];
        const checkOutCol = checkOutCandidates.find((c) => headers.includes(c)) ??
          headers.find((h) => h.toLowerCase().includes('check') && h.toLowerCase().includes('out')) ?? null;

        const listingCandidates = ['Listing', 'listing', 'Property', 'Unit'];
        const listingCol = listingCandidates.find((c) => headers.includes(c)) ??
          headers.find((h) => h.toLowerCase().includes('listing') || h.toLowerCase().includes('property')) ?? null;

        const sourceCandidates = ['Source', 'source', 'Platform', 'platform', 'Channel', 'channel',
          'Booking Source', 'booking_source', 'OTA', 'Listing Source', 'Booked Via', 'booked_via'];
        const sourceCol = sourceCandidates.find((c) => headers.includes(c)) ??
          headers.find((h) => {
            const l = h.toLowerCase();
            return l === 'source' || l === 'platform' || l === 'channel' || l.includes('booking source');
          }) ?? null;

        // Filter out summary/grand-total rows: rows where the name is empty
        // (e.g. a total row at the bottom with an aggregated Grand Total value)
        const filteredRows = rawRows.filter((raw) => {
          if (guestCol) return (raw[guestCol] ?? '').trim() !== '';
          if (firstNameCol) return (raw[firstNameCol] ?? '').trim() !== '';
          return true;
        });
        const effectiveRows = filteredRows.length > 0 ? filteredRows : rawRows;

        // Detect side-table promo code pattern:
        // Some PMS exports have a separate "Promo Code Usage" table alongside the booking list
        // (e.g. columns G-I: Name | Surname | Promo Code). Build a name→code lookup from it.
        const sideTableCodeMap = !couponCol
          ? buildSideTableCodeMap(effectiveRows, headers)
          : new Map<string, string>();

        const rows: PMSRow[] = effectiveRows.map((raw) => {
          // Build guest name from single column or split first/last name
          const guest = guestCol
            ? (raw[guestCol] ?? '').trim()
            : firstNameCol
            ? `${(raw[firstNameCol] ?? '').trim()} ${lastNameCol ? (raw[lastNameCol] ?? '').trim() : ''}`.trim()
            : '';

          const rawCoupon = couponCol ? (raw[couponCol] ?? '').trim() : '';
          // Filter out non-code placeholder values
          const NOT_A_CODE = /^(no coupon|no promo|none|n\/a|na|not applicable|-+|0)$/i;
          let couponName = rawCoupon && !NOT_A_CODE.test(rawCoupon) ? rawCoupon.toUpperCase() : '';
          if (!couponName && sideTableCodeMap.size > 0) {
            const guestNameNorm = guest.toLowerCase().replace(/\s+/g, ' ');
            couponName = (sideTableCodeMap.get(guestNameNorm) ?? '').toUpperCase();
          }
          return {
            guest,
            email: emailCol ? (raw[emailCol] ?? '').trim() : '',
            couponName,
            couponDiscount: discountCol ? parseNumber(raw[discountCol]) : 0,
            revenue: parseNumber(raw[revResult.column]),
            checkIn: checkInCol ? (raw[checkInCol] ?? '').trim() : '',
            checkOut: checkOutCol ? (raw[checkOutCol] ?? '').trim() : '',
            listing: listingCol ? (raw[listingCol] ?? '').trim() : '',
            revenueColumnUsed: revResult.column,
            source: sourceCol ? (raw[sourceCol] ?? '').trim() : '',
          };
        });

        resolve({
          rows,
          headers,
          revenueColumn: revResult.column,
          isNetIncome: revResult.isNetIncome,
          hasCouponColumn: !!couponCol || sideTableCodeMap.size > 0,
          hasEmailColumn: !!emailCol,
          hasSourceColumn: !!sourceCol,
        });
      },
      error: reject,
    });
  });
}
