import React from 'react'
import Pagination from './Pagination'
import List from './List'

type Props = {}

function ListMain({}: Props) {
  return (
    <div className="z-10 flex flex-col items-center w-full p-2">
      <List />
      <Pagination />
    </div>
  )
}

export default ListMain
