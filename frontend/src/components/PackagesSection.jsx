import Reveal from './Reveal.jsx'

const menuItems = [
  ['Veg Briyani', '₹60'],
  ['Tomato Rice', '₹50'],
  ['Coriander Rice', '₹50'],
  ['Curd Rice', '₹50'],
  ['Lemon Rice', '₹50'],
  ['Tamarind Rice', '₹50'],
  ['Vada', '₹10'],
  ['Boiled Egg', '₹15'],
]

export default function PackagesSection() {
  return (
    <section className="section section--dark" id="menus">
      <div className="container">
        <div className="text-center mb-5 reveal in">
          <span className="eyebrow eyebrow--center">Daily menu</span>
          <h2 className="display-heading">Fresh favourites, <em>fair prices</em></h2>
          <p className="section-lead mx-auto text-center">Choose from our daily rice dishes and snacks.</p>
        </div>

        <div className="row justify-content-center">
          <div className="col-lg-8">
            <Reveal className="menu-panel in">
              <ul className="menu-list">
                {menuItems.map(([name, price]) => (
                  <li className="menu-item" key={name}>
                    <span className="menu-item__main"><span className="menu-item__name">{name}</span></span>
                    <span className="menu-item__leader" aria-hidden="true" />
                    <span className="menu-item__price">{price}</span>
                  </li>
                ))}
              </ul>
              <div className="menu-panel__head text-center mt-4">
                <p className="menu-panel__price-note">Order services</p>
                <p>Veg &amp; Non-Veg Full Meals</p>
                <p>Contact us for booking &amp; bulk orders.</p>
                <a className="btn btn-amutham mt-3" href="/quote">Contact us to order</a>
              </div>
            </Reveal>
          </div>
        </div>
      </div>
    </section>
  )
}
