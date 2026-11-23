import { useState } from 'react'
import DietTag from './DietTag.jsx'
import biriyaniImage from '../assets/biriyani.jpeg'
import curdRiceImage from '../assets/curd rice.jpeg'
import eggGravyImage from '../assets/egg gravy.jpeg'
import lemonRiceImage from '../assets/lemon rice.jpeg'
import nonVegMealsImage from '../assets/non veg meals.jpeg'
import vadaImage from '../assets/vada.jpeg'
import vegBiriyaniImage from '../assets/veg biriyani.jpeg'
import vegMealsImage from '../assets/veg meals.jpeg'
import tomatoRiceImage from '../assets/WhatsApp Image 2026-11-16 at 3.11.08 PM.jpeg'

const dishes = [
  { name: 'Biryani', description: 'Biryani served with the chicken pieces and boiled egg shown in the image.', image: biriyaniImage, tags: ['nv'] },
  { name: 'Curd Rice', description: 'Curd rice, shown with its toppings.', image: curdRiceImage, tags: [] },
  { name: 'Egg Gravy', description: 'Egg gravy served with boiled egg.', image: eggGravyImage, tags: ['nv'] },
  { name: 'Lemon Rice', description: 'Lemon rice served with lemon wedges on the side.', image: lemonRiceImage, tags: [] },
  { name: 'Non-Veg Meals', description: 'A non-vegetarian meal served on a banana leaf.', image: nonVegMealsImage, tags: ['nv'] },
  { name: 'Vada', description: 'Vada served with the accompaniments shown.', image: vadaImage, tags: [] },
  { name: 'Veg Briyani', description: 'Vegetable biryani.', image: vegBiriyaniImage, tags: ['v'] },
  { name: 'Veg Meals', description: 'A vegetarian meal served on a banana leaf.', image: vegMealsImage, tags: ['v'] },
  { name: 'Tomato Rice', description: 'Tomato rice.', image: tomatoRiceImage, tags: [] },
]

const filters = [['all', 'All dishes'], ['v', 'Vegetarian'], ['nv', 'Non-vegetarian']]

export default function DishesSection() {
  const [filter, setFilter] = useState('all')

  return (
    <section className="section section--tint" id="dishes">
      <div className="container">
        <div className="text-center mb-5 reveal in">
          <span className="eyebrow eyebrow--center">Our food</span>
          <h2 className="display-heading">Dishes made for <em>everyday</em></h2>
          <p className="section-lead mx-auto text-center">Explore our rice dishes, snacks and meal options.</p>
        </div>
        <div className="filter-bar reveal in" role="group" aria-label="Filter dishes by dietary type">
          {filters.map(([id, label]) => <button className="filter-btn" type="button" key={id} aria-pressed={filter === id} onClick={() => setFilter(id)}>{label}</button>)}
        </div>
        <p className="dietary-legend" aria-label="Dietary label meanings">
          <span><strong>V</strong> Vegetarian</span>
          <span><strong>NV</strong> Non-vegetarian</span>
        </p>
        <div className="dish-grid">
          {dishes.filter((dish) => filter === 'all' || dish.tags.includes(filter)).map(({ name, description, image, tags }) => (
            <article className="dish-card reveal in" key={name}>
              <div className="dish-card__media"><img src={image} alt={name} width="480" height="360" loading="lazy" /></div>
              <div className="dish-card__body"><h3 className="dish-card__name">{name}</h3><p className="dish-card__desc">{description}</p><div className="dish-card__tags">{tags.map((tag) => <DietTag key={tag} tag={tag} />)}</div></div>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
