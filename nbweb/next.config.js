/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: [
      // 'picsum.photos',
      // 'api',
      // '127.0.0.1',
      'minio',
      // 'localhost'
    ],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    remotePatterns: [
      {
        protocol: 'http',
        hostname: '127.0.0.1',
        port: '53330',
        pathname: '/basins/**',
      },
      {
        protocol: 'http',
        hostname: 'minio',
        port: '9000',
        pathname: '/basins/**',
      },
      // {
      //   protocol: 'http',
      //   hostname: '127.0.0.1',
      //   port: '53330',
      //   pathname: '/basins/**',
      // },
    ],
  },
}

module.exports = nextConfig
