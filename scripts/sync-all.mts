// Automatic HiddenGem-platform sync — runs before `next dev` / `next build`
// (see the predev/prebuild scripts in package.json). Pulls every month with ad
// data into public/data so the dashboard is populated with no manual step.
//
// Incremental by default: always refreshes the newest few months and skips
// older months already synced. Env knobs (all optional):
//   HG_SYNC_FORCE=1          re-sync every month (ignore what's already synced)
//   HG_SYNC_STRICT=1         fail (exit 1) on any sync error, anywhere
//   HG_SYNC_MAX_MONTHS=N     how far back to look (default 36)
//   HG_SYNC_REFRESH_MONTHS=N always re-sync the newest N months (default 2)
//
// On CI (Netlify sets NETLIFY=true), missing credentials or a run that produces
// NO data FAILS the build — a data dashboard that deploys blank is worse than a
// red build; Netlify keeps the last good deploy live. Locally (no CI), those
// cases only warn so dev never breaks for someone without platform credentials.

import fs from 'fs';
import path from 'path';
import { syncAllPlatformPeriods } from '../src/lib/sync/syncPlatformPeriod';

// Load .env.local / .env (real env vars take precedence, like Next).
function loadEnvLocal(cwd: string) {
  for (const file of ['.env.local', '.env']) {
    const p = path.join(cwd, file);
    if (!fs.existsSync(p)) continue;
    for (const raw of fs.readFileSync(p, 'utf8').split('\n')) {
      const line = raw.trim();
      if (!line || line.startsWith('#')) continue;
      const eq = line.indexOf('=');
      if (eq === -1) continue;
      const key = line.slice(0, eq).trim().replace(/^export\s+/, '');
      let val = line.slice(eq + 1).trim();
      if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
        val = val.slice(1, -1);
      }
      if (!(key in process.env)) process.env[key] = val;
    }
  }
}

loadEnvLocal(process.cwd());

// Parse a numeric env var, ignoring non-numeric junk (NaN → undefined → default).
function numEnv(name: string): number | undefined {
  const raw = process.env[name];
  if (!raw) return undefined;
  const n = Number(raw);
  return Number.isFinite(n) ? n : undefined;
}

function manifestHasPeriods(cwd: string): boolean {
  try {
    const m = JSON.parse(fs.readFileSync(path.join(cwd, 'public', 'data', 'manifest.json'), 'utf8'));
    return Array.isArray(m.periods) && m.periods.length > 0;
  } catch {
    return false;
  }
}

const explicitStrict = process.env.HG_SYNC_STRICT === '1';
const isCI = process.env.NETLIFY === 'true' || process.env.CI === 'true';
const failOnNoData = explicitStrict || isCI;

async function main() {
  if (!process.env.HG_PLATFORM_URL || !process.env.HG_CRON_SECRET) {
    const msg = 'HG_PLATFORM_URL / HG_CRON_SECRET not set';
    if (failOnNoData) {
      console.error(`[sync-all] ${msg} — failing build (CI/strict). Set them in the Netlify site env.`);
      process.exitCode = 1;
    } else {
      console.warn(`[sync-all] ${msg} — skipping HiddenGem sync. Set them in .env.local to enable.`);
    }
    return;
  }

  console.log('[sync-all] Pulling months from HiddenGem platform...');
  const result = await syncAllPlatformPeriods({
    skipExisting: process.env.HG_SYNC_FORCE !== '1',
    maxMonths: numEnv('HG_SYNC_MAX_MONTHS'),
    refreshRecentMonths: numEnv('HG_SYNC_REFRESH_MONTHS'),
    onLog: (m) => console.log('  ' + m),
  });

  console.log(
    `[sync-all] Done — ${result.periodsSynced.length} synced, ${result.periodsSkipped.length} skipped, ${result.totalClients} client-period(s).`,
  );

  if (result.errors.length > 0) {
    console.warn(`[sync-all] ${result.errors.length} non-fatal error(s):`);
    for (const e of result.errors) console.warn('  - ' + e);
    if (explicitStrict) process.exitCode = 1; // only an explicit strict flag fails on partial errors
  }

  // Refuse to ship a blank dashboard on CI: credentials were present, so we
  // expected data. If none landed (platform down / empty), fail the build.
  if (!manifestHasPeriods(process.cwd())) {
    const msg = 'sync produced no periods — the dashboard would be empty';
    if (failOnNoData) {
      console.error(`[sync-all] ${msg} — failing build.`);
      process.exitCode = 1;
    } else {
      console.warn(`[sync-all] ${msg}.`);
    }
  }
}

main().catch((err) => {
  console.error('[sync-all] Sync failed:', err instanceof Error ? err.message : err);
  if (failOnNoData) process.exitCode = 1;
});
