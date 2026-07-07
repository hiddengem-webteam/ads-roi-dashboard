import { ProcessedData } from '@/types';
import { processAllData, UploadedFilesMap } from './processor';

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

export interface Manifest {
  periods: ManifestPeriod[];
}

async function urlToFile(url: string): Promise<File> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch ${url}: ${res.status}`);
  const blob = await res.blob();
  const filename = url.split('/').pop() ?? 'data.csv';
  return new File([blob], filename, { type: 'text/csv' });
}

export async function loadManifest(): Promise<Manifest> {
  const res = await fetch('/data/manifest.json');
  if (!res.ok) throw new Error('Could not load data manifest');
  return res.json();
}

export async function loadPeriod(period: ManifestPeriod): Promise<ProcessedData> {
  const files: UploadedFilesMap = {
    metaAds: null,
    promoCodes: null,
    pmsFiles: {},
    ghlFiles: {},
  };

  const fetches: Promise<void>[] = [];

  if (period.metaAds) {
    fetches.push(urlToFile(period.metaAds).then((f) => { files.metaAds = f; }));
  }
  if (period.promoCodes) {
    fetches.push(urlToFile(period.promoCodes).then((f) => { files.promoCodes = f; }));
  }
  for (const client of period.clients) {
    if (client.pms) {
      fetches.push(urlToFile(client.pms).then((f) => { files.pmsFiles[client.name] = f; }));
    }
    if (client.ghl) {
      fetches.push(urlToFile(client.ghl).then((f) => { files.ghlFiles[client.name] = f; }));
    }
  }

  await Promise.all(fetches);
  return processAllData(files);
}
