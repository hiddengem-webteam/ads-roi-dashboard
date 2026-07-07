import type { NextConfig } from "next";

// On Netlify (NETLIFY=true), produce a static export.
// Locally, leave output unset so API routes work in `next dev`.
const isNetlify = process.env.NETLIFY === 'true' || process.env.NETLIFY === '1';

const nextConfig: NextConfig = {
  ...(isNetlify ? { output: "export" } : {}),
  trailingSlash: true,
};

export default nextConfig;
