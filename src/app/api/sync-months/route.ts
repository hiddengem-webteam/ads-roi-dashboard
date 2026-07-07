export const dynamic = 'force-static';

import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import { getAuth, getDriveClient } from '@/lib/sync/driveClient';

function toPeriodId(label: string): string {
  return label.toLowerCase().replace(/\s+/g, '-');
}

function getExistingPeriodIds(): Set<string> {
  const manifestPath = path.join(process.cwd(), 'public', 'data', 'manifest.json');
  if (!fs.existsSync(manifestPath)) return new Set();
  try {
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    return new Set<string>((manifest.periods ?? []).map((p: { id: string }) => p.id));
  } catch {
    return new Set();
  }
}

// Parse a "Month YYYY" label into a sortable number (YYYYMM)
function labelToSortKey(label: string): number {
  const months: Record<string, number> = {
    january: 1, february: 2, march: 3, april: 4, may: 5, june: 6,
    july: 7, august: 8, september: 9, october: 10, november: 11, december: 12,
  };
  const parts = label.toLowerCase().split(/\s+/);
  const month = months[parts[0]] ?? 0;
  const year = parseInt(parts[1] ?? '0', 10);
  return year * 100 + month;
}

export async function GET() {
  try {
    const rootFolderId = process.env.DRIVE_ROOT_FOLDER_ID;
    if (!rootFolderId) {
      return NextResponse.json({ error: 'DRIVE_ROOT_FOLDER_ID env var not set' }, { status: 500 });
    }

    const auth = getAuth();
    const drive = getDriveClient(auth);

    // First verify we can see the root folder itself
    // supportsAllDrives=true handles both My Drive and Shared Drives
    let rootCheck;
    try {
      rootCheck = await drive.files.get({
        fileId: rootFolderId,
        fields: 'id, name',
        supportsAllDrives: true,
      });
    } catch (e) {
      return NextResponse.json({ error: `Cannot access root folder (${rootFolderId}): ${String(e)}` }, { status: 500 });
    }

    const res = await drive.files.list({
      q: `'${rootFolderId}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false`,
      fields: 'files(id, name)',
      pageSize: 100,
      supportsAllDrives: true,
      includeItemsFromAllDrives: true,
    });

    const existingIds = getExistingPeriodIds();
    const folders = res.data.files ?? [];

    console.log(`[sync-months] Root folder: "${rootCheck.data.name}" — found ${folders.length} subfolders`);

    const result = folders
      .filter((f) => f.id && f.name)
      .map((f) => ({
        folderId: f.id!,
        name: f.name!,
        periodId: toPeriodId(f.name!),
        alreadySynced: existingIds.has(toPeriodId(f.name!)),
      }))
      .sort((a, b) => labelToSortKey(b.name) - labelToSortKey(a.name));

    return NextResponse.json(result);
  } catch (err) {
    console.error('[sync-months]', err);
    return NextResponse.json({ error: String(err) }, { status: 500 });
  }
}
