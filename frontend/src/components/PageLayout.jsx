import { useEffect } from 'react'
import Footer from './Footer.jsx'
import Navbar from './Navbar.jsx'

export default function PageLayout({ isMenusPage, title, children }) {
  useEffect(() => {
    document.title = title
  }, [title])

  return (
    <>
      <a className="skip-link" href="/main">Skip to content</a>
      <Navbar isMenusPage={isMenusPage} />
      {children}
      <Footer />
    </>
  )
}
