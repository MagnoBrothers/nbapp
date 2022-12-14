import { useRouter } from 'next/router'
import React from 'react'
import { Job } from '../../../domain/basin/interface'
import Card from './Card'

type Props = { job: Job; isLoading: boolean }

function ListItem({ job, isLoading }: Props) {
  const router = useRouter()

  return (
    <div
      className="max-w-4xl"
      onClick={() => {
        router.push(`/basins/${job.id}`)
      }}
    >
      {/* small screen */}
      <div className="sm:hidden">
        <Card job={job} isLoading={isLoading} />
      </div>
      {/* large screen */}
      <div className="max-sm:hidden">
        <Card job={job} isLoading={isLoading} />
      </div>
    </div>
  )
}

export default ListItem
