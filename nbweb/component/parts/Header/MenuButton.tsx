import MenuIcon from '../icons/MenuIcon'

type Props = {}

function MenuButton({}: Props) {
  return (
    <label tabIndex={0} className="btn btn-ghost btn-circle">
      <MenuIcon />
    </label>
  )
}

export default MenuButton
