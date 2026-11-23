import Reveal from './Reveal.jsx'
import QuoteForm from './QuoteForm.jsx'

export default function QuoteSection() {
  return (
    <section className="section section--dark" id="quote">
      <div className="container">
        <div className="row g-4 g-lg-5 align-items-center">
          <Reveal className="col-lg-6">
            <span className="eyebrow">Request a quote</span>
            <h2 className="display-heading">Tell us about <em>your event</em></h2>
            <p className="section-lead">Share a few details and we’ll come back with a tailored menu proposal and an itemised quote. No obligation, no pressure — just great food ideas.</p>
            <div className="quote-aside mt-4">
              {[
                ['Fast, human replies', 'A real member of our events team responds within one working day.'],
                ['Transparent pricing', 'Per-person rates with everything itemised — no surprise service charges.'],
                ['Complimentary tasting', 'Confirmed bookings over 40 guests include a private menu tasting.'],
              ].map(([title, text], index) => (
                <div className="quote-aside__item" key={title}>
                  <span className="quote-aside__k">0{index + 1}</span>
                  <div><p className="quote-aside__t">{title}</p><p className="quote-aside__d">{text}</p></div>
                </div>
              ))}
            </div>
          </Reveal>
          <Reveal className="col-lg-6" delay="1"><QuoteForm /></Reveal>
        </div>
      </div>
    </section>
  )
}
