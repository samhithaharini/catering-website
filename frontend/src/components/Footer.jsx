export default function Footer() {
  return (
    <footer className="footer" id="footer"><div className="container"><div className="row g-4">
      <div className="col-lg-4"><span className="footer__brand"><span className="brand-mark" aria-hidden="true" />AMUTHAM</span><p className="footer__text">A boutique catering house and private-chef team crafting seasonal menus for the moments that matter.</p></div>
      <div className="col-6 col-lg-2"><h5>Explore</h5><ul className="footer__links">{[['Services', '/services'], ['Menu', '/menus'], ['Gallery', '/gallery']].map(([label, href]) => <li key={label}><a href={href}>{label}</a></li>)}</ul></div>
      <div className="col-6 col-lg-2"><h5>Occasions</h5><ul className="footer__links">{[['Weddings', '/services'], ['Corporate', '/services'], ['Private parties', '/services'], ['Get a quote', '/quote']].map(([label, href]) => <li key={label}><a href={href}>{label}</a></li>)}</ul></div>
      <div className="col-lg-4"><h5>Get in touch</h5><ul className="footer__contact"><li><span>The Old Bakery, 14 Mill Lane, Riverside</span></li><li><a href="tel:+441234567890">+44 (0)1234 567 890</a></li><li><a href="mailto:hello@amuthamcatering.example">hello@amuthamcatering.example</a></li></ul></div>
      </div><div className="footer__bottom"><span>© 2026 AMUTHAM Catering. All rights reserved.</span></div></div></footer>
  )
}
