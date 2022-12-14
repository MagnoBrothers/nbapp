interface ListJobsArgs {
  url: string
  args: {
    user: string
    skip: string
    limit: string
  }
}

interface RetrieveJobArgs {
  url: string
  args: {
    user: string
    jobId: string
  }
}

interface Basin {
  name: string
  imw: number
  imh: number
  coefs: string
  crmin: number
  crmax: number
  cimin: number
  cimax: number
  itmax: number
  tol: number
  image_url: string
  thumbnail_url: string
}

interface Job {
  id: string
  basin: Basin
  status: 'running' | 'done' | 'failed' | 'pending'
  progress: number
  date: Date
}

interface JobListResp {
  total: number
  data: Job[]
}

export { ListJobsArgs, RetrieveJobArgs, CreateJob, Job, Basin, JobListResp }
