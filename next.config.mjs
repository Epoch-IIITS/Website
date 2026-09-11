/** @type {import('next').NextConfig} */
const nextConfig = {
  // PDFKit loads its built-in font metrics and ICC profile relative to its own
  // package directory. Bundling it moves the runtime file and breaks those paths.
  serverExternalPackages: ["pdfkit"],
  eslint: {
    ignoreDuringBuilds: true,
  },
  images: {
    unoptimized: true,
  },
}

export default nextConfig
