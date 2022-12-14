import Base from '../parts/Base'
import Footer from '../parts/Footer'
import Header from '../parts/Header'
import CreateMain from '../parts/CreateMain'

export default function BasinsCreateScreen() {
  return (
    <Base title="basin create">
      {/* container */}
      <div className="flex flex-col items-center">
        <Header activeIndex={2} isValidating={false} />
        <CreateMain />
        <Footer />
      </div>
    </Base>
  )
}
