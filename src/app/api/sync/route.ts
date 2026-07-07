import { NextRequest, NextResponse } from 'next/server';
import { syncPeriod } from '@/lib/sync/syncPeriod';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { folderId, label } = body as { folderId?: string; label?: string };

    if (!folderId || !label) {
      return NextResponse.json({ error: 'folderId and label are required' }, { status: 400 });
    }

    const result = await syncPeriod(folderId, label);
    return NextResponse.json(result);
  } catch (err) {
    console.error('[sync]', err);
    return NextResponse.json({ error: String(err) }, { status: 500 });
  }
}
