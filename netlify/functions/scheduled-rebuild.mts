// Netlify scheduled function — keeps the deployed dashboard current.
//
// Every 4 hours it POSTs to this site's build hook, which triggers a fresh
// production build. The build's `prebuild` step (scripts/sync-all.mts) re-pulls
// the latest platform data and bakes it into the new static deploy.
//
// Fires at :30 past every 4th hour — 30 min after the platform's own :00
// Meta / PMS / GHL syncs, so their fresh data is already in Supabase.
//
// Setup: create a build hook (Netlify → Site configuration → Build & deploy →
// Build hooks) and set its URL as the BUILD_HOOK_URL environment variable.
// No infinite-loop risk: a build does not re-invoke this function — only the
// cron schedule does.

export default async function handler() {
  const hook = process.env.BUILD_HOOK_URL;
  if (!hook) {
    console.error('[scheduled-rebuild] BUILD_HOOK_URL not set — skipping');
    return;
  }
  try {
    const res = await fetch(hook, { method: 'POST' });
    console.log(`[scheduled-rebuild] build hook POST → ${res.status}`);
  } catch (err) {
    console.error('[scheduled-rebuild] failed to trigger build:', err);
  }
}

export const config = {
  schedule: '30 */4 * * *', // every 4 hours, 30 min past the hour
};
