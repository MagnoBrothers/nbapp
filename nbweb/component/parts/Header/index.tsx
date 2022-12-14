import Breadcrumbs from './Breadcrumbs'
import HomeButton from './HomeButton'
import NavEnd from './NavEnd'

type Props = {
  activeIndex: number
  isValidating: boolean
}

export default function Header({ activeIndex, isValidating }: Props) {
  return (
    <header className="z-50 flex justify-center w-full">
      <nav className="fixed w-full max-w-4xl shadow-md">
        <div className="navbar bg-base-100">
          {/* nav start */}
          <div className="flex-1">
            <HomeButton />
            <Breadcrumbs isValidating={isValidating} />
          </div>

          {/* nav end */}
          <div className="flex-none">
            <NavEnd activeIndex={activeIndex} />
          </div>
        </div>
      </nav>

      {/* dummy navbar to take space underneath the actual navbar */}
      <nav className="navbar" />
    </header>
  )
}
