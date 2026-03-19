import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Required for the multi-stage Docker build (copies .next/standalone)
  output: "standalone",
  images: {
    // CarSensor serves images from these domains
    remotePatterns: [
      { protocol: "https", hostname: "**.carsensor.net" },
      { protocol: "https", hostname: "**.ccsrpcma.carsensor.net" },
      { protocol: "https", hostname: "example.com" },
    ],
  },
};

export default nextConfig;
