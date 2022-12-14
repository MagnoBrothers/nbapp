import Image from 'next/image'
import { useRouter } from 'next/router'
import { env } from 'tools/env'
import Base from '../parts/Base'
import ChevronIcon from '../parts/icons/ChevronIcon'

export default function ImageScreen() {
  const router = useRouter()

  const title = `image: ${router.query.id}`

  return (
    <Base title={title}>
      <div className="relative h-screen">
        {router.query.id && (
          <Image
            src={[
              env.NEXT_PUBLIC_HTTP_PROTOCOL,
              ':',
              env.NEXT_PUBLIC_MINIO_HOSTNAME,
              ':',
              env.NEXT_PUBLIC_MINIO_PORT,
              '/basins/main_',
              router.query.id,
              '.png',
            ].join('')}
            alt={`basin image`}
            fill
          />
        )}
      </div>
      <div className="fixed top-4 left-4">
        <button
          className="opacity-40 btn hover:bg-gray-600"
          onClick={() => {
            router.push(`/basins/${router.query.id}`)
          }}
        >
          <ChevronIcon pointing="left" />
        </button>
      </div>
    </Base>
  )
}
