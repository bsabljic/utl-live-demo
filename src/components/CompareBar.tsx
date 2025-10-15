import React, { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell } from 'recharts'
import DegradedBanner from './DegradedBanner'

type Metric = 'f1_score' | 'latency_ms' | 'false_positive_rate' | 'efficiency'

interface Props {
  metric?: Metric
  topN?: number
  sum?: ''|'brief'|'full'
}

export default function CompareBar({ metric='f1_score', topN=6, sum='' }: Props){
  const [payload, setPayload] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string|null>(null)
  const [source, setSource] = useState<string|undefined>(undefined)

  useEffect(()=>{
    const run = async () => {
      try {
        setLoading(true); setError(null)
        const params = new URLSearchParams({ metric, topN: String(topN), sum })
        const resp = await axios.get(`/api/compare?${params.toString()}`)
        setPayload(resp.data)
        setSource(resp.headers['x-data-source'])
      } catch (e:any) {
        setError(e?.message || 'Failed to load')
      } finally {
        setLoading(false)
      }
    }
    run()
  }, [metric, topN, sum])

  if (loading) return <div>Loading {metric}…</div>
  if (error) return <div style={{ color:'#fca5a5' }}>Error: {error}</div>
  if (!payload?.ok) return <div>No data</div>

  const rows = (payload.domains || []).map((d:any)=>({ ...d, _val: d.diff, _neg: d.diff < 0 }))
  const unit = metric==='latency_ms' ? 'ms' : (metric==='false_positive_rate' ? '%' : '')

  return (
    <div style={{ background:'#111827', border:'1px solid #334155', padding:16, borderRadius:12 }} data-testid={`compare-${metric}`}>
      <DegradedBanner source={source} />
      {payload.summary && (
        <div style={{ padding:12, background:'#0d948833', border:'1px solid #14b8a6', borderRadius:8, marginBottom:12 }}>
          🧠 Powered by Claude — {payload.summary}
        </div>
      )}
      <div style={{ height:400 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={rows} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="domain" angle={-30} textAnchor="end" height={70} />
            <YAxis tickFormatter={(v)=>`${v}${unit}`} />
            <Tooltip formatter={(v:number)=>[`${v.toFixed(3)}${unit}`, 'Δ (UTL - Baseline)']} />
            <Legend />
            <Bar dataKey="_val" name={`Δ ${unit}`}>
              {rows.map((r:any, i:number)=>(
                <Cell key={i} fill={r._neg ? '#ef4444' : '#10b981'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
