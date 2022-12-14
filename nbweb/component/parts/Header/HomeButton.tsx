import { useRouter } from 'next/router'
import LogoIcon from '../icons/LogoIcon'

type Props = {}

function HomeButton({}: Props) {
  const router = useRouter()

  return (
    <button
      className="btn btn-circle btn-ghost"
      onClick={() => {
        router.push('/')
      }}
    >
      <LogoIcon />
    </button>
  )
}

export default HomeButton
