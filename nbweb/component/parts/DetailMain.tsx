import cn from 'classnames'
import moment from 'moment'
import Image from 'next/image'
import { useRouter } from 'next/router'
import React from 'react'
import useBasinsDetail from '../hooks/useBasinsDetail'

type Props = {}

function DetailMain({}: Props) {
  const { job } = useBasinsDetail()
  const router = useRouter()

  if (!job) return <>loading...</>
  const params = [
    {
      name: 'name',
      value: job.basin.name,
    },
    {
      name: 'coefs',
      value: job.basin.coefs,
    },
    {
      name: 'imw',
      value: job.basin.imw,
    },
    {
      name: 'imh',
      value: job.basin.imh,
    },
    {
      name: 'crmin',
      value: job.basin.crmin,
    },
    {
      name: 'crmax',
      value: job.basin.crmax,
    },
    {
      name: 'cimin',
      value: job.basin.cimin,
    },
    {
      name: 'cimax',
      value: job.basin.cimax,
    },
    {
      name: 'itmax',
      value: job.basin.itmax,
    },
    {
      name: 'tol',
      value: job.basin.tol,
    },
    {
      name: 'progress',
      value: `${job.progress}%`,
    },
    {
      name: 'status',
      value: job.status,
    },
    {
      name: 'date',
      value: moment(job.date).format('YYYY/MM/DD, HH:mm:ss'),
    },
  ]

  return (
    <div className="flex justify-center w-full max-w-4xl">
      <div className="flex flex-col items-center w-full px-10 pt-20 pb-10 max-sm:justify-evenly sm:justify-evenly sm:items-start sm:flex-row bg-base-200">
        <div
          className=""
          onClick={() => {
            job.status === 'done' && router.push(`/basins/${job.id}/image`)
          }}
        >
          {job.basin.thumbnailUrl && (
            <Image
              alt="basin thumbnail"
              src={job.basin.thumbnailUrl}
              width={300}
              height={300}
              // className="max-w-sm border-4 rounded-lg shadow-2xl hover:border-accent hover:cursor-pointer"
              className={cn([
                'max-w-sm',
                'border-4',
                'rounded-lg',
                'shadow-2xl',
                {
                  'hover:border-accent': job.status === 'done',
                  'hover:cursor-pointer': job.status === 'done',
                },
              ])}
            />
          )}
        </div>
        <div className="flex flex-col items-start w-full max-sm:items-center sm:pl-5 max-sm:pt-5">
          <div className="pb-4 ">
            <h1 className="text-4xl font-bold break-all">{job.basin.name}</h1>
          </div>
          <div className="flex w-full">
            <div className="basis-1/3">
              {params.map((item, index) => {
                return (
                  <div key={index} className="font-bold">
                    {item.name}
                  </div>
                )
              })}
            </div>
            <div className="basis-2/3">
              {params.map((item, index) => {
                return <div key={index}>{item.value}</div>
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DetailMain
