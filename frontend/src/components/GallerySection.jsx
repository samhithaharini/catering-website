import { useEffect, useState } from 'react'
import Reveal from './Reveal.jsx'

const gallery = [
  'Long banquet table dressed for a summer wedding reception',
  'Chef plating a fine-dining course during service',
  'Grazing table piled with cheeses, fruit and charcuterie',
  'Waiter passing a tray of canapés at a cocktail reception',
  'Close-up of a plated dessert with berries and gold leaf',
  'Outdoor marquee dinner lit with festoon lights at dusk',
  'Buffet spread of colourful seasonal salads and breads',
  'Guests toasting with champagne at a garden party',
].map((caption, index) => ({ caption, image: `gallery-${index + 1}.jpg` }))

export default function GallerySection() {
  const [lightboxIndex, setLightboxIndex] = useState(null)

  useEffect(() => {
    if (lightboxIndex === null) return undefined
    const onKeyDown = (event) => {
      if (event.key === 'Escape') setLightboxIndex(null)
      if (event.key === 'ArrowRight') setLightboxIndex((index) => (index + 1) % gallery.length)
      if (event.key === 'ArrowLeft') setLightboxIndex((index) => (index - 1 + gallery.length) % gallery.length)
    }
    document.addEventListener('keydown', onKeyDown)
    return () => document.removeEventListener('keydown', onKeyDown)
  }, [lightboxIndex])

  return (
    <>
      <section className="section section--tint" id="gallery">
        <div className="container">
          <div className="row align-items-end mb-5">
            <Reveal className="col-lg-8"><span className="eyebrow">Recent events</span><h2 className="display-heading">Catered &amp; <em>styled by us</em></h2></Reveal>
            <Reveal className="col-lg-4" delay="1"><p className="section-lead">A look at the tables, spreads and moments from weddings and events across the region.</p></Reveal>
          </div>
          <div className="gallery-grid">{gallery.map(({ image, caption }, index) => <button type="button" className={`gallery-item${index === 0 || index === 5 ? ' tall' : ''}`} key={image} aria-label={`View: ${caption}`} onClick={() => setLightboxIndex(index)}><img src={`/img/${image}`} alt={caption} width="600" height={index === 0 || index === 5 ? '800' : '400'} loading="lazy" /></button>)}</div>
        </div>
      </section>
      {lightboxIndex !== null && <div className="lightbox open" role="dialog" aria-modal="true" aria-label="Event gallery image viewer" onClick={() => setLightboxIndex(null)}>
        <button className="lightbox__btn lightbox__close" type="button" aria-label="Close gallery" onClick={() => setLightboxIndex(null)}>×</button>
        <button className="lightbox__btn lightbox__prev" type="button" aria-label="Previous image" onClick={(event) => { event.stopPropagation(); setLightboxIndex((lightboxIndex - 1 + gallery.length) % gallery.length) }}>‹</button>
        <img className="lightbox__img" src={`/img/${gallery[lightboxIndex].image}`} alt={gallery[lightboxIndex].caption} onClick={(event) => event.stopPropagation()} />
        <button className="lightbox__btn lightbox__next" type="button" aria-label="Next image" onClick={(event) => { event.stopPropagation(); setLightboxIndex((lightboxIndex + 1) % gallery.length) }}>›</button>
        <p className="lightbox__cap">{gallery[lightboxIndex].caption}</p>
      </div>}
    </>
  )
}
