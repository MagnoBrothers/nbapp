import useBasinsList from '../hooks/useBasinsList'
import Base from '../parts/Base'
import Footer from '../parts/Footer'
import Header from '../parts/Header'
import ListMain from '../parts/ListMain'

export default function BasinsListScreen() {
  const { isValidating } = useBasinsList()

  return (
    <Base title="basins list">
      <div className="flex flex-col items-center">
        <Header activeIndex={1} isValidating={isValidating} />
        <ListMain />
        <Footer />
      </div>
    </Base>
  )
}
