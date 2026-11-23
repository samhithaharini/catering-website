import CallToActionSection from '../components/CallToActionSection.jsx'
import PackagesSection from '../components/PackagesSection.jsx'
import PageLayout from '../components/PageLayout.jsx'
import QuoteSection from '../components/QuoteSection.jsx'

export default function MenusPage() {
  return (
    <PageLayout isMenusPage title="Daily Menu & Catering Orders — Amutham">
      <header className="page-head">
        <div className="page-head__bg"><img src="/img/menus-header.jpg" alt="" width="1920" height="900" fetchPriority="high" /></div>
        <div className="container page-head__inner" id="full-menus"><p className="crumb"><a href="/">Home</a> / Menu</p><h1 className="page-head__title">Our daily <em>menu</em></h1><p className="section-lead">Fresh rice dishes, snacks and full meal orders from Sri Amutham Catering Services in Unjavelampatti, Pollachi.</p></div>
      </header>
      <main id="main">
        <PackagesSection />
        <QuoteSection />
        <CallToActionSection eyebrow="Meal bookings" heading="Ready to place" emphasis="an order?" text="Contact us for meal bookings and bulk orders." />
      </main>
    </PageLayout>
  )
}
