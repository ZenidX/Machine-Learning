import { useEffect, useRef } from 'react'
import mermaid from 'mermaid'

mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    primaryColor: '#3b82f6',
    primaryTextColor: '#1e3a8a',
    primaryBorderColor: '#2563eb',
    lineColor: '#64748b',
    secondaryColor: '#f1f5f9',
    tertiaryColor: '#f8fafc',
    fontFamily: 'system-ui, -apple-system, sans-serif',
  },
  flowchart: {
    htmlLabels: true,
    curve: 'basis',
  },
})

export default function MermaidDiagram({ chart, className = '' }) {
  const containerRef = useRef(null)

  useEffect(() => {
    if (containerRef.current && chart) {
      containerRef.current.innerHTML = ''

      const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`

      mermaid.render(id, chart).then(({ svg }) => {
        if (containerRef.current) {
          containerRef.current.innerHTML = svg
        }
      }).catch((error) => {
        console.error('Mermaid rendering error:', error)
        if (containerRef.current) {
          containerRef.current.innerHTML = `<pre class="text-red-500">${error.message}</pre>`
        }
      })
    }
  }, [chart])

  return (
    <div
      ref={containerRef}
      className={`mermaid-container flex justify-center overflow-x-auto ${className}`}
    />
  )
}
