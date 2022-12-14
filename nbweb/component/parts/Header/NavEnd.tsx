import { Fragment } from 'react'
import MenuButton from './MenuButton'
import cls from 'classnames'
import ListIcon from '../icons/ListIcon'
import LogoIcon from '../icons/LogoIcon'
import PlusIcon from '../icons/PlusIcon'
import { useRouter } from 'next/router'

type Props = { activeIndex?: number }

export default function NavEnd(props: Props) {
  const { activeIndex = 2 } = props

  const router = useRouter()

  const listItems = [
    {
      text: '',
      icon: <LogoIcon />,
      url: '/',
    },
    {
      text: 'list',
      icon: <ListIcon />,
      url: '/basins',
    },
    {
      text: 'create',
      icon: <PlusIcon />,
      url: '/basins/create',
    },
  ]

  return (
    <Fragment>
      {/* <div className="navbar-end md:hidden"> */}
      <div className="md:hidden">
        <div className="dropdown dropdown-end">
          <MenuButton />
          {/* dropdown menu */}
          <ul
            tabIndex={0}
            className="w-40 border-2 border-primary menu bg-base-200 dropdown-content"
          >
            {listItems.map((item, index) => {
              return (
                <li
                  key={index}
                  className={cls({
                    bordered: activeIndex == index,
                  })}
                  tabIndex={0}
                  onClick={() => {
                    router.push(item.url)
                  }}
                >
                  <a>
                    {item.icon}
                    {item.text}
                  </a>
                </li>
              )
            })}
          </ul>
        </div>
      </div>

      {/* buttons */}
      {/* <div className="navbar-end max-md:hidden"> */}
      <div className="flex flex-row max-md:hidden">
        {listItems.map((item, index) => {
          if (item.text) {
            return (
              <div
                key={index}
                className={cls(
                  'px-4 py-2 text-sm hover:underline bg-base-100 hover:cursor-pointer',
                  {
                    underline: activeIndex == index,
                  },
                )}
                onClick={() => {
                  router.push(item.url)
                }}
              >
                {item.text}
              </div>
            )
          }
        })}
      </div>
    </Fragment>
  )
}
