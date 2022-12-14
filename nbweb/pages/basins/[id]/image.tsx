import ImageScreen from 'component/screen/ImageScreen'
import { useRouter } from 'next/router'

export default function BasinImage() {
  const router = useRouter()
  const { id, blob } = router.query

  return <ImageScreen />
}
