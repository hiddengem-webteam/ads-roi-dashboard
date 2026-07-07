import { google } from 'googleapis';
import type { JWT } from 'google-auth-library';
import fs from 'fs';
import path from 'path';

const SCOPES = [
  'https://www.googleapis.com/auth/drive.readonly',
  'https://www.googleapis.com/auth/spreadsheets.readonly',
];

export function getAuth(): JWT {
  const saPath = process.env.GOOGLE_SERVICE_ACCOUNT_PATH;
  if (!saPath) {
    throw new Error('GOOGLE_SERVICE_ACCOUNT_PATH env var is not set');
  }
  const resolved = path.resolve(process.cwd(), saPath);
  if (!fs.existsSync(resolved)) {
    throw new Error(`Service account file not found at: ${resolved}`);
  }
  const key = JSON.parse(fs.readFileSync(resolved, 'utf8'));
  return new google.auth.JWT({
    email: key.client_email,
    key: key.private_key,
    scopes: SCOPES,
  });
}

export function getDriveClient(auth: JWT) {
  return google.drive({ version: 'v3', auth });
}

export function getSheetsClient(auth: JWT) {
  return google.sheets({ version: 'v4', auth });
}
