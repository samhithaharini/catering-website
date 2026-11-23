import { useEffect } from 'react'
import HomePage from './pages/HomePage.jsx'
import MenusPage from './pages/MenusPage.jsx'

const sectionRoutes = {
  '/main': 'main',
  '/hero': 'hero',
  '/services': 'services',
  '/dishes': 'dishes',
  '/how-it-works': 'how',
  '/quote': 'quote',
  '/gallery': 'gallery',
  '/stats': 'stats',
  '/dietary': 'dietary',
  '/call-to-action': 'cta',
  '/packages': 'packages',
  '/menu-styles': 'menus',
}

export default function App() {
  const path = window.location.pathname.replace(/\/+$/, '') || '/'
  const isMenusPage = path === '/menus' || path === '/packages' || path === '/menu-styles' || path === '/sample-menus'
  const sectionId = sectionRoutes[path]

  useEffect(() => {
    if (sectionId) document.getElementById(sectionId)?.scrollIntoView()
  }, [sectionId])

  return isMenusPage ? <MenusPage /> : <HomePage />
}
