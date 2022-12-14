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
  imageUrl: string
  thumbnailUrl: string
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

export { ResponseJson, Basin, Job, JobListResp, JobDetailResp }
