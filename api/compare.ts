import type { VercelRequest, VercelResponse } from '@vercel/node'
import { fetchMetrics, computeDiffs } from './utils/csv-adapter'
import { generateSummary } from './utils/claude-client'
import { checkRateLimit } from './utils/rate-limit'

const METRICS = ["f1_score","latency_ms","false_positive_rate","efficiency"] as const

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method==='OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin','*')
    res.setHeader('Access-Control-Allow-Methods','GET, POST, OPTIONS')
    res.setHeader('Access-Control-Allow-Headers','Content-Type, Authorization')
    return res.status(200).end()
  }

  const rate = await checkRateLimit(req)
  if (rate.limited) {
    res.setHeader('Retry-After', String(rate.retryAfter))
    res.setHeader('X-RateLimit-Remaining','0')
    return res.status(429).json({ ok:false, error:'Rate limited', retryAfter: rate.retryAfter })
  } else {
    res.setHeader('X-RateLimit-Remaining', String(rate.remaining))
  }

  const { file1='Span Baseline', file2='UTL Framework', metric='f1_score', sum='', topN='12' } = req.query
  if (!METRICS.includes(metric as any)) {
    return res.status(400).json({ ok:false, error:`Unknown metric '${metric}'. Allowed: ${METRICS.join(', ')}` })
  }

  try {
    const raw = await fetchMetrics()
    const data = computeDiffs(raw)
    const top_n = parseInt(String(topN),10) || 12

    const domains = data
      .map((d:any)=>({ domain:d.domain, A:d.baseline, B:d.utl, diff:d.diff[metric as string] }))
      .filter((d:any)=>d.domain && Number.isFinite(d.diff))
      .sort((a:any,b:any)=>Math.abs(b.diff)-Math.abs(a.diff))
      .slice(0, top_n)

    let summary: string | undefined
    if (sum) {
      summary = await generateSummary(metric as any, domains as any, sum as 'brief'|'full')
    }

    res.setHeader('Access-Control-Allow-Origin','*')
    res.setHeader('Cache-Control', sum ? 'public, s-maxage=5' : 'public, s-maxage=60')
    res.setHeader('X-Data-Source', raw?.[0]?.timestamp ? 'live' : 'fallback')
    res.setHeader('X-Domains-Count', String(domains.length))

    return res.json({ ok:true, files:[file1,file2], metric, domains, summary, timestamp: new Date().toISOString() })
  } catch (e:any) {
    return res.status(503).json({ ok:false, error:'Data pipeline unavailable', detail: e?.message })
  }
}
