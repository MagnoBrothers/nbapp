import '../styles/globals.css'
import type { AppProps } from 'next/app'
import cls from 'classnames'

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <div
      data-theme={cls([
        // 'forest',
        // 'light',
        // 'dark',
        'fantasy',
        // 'autumn',
        // 'dracula',
        // 'emerald',
        // 'lemonade',
      ])}
      // className="bg-base-200"
    >
      <Component {...pageProps} />
    </div>
  )
}

export default MyApp
