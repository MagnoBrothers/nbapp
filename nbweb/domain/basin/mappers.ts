import {
  Basin as BasinClient,
  Job as JobClient,
  JobListResp as JobListRespClient,
} from '../../tools/client/interface'
import { Basin, Job, JobListResp } from './interface'

function mapClientBasinToBasin(basinClient: BasinClient): Basin {
  const basin: Basin = {
    name: basinClient?.name,
    cimax: basinClient.cimax,
    cimin: basinClient.cimin,
    crmax: basinClient.crmax,
    crmin: basinClient.crmin,
    coefs: basinClient.coefs,
    imw: basinClient.imw,
    imh: basinClient.imh,
    itmax: basinClient.itmax,
    tol: basinClient.tol,
    imageUrl: basinClient.image_url,
    thumbnailUrl: basinClient.thumbnail_url,
  }
  return basin
}

function mapClientJobToJob(jobClient: JobClient): Job {
  const job: Job = {
    id: jobClient.id,
    basin: mapClientBasinToBasin(jobClient.basin),
    progress: jobClient.progress,
    status: jobClient.status,
    date: jobClient.date,
  }
  return job
}

function mapClientJobListToJobList(
  jobListRespClient: JobListRespClient,
): JobListResp | undefined {
  if (!jobListRespClient) return undefined

  const jobListResp: JobListResp = {
    total: jobListRespClient.total,
    data: jobListRespClient.data.map(mapClientJobToJob),
  }
  return jobListResp
}

export { mapClientBasinToBasin, mapClientJobToJob, mapClientJobListToJobList }
