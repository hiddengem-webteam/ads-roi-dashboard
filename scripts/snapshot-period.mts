// One-off snapshot generator: runs the REAL production parsing/analysis
// pipeline (the same processAllData() the live dashboard uses) against a
// period's already-synced CSVs, and freezes the result as static JSON.
//
// Usage: npx tsx scripts/snapshot-period.mts july-2026
//
// Why this exists: the /july route is a frozen reference view, hardcoded
// now on purpose so it doesn't drift while we keep iterating on the live
// dashboard's logic. Generating it by re-running the real analysis code
// (rather than hand-typing numbers) keeps that freeze accurate.

import fs from 'fs';
import path from 'path';
import { processAllData, UploadedFilesMap } from '../src/lib/analysis/processor';

// Papa.parse requires a browser FileReader when given a File/Blob input.
// Node has global File/Blob (v20+) but no FileReader — polyfill just enough
// of it (readAsText via Blob.text()) so the real parser functions work as-is.
class NodeFileReader {
  onload: ((ev: { target: { result: string } }) => void) | null = null;
  onerror: ((err: unknown) => void) | null = null;
  result: string | null = null;
  readAsText(blob: Blob) {
    blob.text().then((text) => {
      this.result = text;
      this.onload?.({ target: { result: text } });
    }).catch((err) => this.onerror?.(err));
  }
}
// @ts-expect-error - Node has no FileReader; this polyfill is sufficient for Papa.parse's FileStreamer path.
globalThis.FileReader = NodeFileReader;

interface ManifestClient {
  name: string;
  pms?: string;
  ghl?: string;
}
interface ManifestPeriod {
  id: string;
  label: string;
  metaAds?: string;
  promoCodes?: string;
  clients: ManifestClient[];
}
interface Manifest {
  periods: ManifestPeriod[];
}

const ROOT = path.resolve(import.meta.dirname, '..');

function readAsFile(publicPath: string): File {
  const abs = path.join(ROOT, 'public', publicPath);
  const buf = fs.readFileSync(abs);
  const filename = publicPath.split('/').pop() ?? 'data.csv';
  return new File([buf], filename, { type: 'text/csv' });
}

async function main() {
  const periodId = process.argv[2];
  if (!periodId) {
    console.error('Usage: npx tsx scripts/snapshot-period.mts <period-id>');
    process.exit(1);
  }

  const manifest: Manifest = JSON.parse(
    fs.readFileSync(path.join(ROOT, 'public', 'data', 'manifest.json'), 'utf8'),
  );
  const period = manifest.periods.find((p) => p.id === periodId);
  if (!period) {
    console.error(`Period "${periodId}" not found in manifest.json. Available: ${manifest.periods.map((p) => p.id).join(', ')}`);
    process.exit(1);
  }

  const files: UploadedFilesMap = { metaAds: null, promoCodes: null, pmsFiles: {}, ghlFiles: {} };
  if (period.metaAds) files.metaAds = readAsFile(period.metaAds);
  if (period.promoCodes) files.promoCodes = readAsFile(period.promoCodes);
  for (const client of period.clients) {
    if (client.pms) files.pmsFiles[client.name] = readAsFile(client.pms);
    if (client.ghl) files.ghlFiles[client.name] = readAsFile(client.ghl);
  }

  console.log(`Processing ${periodId} (${period.clients.length} manifest clients)...`);
  const data = await processAllData(files);
  console.log(`Done — ${Object.keys(data.clients).length} clients with data, ${data.flags.length} flags.`);

  const outDir = path.join(ROOT, 'public', 'data', 'snapshots');
  fs.mkdirSync(outDir, { recursive: true });
  const outPath = path.join(outDir, `${periodId}.json`);
  fs.writeFileSync(outPath, JSON.stringify({ period, data }, null, 2), 'utf8');
  console.log(`Wrote ${outPath}`);
}

main().catch((err) => {
  console.error('Snapshot failed:', err);
  process.exit(1);
});
