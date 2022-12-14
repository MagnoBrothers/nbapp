import {} from 'react'
import useBasinsDetail from '../hooks/useBasinsDetail'
import Base from '../parts/Base'
import DetailMain from '../parts/DetailMain'
import Footer from '../parts/Footer'
import Header from '../parts/Header'

export default function BasinsDetailScreen() {
  const { job, error, isValidating } = useBasinsDetail()

  let title = 'basins detail'
  if (job) title = `basin: ${job.id}`

  return (
    <Base title={title}>
      <div className="flex flex-col items-center">
        <Header activeIndex={-1} isValidating={isValidating} />
        <DetailMain />
        <Footer />
      </div>
    </Base>
  )
}
