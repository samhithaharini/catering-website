import { useRef, useState } from 'react'

const menuStyles = [
  {
    id: 'daily',
    name: 'Daily Menu',
    orderService: 'Veg & Non-Veg Full Meals',
    orderContact: 'Contact for Booking & Bulk Orders',
    items: [
      ['Veg Briyani', '₹60'],
      ['Tomato Rice', '₹50'],
      ['Coriander Rice', '₹50'],
      ['Curd Rice', '₹50'],
      ['Lemon Rice', '₹50'],
      ['Tamarind Rice', '₹50'],
      ['Vada', '₹10'],
      ['Boiled Egg', '₹15'],
    ],
  },
]

export default function MenuTabs({ fullPage = false }) {
  const [active, setActive] = useState(0)
  const tabsRef = useRef([])

  function handleKeyDown(event, index) {
    let next = index
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % menuStyles.length
    if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + menuStyles.length) % menuStyles.length
    if (next !== index) {
      event.preventDefault()
      setActive(next)
      tabsRef.current[next]?.focus()
    }
  }

  return (
    <>
      <div className="menu-tabs reveal reveal--d1 in" role="tablist" aria-label={fullPage ? 'Menu' : 'Daily menu'}>
        {menuStyles.map((menu, index) => (
          <button
            className="menu-tab"
            type="button"
            role="tab"
            id={`${fullPage ? 'full-' : ''}tab-${menu.id}`}
            aria-controls={`${fullPage ? 'full-' : ''}panel-${menu.id}`}
            aria-selected={active === index}
            tabIndex={active === index ? 0 : -1}
            key={menu.id}
            ref={(element) => { tabsRef.current[index] = element }}
            onClick={() => setActive(index)}
            onKeyDown={(event) => handleKeyDown(event, index)}
          >{menu.name}</button>
        ))}
      </div>
      <div className="row justify-content-center">
        <div className="col-lg-9">
          {menuStyles.map((menu, index) => (
            <div
              className={`menu-panel reveal${active === index ? ' in' : ''}`}
              role="tabpanel"
              id={`${fullPage ? 'full-' : ''}panel-${menu.id}`}
              aria-labelledby={`${fullPage ? 'full-' : ''}tab-${menu.id}`}
              key={menu.id}
              hidden={active !== index}
              tabIndex={0}
            >
              <ul className="menu-list">
                {menu.items.map(([name, price]) => (
                  <li className="menu-item" key={name}>
                    <span className="menu-item__main">
                      <span className="menu-item__name">{name}</span>
                    </span>
                    <span className="menu-item__leader" aria-hidden="true" />
                    <span className="menu-item__price">{price}</span>
                  </li>
                ))}
              </ul>
              <div className="menu-panel__head text-center mt-4">
                <p className="menu-panel__price-note">Order Services</p>
                <p>{menu.orderService}</p>
                <p>{menu.orderContact}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  )
}
