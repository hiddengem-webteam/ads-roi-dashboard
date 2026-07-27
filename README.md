This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

## HiddenGem AI platform data (automatic)

The dashboard renders from `public/data/manifest.json` + per-period CSVs. These
are pulled from the HiddenGem AI platform **automatically** — the `sync-all`
script runs before `next dev` and before `next build` (via the `predev` /
`prebuild` npm hooks), so the dashboard is always populated with no manual step.
The generated files contain client PII and are git-ignored; each build/deploy
regenerates them fresh.

### Setup

`cp .env.example .env.local` and set:

- `HG_PLATFORM_URL` — the platform's base URL (e.g. `https://hiddengem-ai.netlify.app`)
- `HG_CRON_SECRET` — the platform's agency `CRON_SECRET` (server-only; never exposed to the browser)

Then just `npm run dev`. For production, set the same two vars in the Netlify
build environment — `prebuild` bakes every month into the static export.

If the two vars aren't set, the sync is skipped with a warning so dev/build never
breaks. `npm run sync` runs it on demand.

### What the sync does

Walks months newest→oldest and pulls each into its own period. It's incremental:
the newest 2 months are always refreshed; older months already synced are skipped
(fast repeat runs). It auto-discovers how far back to go — stopping after 3
consecutive empty months, capped at 36. Env knobs (all optional):

| Var | Effect |
| --- | --- |
| `HG_SYNC_FORCE=1` | re-sync every month (ignore what's already synced) |
| `HG_SYNC_STRICT=1` | exit non-zero if the sync errors (fail the build) |
| `HG_SYNC_MAX_MONTHS=N` | how far back to look (default 36) |
| `HG_SYNC_REFRESH_MONTHS=N` | always re-sync the newest N months (default 2) |

### What it pulls (and what it doesn't)

Pulled from the platform (`GET /api/v1/clients`, `/api/v1/admin/roi-export`,
`/api/v1/clients/[id]/contacts`, authenticated with `HG_CRON_SECRET`):

| Dashboard input | Source | Notes |
| --- | --- | --- |
| Meta Ads | `roi-export` campaigns | full: spend / impressions / link clicks / leads / purchases / value |
| PMS (direct bookings) | `roi-export` direct_bookings | guest, email, revenue, check-in only — no coupon / listing / checkout / source |
| GHL leads | client contacts | id, name, phone, email, created, tags (name is one field; tags in `role`) |
| Promo codes | **not available** | keep a `Promo codes.csv` in the period's `shared/` dir to enable promo attribution (hybrid) |

Because promo codes and PMS coupon fields aren't stored on the platform, the
promo-attribution section stays empty unless you provide a `Promo codes.csv`
manually. Everything else (ad stats, lead matching, revenue summary) fills
automatically.

> The Google Drive **Sync Month** panel (bottom-right, localhost only) still
> exists as an alternative source and writes the same files.

### Keeping production current (scheduled rebuilds)

The deployed dashboard is a static snapshot from its last build. To refresh it on
the platform's 4-hour cadence, a Netlify scheduled function
([`netlify/functions/scheduled-rebuild.mts`](netlify/functions/scheduled-rebuild.mts))
POSTs a build hook every 4 hours, triggering a rebuild — which re-runs `prebuild`
→ the sync → a fresh deploy.

One-time setup in Netlify:

1. **Site configuration → Build & deploy → Build hooks → Add build hook**
   (branch: `main`). Copy the URL.
2. **Site configuration → Environment variables** → add:
   - `BUILD_HOOK_URL` — the hook URL from step 1
   - `HG_PLATFORM_URL` and `HG_CRON_SECRET` — so the build's sync can pull
3. Deploy once. The function then fires at **:30 past every 4th hour (UTC)** —
   ~30 min after the platform's `:00` Meta/PMS/GHL syncs land. Change the cadence
   via the `schedule` cron in the function file.

There's no infinite-loop risk: a build does not re-invoke the function; only the
cron does.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
