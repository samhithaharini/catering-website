import Reveal from './Reveal.jsx'

const steps = [
  ['Enquire', 'Tell us your date, guest count and the mood you’re after. We reply within one working day with ideas and a ballpark quote.'],
  ['Menu & tasting', 'We design a bespoke menu together, then invite you to a private tasting to finalise every dish and pairing.'],
  ['We cater', 'Our chefs and front-of-house team arrive, set up, cook on site and clear away — you don’t lift a finger.'],
  ['You celebrate', 'Relax with your guests while we take care of the food, the service and every detail on the day.'],
]

export default function HowItWorksSection() {
  return (
    <section className="section section--paper" id="how">
      <div className="container">
        <div className="text-center mb-5 reveal in"><span className="eyebrow eyebrow--center">How it works</span><h2 className="display-heading">From first enquiry <em>to your celebration</em></h2></div>
        <div className="steps">{steps.map(([title, text], index) => <Reveal as="article" className={`step reveal--d${index}`} key={title}><span className="step__num">0{index + 1}</span><h3 className="step__title">{title}</h3><p className="step__text">{text}</p></Reveal>)}</div>
      </div>
    </section>
  )
}
