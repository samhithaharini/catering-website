import { useEffect, useState } from 'react'

export default function Navbar({ isMenusPage }) {
  const [menuOpen, setMenuOpen] = useState(false)
  const [solid, setSolid] = useState(window.scrollY > 40)

  useEffect(() => {
    const update = () => setSolid(window.scrollY > 40)
    window.addEventListener('scroll', update, { passive: true })
    return () => window.removeEventListener('scroll', update)
  }, [])

  const homeLink = (id) => `/${id}`

  return (
    <nav id="site-navigation" className={`amutham-nav navbar navbar-expand-lg${solid ? ' is-solid' : ''}`} aria-label="Primary">
      <div className="container">
        <a className="navbar-brand" href="/"><span className="brand-mark" aria-hidden="true" />AMUTHAM</a>
        <button className="navbar-toggler" type="button" aria-expanded={menuOpen} aria-controls="amuthamNav" aria-label="Toggle navigation" onClick={() => setMenuOpen(!menuOpen)}>
          <span className="toggler-bar" /><span className="toggler-bar" /><span className="toggler-bar" />
        </button>
        <div className={`collapse navbar-collapse${menuOpen ? ' show' : ''}`} id="amuthamNav">
          <ul className="navbar-nav ms-auto align-items-lg-center mb-2 mb-lg-0">
            {['services', 'dishes', 'gallery'].map((id) => (
              <li className="nav-item" key={id}><a className="nav-link" href={homeLink(id)} onClick={() => setMenuOpen(false)}>{id[0].toUpperCase() + id.slice(1)}</a></li>
            ))}
            <li className="nav-item"><a className={`nav-link${isMenusPage ? ' active' : ''}`} href="/menus">Full menus</a></li>
          </ul>
          <a className="btn btn-ghost nav-cta" href="/menus" onClick={() => setMenuOpen(false)}>View menus</a>
          <a className="btn btn-amutham nav-cta" href="/quote" onClick={() => setMenuOpen(false)}>Request a quote</a>
        </div>
      </div>
    </nav>
  )
}
