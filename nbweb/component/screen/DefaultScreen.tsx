import Image from 'next/image'
import React from 'react'
import Base from '../parts/Base'

type Props = {}

function DefaultScreen({}: Props) {
  return (
    <Base title="404 not found">
      <main className="relative h-screen bg-base-300">
        <Image alt="404 not found" src="/404.svg" fill />
      </main>
    </Base>
  )
}

export default DefaultScreen
