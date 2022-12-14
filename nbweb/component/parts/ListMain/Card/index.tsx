import cls from 'classnames'
import Image from 'next/image'
import React from 'react'
import { Job } from '../../../../domain/basin/interface'
import Progress from './Progress'
import moment from 'moment'

type Props = { job: Job; isLoading: boolean }

function Card({ job, isLoading }: Props) {
  if (isLoading) return <CardLoading />

  return (
    <div className="flex items-center h-40 p-4 border-2 rounded-lg border-primary text-primary-content drop-shadow-md hover:bg-base-300 active:bg-secondary-content">
      {/* left */}
      <div className="flex items-center justify-center flex-none w-1/6 h-full">
        {/* <HomeIcon /> */}
        {job.basin.thumbnailUrl && (
          <Image
            alt="basins image thumbnail"
            src={job.basin.thumbnailUrl}
            width={44}
            height={44}
            style={{
              borderRadius: '50%',
            }}
          />
        )}
      </div>

      {/* middle */}
      <div className="flex flex-col flex-auto h-full justify-evenly">
        <div className="">
          <p className="text-xs text-primary"></p>
        </div>
        <div className="text-xl font-bold text-primary">{job.basin.name}</div>
        <div
          className={cls([
            'badge',
            {
              'badge-success': job.status === 'done',
              'badge-info': job.status === 'running',
              'badge-error': job.status === 'failed',
              'badge-warning': job.status === 'pending',
            },
          ])}
        >
          {job.status}
        </div>
      </div>

      {/* right */}
      <div className="flex flex-col items-center flex-none w-2/6 h-full justify-evenly">
        <Progress job={job} />
        <div
          className="tooltip tooltip-accent tooltip-left"
          data-tip={moment(job.date).format('YYYY/MM/DD, HH:mm:ss')}
        >
          <div className="text-primary">{moment(job.date).fromNow()}</div>
        </div>
      </div>
    </div>
  )
}

export function CardLoading() {
  return <div className="w-full h-40 bg-gray-300 rounded-md animate-pulse" />
}

export default Card
