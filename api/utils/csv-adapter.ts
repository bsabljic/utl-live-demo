import Papa from 'papaparse'

type MetricRow = {
  domain: string
  baseline_f1: string
  baseline_latency: string
  baseline_false_pos: string
  baseline_efficiency: string
  utl_f1: string
  utl_latency: string
  utl_false_pos: string
  utl_efficiency: string
  timestamp?: string
}

const MAX_RETRIES = 3
const TIMEOUT_MS = 5000

export async function fetchMetrics(): Promise<any[]> {
  const sources = [
    process.env.CSV_PUBLIC_URL,
    'https://raw.githubusercontent.com/bsabljic/utl-data/main/utl-metrics.csv'
  ].filter(Boolean) as string[]

  let attempt = 0
  for (const url of sources) {
    for (let i=0;i<MAX_RETRIES;i++) {
      attempt++
      try {
        const controller = new AbortController()
        const t = setTimeout(()=>controller.abort(), TIMEOUT_MS)
        const resp = await fetch(url, { cache:'no-store', signal: controller.signal })
        clearTimeout(t)
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
        const text = await resp.text()
        if (text.length < 50) throw new Error('CSV too small')

        const parsed = Papa.parse(text, { header:true, skipEmptyLines:true })
        if (parsed.errors?.length) throw new Error(parsed.errors.map(e=>e.message).join('; '))
        const rows = (parsed.data as MetricRow[]).filter(r=>r.domain?.trim())
        if (!rows.length) throw new Error('No rows')

        const valid = rows.filter(validateRow)
        if (!valid.length) throw new Error('No valid rows')

        return valid.map(parseRow)
      } catch (e) {
        if (attempt >= sources.length * MAX_RETRIES) {
          return mockFallback()
        }
        await new Promise(r=>setTimeout(r, 500 * (i+1)))
      }
    }
  }
  return mockFallback()
}

export function computeDiffs(domains: any[]) {
  return domains.map(d => ({
    ...d,
    diff: {
      f1_score: d.utl.f1_score - d.baseline.f1_score,
      latency_ms: d.utl.latency_ms - d.baseline.latency_ms,
      false_positive_rate: d.utl.false_positive_rate - d.baseline.false_positive_rate,
      efficiency: d.utl.efficiency - d.baseline.efficiency
    }
  }))
}

function validateRow(r: MetricRow) {
  const bf1 = parseFloat(r.baseline_f1); const uf1 = parseFloat(r.utl_f1)
  const bl = parseInt(r.baseline_latency); const ul = parseInt(r.utl_latency)
  if (!(bf1>=0 && bf1<=1 && uf1>=0 && uf1<=1)) return false
  if (!(bl>0 && ul>0)) return false
  return true
}

function parseRow(r: MetricRow) {
  return {
    domain: r.domain.trim(),
    baseline: {
      f1_score: toNum(r.baseline_f1),
      latency_ms: toInt(r.baseline_latency),
      false_positive_rate: toNum(r.baseline_false_pos),
      efficiency: toNum(r.baseline_efficiency)
    },
    utl: {
      f1_score: toNum(r.utl_f1),
      latency_ms: toInt(r.utl_latency),
      false_positive_rate: toNum(r.utl_false_pos),
      efficiency: toNum(r.utl_efficiency)
    },
    timestamp: r.timestamp
  }
}

function toNum(x?: string){ const n = Number(x); return Number.isFinite(n)?n:0 }
function toInt(x?: string){ const n = parseInt(String(x||'').trim(),10); return Number.isFinite(n)?n:0 }

function mockFallback(){
  return [{
    domain: "High-value clients (fallback)",
    baseline: { f1_score: 0.72, latency_ms: 250, false_positive_rate: 0.12, efficiency: 0.65 },
    utl:      { f1_score: 0.86, latency_ms:  47, false_positive_rate: 0.04, efficiency: 0.92 },
    timestamp: new Date().toISOString()
  }]
}
