import { useEffect, useRef } from 'react'

function useReveal() {
  const ref = useRef(null)

  useEffect(() => {
    const element = ref.current
    if (!element) return undefined

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
      element.classList.add('in')
      return undefined
    }

    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        element.classList.add('in')
        observer.disconnect()
      }
    }, { threshold: 0.14 })
    observer.observe(element)
    return () => observer.disconnect()
  }, [])

  return ref
}

export default function Reveal({ as: Element = 'div', className = '', delay = '', children, ...props }) {
  const ref = useReveal()
  const delayClass = delay ? `reveal--d${delay}` : ''
  return <Element ref={ref} className={`reveal ${delayClass} ${className}`.trim()} {...props}>{children}</Element>
}
