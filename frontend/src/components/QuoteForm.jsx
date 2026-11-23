import { cloneElement, useRef, useState } from 'react'

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/+$/, '')

export default function QuoteForm() {
  const honeypotRef = useRef(null)
  const [values, setValues] = useState({ event_type: '', event_date: '', guests: '', name: '', email: '', notes: '' })
  const [errors, setErrors] = useState({})
  const [status, setStatus] = useState({ type: '', message: '' })
  const [sending, setSending] = useState(false)
  function update(event) {
    const { name, value } = event.target
    setValues((current) => ({ ...current, [name]: value }))
    setErrors((current) => ({ ...current, [name]: '' }))
    setStatus({ type: '', message: '' })
  }

  async function submit(event) {
    event.preventDefault()
    const nextErrors = {}
    if (!values.event_type) nextErrors.event_type = 'Please select an event type.'
    if (!values.event_date) nextErrors.event_date = 'Please choose your event date.'
    if (!Number.isInteger(Number(values.guests)) || Number(values.guests) < 1 || Number(values.guests) > 10000) nextErrors.guests = 'Enter a guest count from 1 to 10,000.'
    if (!values.name.trim()) nextErrors.name = 'Please tell us your name.'
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email.trim())) nextErrors.email = 'Enter a valid email address.'

    setErrors(nextErrors)
    if (Object.keys(nextErrors).length > 0) {
      document.getElementById(Object.keys(nextErrors)[0])?.focus()
      return
    }

    setSending(true)
    setStatus({ type: '', message: '' })
    try {
      const response = await fetch(`${apiBaseUrl}/api/quotes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...values, website: honeypotRef.current?.value || '', guests: Number(values.guests), name: values.name.trim(), email: values.email.trim(), notes: values.notes.trim() }),
      })
      const result = await response.json()
      if (!response.ok) throw new Error(result.error || 'Your enquiry could not be saved.')
      setStatus({ type: 'success', message: 'Thanks — your enquiry has been received. Our team will be in touch.' })
      setValues({ event_type: '', event_date: '', guests: '', name: '', email: '', notes: '' })
    } catch (error) {
      setStatus({
        type: 'failure',
        message: error instanceof TypeError
          ? 'Could not reach the quote server. Start it with “py server.py” and try again.'
          : error.message,
      })
    } finally {
      setSending(false)
    }
  }

  const field = (name, label, content, wide = false) => (
    <div className={`${wide ? 'col-12' : 'col-sm-6'}${errors[name] ? ' field-invalid' : ''}`} data-field key={name}>
      <label className="form-label" htmlFor={name}>{label}</label>
      {cloneElement(content, {
        'aria-invalid': Boolean(errors[name]),
        'aria-describedby': errors[name] ? `${name}-error` : undefined,
      })}
      <span className="form-error" id={`${name}-error`}>{errors[name]}</span>
    </div>
  )

  return (
    <div className="quote-wrap" id="quote-form">
      <form noValidate onSubmit={submit}>
        <div className="quote-honeypot" aria-hidden="true">
          <label htmlFor="quote-website">Leave this field empty</label>
          <input ref={honeypotRef} id="quote-website" name="website" type="text" tabIndex="-1" autoComplete="off" />
        </div>
        <div className="row g-3">
          {field('event_type', 'Event type', (
            <select className="form-select" id="event_type" name="event_type" value={values.event_type} onChange={update} required>
              <option value="">Choose one…</option>
              <option value="wedding">Wedding</option><option value="corporate">Corporate event</option>
              <option value="private-party">Private party</option><option value="cocktail">Cocktail reception</option>
              <option value="buffet">Buffet</option><option value="plated">Plated dinner</option>
            </select>
          ))}
          {field('event_date', 'Event date', <input className="form-control" type="date" id="event_date" name="event_date" value={values.event_date} onChange={update} required />)}
          {field('guests', 'Guest count', <input className="form-control" type="number" id="guests" name="guests" min="1" max="10000" placeholder="e.g. 80" value={values.guests} onChange={update} required />)}
          {field('name', 'Your name', <input className="form-control" type="text" id="name" name="name" maxLength="120" placeholder="Full name" value={values.name} onChange={update} required />)}
          {field('email', 'Email address', <input className="form-control" type="email" id="email" name="email" maxLength="254" placeholder="you@email.com" value={values.email} onChange={update} required />, true)}
          <div className="col-12">
            <label className="form-label" htmlFor="notes">Anything else? <span className="optional-note">(optional)</span></label>
            <textarea className="form-control" id="notes" name="notes" rows="3" maxLength="2000" placeholder="Dietary requirements, venue, style…" value={values.notes} onChange={update} />
          </div>
        </div>
        <button className="btn btn-amutham btn-lg btn-block-sm mt-4" type="submit" disabled={sending}>{sending ? 'Sending…' : 'Send my enquiry'}</button>
        {status.type === 'success' && <div className="form-success show" role="status">{status.message}</div>}
        {status.type === 'failure' && <div className="form-failure" role="alert">{status.message}</div>}
      </form>
    </div>
  )
}
