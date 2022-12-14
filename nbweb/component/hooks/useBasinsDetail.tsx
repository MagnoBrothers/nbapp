import { useRouter } from 'next/router'
import useSWR from 'swr'
import { API_JOBS_URL, listJobs, retrieveJob } from '../../tools/client'
import { REFRESH_INTERVAL } from '../../tools/client/constants'
import { Job } from '../../domain/basin/interface'
import { Job as JobClient } from '../../tools/client/interface'
import {
  mapClientJobListToJobList,
  mapClientJobToJob,
} from '../../domain/basin/mappers'

export type UseBasinsDetailHook = {
  job: Job | null
  error: Error | null
  isValidating: boolean
}

function useBasinsDetail(): UseBasinsDetailHook {
  const {
    query: { id },
    isReady,
  } = useRouter()

  const {
    data,
    error,
    isValidating = true,
  } = useSWR(
    { url: API_JOBS_URL, args: { user: 'user', jobId: id } },
    retrieveJob,
    { refreshInterval: REFRESH_INTERVAL },
  )

  const job = data ? (mapClientJobToJob(data as JobClient) as Job) : null
  return { job, error, isValidating }
}

export default useBasinsDetail
