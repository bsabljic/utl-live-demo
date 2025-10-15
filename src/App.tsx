import React from 'react'
import CompareBar from './components/CompareBar'

export default function App(){
  return (
    <div style={{ minHeight:'100vh', padding:'24px', background:'#0f172a', color:'#e5e7eb' }}>
      <h1 style={{ fontSize:28, marginBottom:8, color:'#2dd4bf' }}>UTL Framework vs Baseline</h1>
      <p style={{ marginBottom:24, color:'#94a3b8' }}>Live CSV feed + Claude executive summaries</p>
      <div style={{ display:'grid', gap:24 }}>
        <CompareBar metric="f1_score" sum="brief" />
        <CompareBar metric="latency_ms" />
      </div>
    </div>
  )
}
