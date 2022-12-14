import { env } from '../../tools/env'

// const API_BASE_URL = 'http://api:9000/api/v1'
const API_BASE_URL = `${env.NEXT_PUBLIC_HTTP_PROTOCOL}://${env.NEXT_PUBLIC_API_HOSTNAME}:${env.NEXT_PUBLIC_API_PORT}/api/v1`

// const API_BASE_URL = `${env.NEXT_PUBLIC_HTTP_PROTOCOL}://${env.NEXT_PUBLIC_API_HOSTNAME}:${env.NEXT_PUBLIC_API_PORT}/api/v1`
const REFRESH_INTERVAL = env.NEXT_PUBLIC_REFRESH_INTERVAL

// const API_BASE_URL = `http://${process.env.NEXT_PUBLIC_API_HOSTNAME}:${process.env.NEXT_PUBLIC_API_PORT}/api/v1`
// const REFRESH_INTERVAL = process.env.NEXT_PUBLIC_REFRESH_INTERVAL

const API_JOBS_URL = `${API_BASE_URL}/jobs`

export { API_BASE_URL, API_JOBS_URL, REFRESH_INTERVAL }
