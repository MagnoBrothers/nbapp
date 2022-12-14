import cn from 'classnames'
import useBasinsList from 'component/hooks/useBasinsList'
import { useRouter } from 'next/router'
import React from 'react'
import ChevronIcon from '../icons/ChevronIcon'

type Props = {}

function Pagination({}: Props) {
  const router = useRouter()
  const { skip, limit, jobList } = useBasinsList()

  const isLoading = Boolean(!jobList)

  if (isLoading) return <PaginationLoading />

  const page = Math.floor(+skip / +limit) + 1
  const count = Math.ceil(+jobList.total / +limit)

  const changePageHandler = (newPage: number) => {
    router.push({
      pathname: '/basins',
      query: {
        skip: `${newPage * +limit - +limit}`,
        limit,
      },
    })
  }

  const isNextPageDisabled = page === count
  const isPrevPageDisabled = page === 1

  return (
    <div className="btn-group">
      <button
        className={cn(['btn', { 'btn-disabled': isPrevPageDisabled }])}
        onClick={() => {
          !isPrevPageDisabled && changePageHandler(page - 1)
        }}
      >
        <ChevronIcon pointing="left" />
      </button>
      <button className="btn btn-ghost">{page}</button>
      <button
        className={cn(['btn', { 'btn-disabled': isNextPageDisabled }])}
        onClick={() => {
          !isNextPageDisabled && changePageHandler(page + 1)
        }}
      >
        <ChevronIcon pointing="right" />
      </button>
    </div>
  )
}

function PaginationLoading() {
  return <div className="h-12 bg-gray-300 rounded-md w-36 animate-pulse"></div>
}

export default Pagination
