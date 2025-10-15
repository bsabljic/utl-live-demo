import React from 'react'
export default function DegradedBanner({ source }:{ source?: string }){
  if (source !== 'fallback') return null
  return (
    <div style={{ padding:12, background:'#78350f33', border:'1px solid #f59e0b55', borderRadius:8, marginBottom:12 }}>
      <strong style={{ color:'#f59e0b' }}>⚠️ Degraded Mode</strong>
      <div style={{ color:'#fde68a' }}>Prikazujemo fallback podatke. Live feed privremeno nedostupan.</div>
    </div>
  )
}
