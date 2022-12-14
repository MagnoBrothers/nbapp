import { cleanEnv, str, port, host, num } from 'envalid'

const env = cleanEnv(
  {
    NODE_ENV: process.env.NODE_ENV,
    NEXT_PUBLIC_API_HOSTNAME: process.env.NEXT_PUBLIC_API_HOSTNAME,
    NEXT_PUBLIC_API_PORT: process.env.NEXT_PUBLIC_API_PORT,
    NEXT_PUBLIC_WEB_HOSTNAME: process.env.NEXT_PUBLIC_WEB_HOSTNAME,
    NEXT_PUBLIC_WEB_PORT: process.env.NEXT_PUBLIC_WEB_PORT,
    NEXT_PUBLIC_HTTP_PROTOCOL: process.env.NEXT_PUBLIC_HTTP_PROTOCOL,
    NEXT_PUBLIC_REFRESH_INTERVAL: process.env.NEXT_PUBLIC_REFRESH_INTERVAL,
    NEXT_PUBLIC_MINIO_HOSTNAME: process.env.NEXT_PUBLIC_MINIO_HOSTNAME,
    NEXT_PUBLIC_MINIO_PORT: process.env.NEXT_PUBLIC_MINIO_PORT,
  },
  {
    NODE_ENV: str({
      choices: ['development', 'test', 'production', 'staging'],
    }),
    NEXT_PUBLIC_API_HOSTNAME: host(),
    NEXT_PUBLIC_API_PORT: port(),
    NEXT_PUBLIC_WEB_HOSTNAME: host(),
    NEXT_PUBLIC_WEB_PORT: port(),
    NEXT_PUBLIC_HTTP_PROTOCOL: str({ choices: ['http', 'https'] }),
    NEXT_PUBLIC_REFRESH_INTERVAL: num(),
    NEXT_PUBLIC_MINIO_HOSTNAME: str(),
    NEXT_PUBLIC_MINIO_PORT: str(),
  },
)

export { env }
