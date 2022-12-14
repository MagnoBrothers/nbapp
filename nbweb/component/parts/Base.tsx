import Head from 'next/head'
import React, { Fragment, ReactNode } from 'react'

type Props = {
  title: string
  children: ReactNode
}

const numFavicons = 19

function Base({ title, children }: Props) {
  const faviconIndex = `${Math.floor(Math.random() * numFavicons)}`

  return (
    <Fragment>
      <Head>
        <title>{title}</title>
        <link rel="icon" href={`/favicons/f${faviconIndex}.ico`} />
      </Head>
      {children}
    </Fragment>
  )
}

export default Base
