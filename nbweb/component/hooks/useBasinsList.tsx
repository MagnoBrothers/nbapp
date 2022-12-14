import { useRouter } from 'next/router'
import useSWR from 'swr'
import { API_JOBS_URL, listJobs } from '../../tools/client'
import { REFRESH_INTERVAL } from '../../tools/client/constants'
import { JobListResp } from '../../domain/basin/interface'
import { JobListResp as JobListRespClient } from '../../tools/client/interface'
import {
  mapClientJobListToJobList,
  mapClientJobToJob,
} from '../../domain/basin/mappers'

export type UseBasinsListHook = {
  skip: string
  limit: string
  jobList: JobListResp
  error: Error
  isValidating: boolean
}

function useBasinsList(): UseBasinsListHook {
  const router = useRouter()

  const { skip = '0', limit = '5' } = router.query
  const { data, error, isValidating } = useSWR(
    { url: API_JOBS_URL, args: { user: 'user', skip, limit } },
    listJobs,
    { refreshInterval: REFRESH_INTERVAL },
  )

  const jobList = mapClientJobListToJobList(
    data as JobListRespClient,
  ) as JobListResp

  return {
    skip: skip as string,
    limit: limit as string,
    jobList,
    error,
    isValidating,
  }
  // return [skip as string, limit as string, jobList, error, isValidating]
}

export default useBasinsList
