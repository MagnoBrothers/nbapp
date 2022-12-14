import React from 'react'
import useBasinsList from '../../hooks/useBasinsList'
import ListItem from './ListItem'

type Props = {}

function List({}: Props) {
  const { jobList, error } = useBasinsList()

  if (error) return <div>error: {JSON.stringify(error)}</div>

  const isLoading = Boolean(!jobList)
  if (isLoading) return <ListLoading />

  return (
    <div className="w-full max-w-4xl">
      {jobList.data.map((job, index) => {
        return (
          <div key={index} className="pb-2">
            <ListItem job={job} isLoading={false} />
          </div>
        )
      })}
    </div>
  )
}

function ListLoading() {
  return (
    <div className="w-full max-w-4xl">
      {Array(5)
        .fill('')
        .map((job, index) => {
          return (
            <div key={index} className="pb-2">
              <ListItem job={job} isLoading={true} />
            </div>
          )
        })}
    </div>
  )
}

export default List
