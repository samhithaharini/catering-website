import Reveal from './Reveal.jsx'

const dietaryOptions = [
  ['Vegan & vegetarian', 'Full plant-based menus that stand on their own, not afterthought side plates.'],
  ['Allergen-aware', 'Gluten-free, nut-free and dairy-free dishes prepared with care.'],
  ['Fully bespoke', 'Cultural menus, halal and kosher-style sourcing, family recipes recreated.'],
]

export default function DietarySection() {
  return (
    <section className="section section--paper" id="dietary"><div className="container">
      <div className="text-center mb-5 reveal in"><span className="eyebrow eyebrow--center">Everyone at the table</span><h2 className="display-heading">Dietary needs &amp; <em>bespoke menus</em></h2><p className="section-lead mx-auto text-center">No guest should feel like an afterthought. Tell us what your table needs and we’ll build around it.</p></div>
      <div className="diet-note">{dietaryOptions.map(([title, text]) => <Reveal className="diet-note__card" key={title}><h3 className="diet-note__title">{title}</h3><p className="diet-note__text">{text}</p></Reveal>)}</div>
    </div></section>
  )
}
