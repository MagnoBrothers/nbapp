import { Roboto } from '@next/font/google'
import { useRouter } from 'next/router'
import { motion } from 'framer-motion'
import cls from 'classnames'
import Image from 'next/image'
import Base from '../parts/Base'

const roboto = Roboto({
  weight: '500',
})

export default function SplashScreen(props: any) {
  const { nextPage = '/basins' } = props
  const router = useRouter()

  const goToNextPage = (e: any) => {
    e.preventDefault()
    router.push(nextPage)
  }

  return (
    <Base title="Newton basins">
      <main
        className={cls([
          'flex',
          // 'items-center',
          'justify-left',
          'items-end',
          'h-screen',
          // 'bg-basins-primary',
          // 'pt-40',
        ])}
        onClick={goToNextPage}
      >
        <Image
          alt="splash logo"
          src="/splash_logo.svg"
          width={700}
          height={700}
        />
        <article
          className="absolute pb-10 pl-10 prose md:right-1/4 md:top-3/4 md:prose-2xl"
          style={roboto.style}
        >
          <motion.div
            className="box"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{
              duration: 2,
            }}
          >
            <h1 className="text-gray-500 select-none text-hero">
              Newton Basins
            </h1>
          </motion.div>
          <motion.div
            className="box"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{
              duration: 2,
              delay: 1,
            }}
          >
            <p className="text-xl text-gray-500 select-none">by MagnoBros</p>
          </motion.div>
        </article>
      </main>
    </Base>
  )
}
