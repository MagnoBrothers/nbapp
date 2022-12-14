import { useRouter } from 'next/router'
import DownloadIcon from '../icons/DownloadIcon'

interface PathElement {
  name: string
  targetUrl: string
}

type Props = { isValidating: boolean }

function Breadcrumbs({ isValidating }: Props) {
  const router = useRouter()

  const pathElements = router.asPath
    .split('/')
    .slice(1)
    .map((el, index, arr): PathElement => {
      const isQueryArgs = el.includes('?')

      return {
        name: isQueryArgs ? el.slice(0, el.indexOf('?')) : el,
        targetUrl: '/' + arr.slice(0, index + 1).join('/'),
      }
    })

  return (
    <div className="flex items-center px-4 text-sm breadcrumbs">
      <ul>
        {pathElements.map((elem: PathElement, index: number) => {
          return (
            <li
              key={index}
              onClick={() => {
                router.push(elem.targetUrl)
              }}
            >
              <a
                onClick={() => {
                  router.push(elem.targetUrl)
                }}
              >
                {elem.name.length > 8
                  ? `${elem.name.slice(0, 8)}...`
                  : elem.name}
              </a>
            </li>
          )
        })}
      </ul>
      {isValidating && (
        <div className="pl-3">
          <DownloadIcon />
        </div>
      )}
    </div>
  )
}

export default Breadcrumbs
