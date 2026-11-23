export default function StatsSection() {
  const stats = [['620', '+', 'Events Catered'], ['84,000', '+', 'Guests Served'], ['14', '', 'Years Catering'], ['4.9', '★', 'Average Review']]

  return (
    <section className="section section--dark section--tight" id="stats"><div className="container"><div className="stats">{stats.map(([number, suffix, label]) => <div className="stat reveal in" key={label}><div className="stat__num">{number}<span className="suffix">{suffix}</span></div><div className="stat__label">{label}</div></div>)}</div></div></section>
  )
}
