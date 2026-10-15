import type { NextConfig } from "next";

// On Netlify (NETLIFY=true), produce a static export.
// Locally, leave output unset so API routes work in `next dev`.
const isNetlify = process.env.NETLIFY === 'true' || process.env.NETLIFY === '1';

const nextConfig: NextConfig = {
  ...(isNetlify ? { output: "export" } : {}),
  trailingSlash: true,
  // Dev only: the weekly archive in public/weekly is plain static HTML. Netlify
  // resolves /weekly/ -> index.html and the latest-page redirects live in
  // netlify.toml, but `next dev` serves public/ files only by exact path, so
  // mirror both here. Rewrites are not allowed with output: "export".
  ...(isNetlify
    ? {}
    : {
        async rewrites() {
          return [
            { source: "/weekly", destination: "/weekly/index.html" },
            {
              source: "/weekly/:slug(ad-spend|pixel-domains|client-benchmark)",
              destination: "/weekly/:slug/latest.html",
            },
          ];
        },
      }),
};

export default nextConfig;
