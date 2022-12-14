import cls from 'classnames'
import { Job } from 'domain/basin/interface'
import React from 'react'
import CheckedIcon from '../../icons/CheckedIcon'

type Props = { job: Job }

function Progress({ job }: Props) {
  return (
    <div
      className={cls([
        'radial-progress',
        {
          'text-success': job.progress === 100,
          'text-info': job.progress !== 100,
        },
      ])}
      style={{
        '--value': `${job.progress}`,
        '--size': '4rem',
        '--thickness': '6px',
      }}
    >
      {/* <div className="text-sm">{`${job.progress}%`}</div> */}
      <div className="text-sm">
        {job.progress === 100 ? <CheckedIcon /> : `${job.progress}%`}
      </div>
    </div>
  )
}

export default Progress
