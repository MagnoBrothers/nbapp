import { API_BASE_URL, API_JOBS_URL } from './constants'
import {
  ListJobsArgs,
  RetrieveJobArgs,
  Job,
  Basin,
  JobListResp,
} from './interface'

async function listJobs(listJobsArgs: ListJobsArgs): Promise<JobListResp> {
  const {
    url,
    args: { user, skip, limit },
  } = listJobsArgs

  const response = await fetch(
    url +
      '?' +
      new URLSearchParams({
        skip,
        limit,
      }),
  )
  const jobsResp = await response.json()
  return jobsResp
}

async function retrieveJob(
  retrieveJobArgs: RetrieveJobArgs,
): Promise<Job | null> {
  const {
    url,
    args: { user, jobId },
  } = retrieveJobArgs

  if (!jobId) return null

  const jobResponse = await fetch(url + '/' + jobId)
  const job = await jobResponse.json()

  return job
}

// async function getImageSrc(url: string) {
//   const imageResponse = await fetch(url)
//   const imageBlob = await imageResponse.blob()
//   const imageSrc = URL.createObjectURL(imageBlob)

//   return imageSrc
// }

async function createJob({
  basinName,
  imw,
  imh,
  coefs,
  crmin,
  crmax,
  cimin,
  cimax,
  itmax,
  tol,
}: any): Promise<Job> {
  const response = await fetch(API_JOBS_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      basin: {
        name: basinName,
        imw,
        imh,
        coefs,
        crmin,
        crmax,
        cimin,
        cimax,
        itmax,
        tol,
      },
    }),
  })
  const result = await response.json()
  // console.log(result)
  return result
}

export {
  API_BASE_URL,
  API_JOBS_URL,
  listJobs,
  retrieveJob,
  createJob,
  // getImageSrc,
}
