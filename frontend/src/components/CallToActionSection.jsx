export default function CallToActionSection({ eyebrow, heading, emphasis, text }) {
  return (
    <section className="section cta-band" id="cta">
      <div className="cta-band__bg"><img src="/img/hero-table.jpg" alt="" width="1920" height="900" loading="lazy" /></div>
      <div className="container cta-band__inner"><div className="row align-items-center g-4">
        <div className="col-lg-8 reveal in"><span className="eyebrow">{eyebrow}</span><h2 className="cta-band__title">{heading} <em>{emphasis}</em></h2><p className="cta-band__text">{text}</p></div>
        <div className="col-lg-4 text-lg-end"><a className="btn btn-amutham btn-lg" href="/quote">Request a quote</a></div>
      </div></div>
    </section>
  )
}
