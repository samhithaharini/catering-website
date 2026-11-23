import Reveal from './Reveal.jsx'

const services = [
  ['Weddings', 'Ceremony canapés through to the late-night grazing table, tailored to your day.', 'event-weddings.jpg'],
  ['Corporate Events', 'Conferences, product launches and board lunches delivered on time, on brand.', 'event-corporate.jpg'],
  ['Private Parties', 'Milestone birthdays and anniversaries with a private chef in your own kitchen.', 'event-private.jpg'],
  ['Cocktail Receptions', 'Passed bites and a bespoke drinks list to keep a standing crowd delighted.', 'event-cocktail.jpg'],
  ['Buffets & Grazing', 'Abundant sharing spreads and grazing tables styled to be as beautiful as they are generous.', 'event-buffet.jpg'],
  ['Plated Dinners', 'Multi-course fine dining with front-of-house service for a seated occasion.', 'event-plated.jpg'],
]

export default function ServicesSection() {
  return (
    <section className="section section--paper" id="services">
      <div className="container">
        <div className="row align-items-end mb-5">
          <Reveal className="col-lg-8"><span className="eyebrow">What we cater</span><h2 className="display-heading">Every occasion, <em>plated to perfection</em></h2></Reveal>
          <Reveal className="col-lg-4" delay="1"><p className="section-lead">From intimate supper clubs to 400-guest galas, our team scales the same care to every table.</p></Reveal>
        </div>
        <div className="event-grid">
          {services.map(([title, text, image], index) => (
            <Reveal as="article" className={`event-card reveal--d${index % 3}`} key={title}>
              <img src={`/img/${image}`} alt={title} width="600" height="680" loading="lazy" />
              <div className="event-card__body"><span className="event-card__num">{String(index + 1).padStart(2, '0')}</span><h3 className="event-card__title">{title}</h3><p className="event-card__text">{text}</p></div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}
