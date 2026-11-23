import CallToActionSection from '../components/CallToActionSection.jsx'
import DietarySection from '../components/DietarySection.jsx'
import DishesSection from '../components/DishesSection.jsx'
import GallerySection from '../components/GallerySection.jsx'
import HowItWorksSection from '../components/HowItWorksSection.jsx'
import PageLayout from '../components/PageLayout.jsx'
import QuoteSection from '../components/QuoteSection.jsx'
import ServicesSection from '../components/ServicesSection.jsx'
import StatsSection from '../components/StatsSection.jsx'

export default function HomePage() {
  return (
    <PageLayout isMenusPage={false} title="Amutham — Catering & Private-Event Chefs">
      <header className="hero" id="hero">
        <div className="hero__bg"><img src="/img/hero-table.jpg" alt="" width="1920" height="1280" fetchPriority="high" /></div>
        <div className="container hero__inner"><div className="row"><div className="col-lg-8 col-xl-7">
          <span className="hero__tag"><span className="dot" aria-hidden="true" />620+ events catered across the region</span>
          <h1 className="hero__title">Unforgettable food, <em>beautifully catered</em> for the moments that matter.</h1>
          <p className="hero__sub">Amutham is a boutique catering house and private-chef team crafting seasonal menus for weddings, celebrations, and corporate events — from passed canapés to full plated dinners.</p>
          <div className="hero__cta"><a className="btn btn-amutham btn-lg" href="/quote">Request a quote</a><a className="btn btn-ghost btn-lg" href="/menus">Browse menus</a></div>
          <div className="hero__meta">{[['14', 'Years catering'], ['4.9★', 'Across 300+ reviews'], ['100%', 'Seasonal & locally sourced']].map(([value, label]) => <div key={label}><span className="hero__meta-num">{value}</span><span className="hero__meta-label">{label}</span></div>)}</div>
        </div></div></div>
      </header>
      <main id="main">
        <ServicesSection />
        <DishesSection />
        <HowItWorksSection />
        <QuoteSection />
        <GallerySection />
        <StatsSection />
        <DietarySection />
        <CallToActionSection eyebrow="Let’s plan it" heading="Request your" emphasis="catering quote" text="Dates fill quickly in peak season. Send us your details and we’ll craft a menu proposal for your celebration." />
      </main>
    </PageLayout>
  )
}
