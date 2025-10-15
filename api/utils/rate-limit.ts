import type { VercelRequest } from '@vercel/node'
import { kv } from '@vercel/kv'

export async function checkRateLimit(req: VercelRequest, maxRequests=10, windowMs=60000){
  const ip = (req.headers['x-forwarded-for'] as string)?.split(',')[0]?.trim() || 'unknown'
  const metric = String(req.query.metric || 'all')
  const key = `rate:${ip}:${metric}`
  const now = Date.now()
  const windowStart = now - windowMs

  const count = await kv.zcount(key, windowStart, now)
  if (count >= maxRequests) {
    const retryAfter = Math.ceil((windowMs - (now % windowMs))/1000)
    return { limited:true, remaining:0, retryAfter }
  }
  await kv.zadd(key, { score: now, member: String(now) })
  await kv.zremrangebyscore(key, 0, windowStart)
  return { limited:false, remaining: maxRequests - count - 1, retryAfter:0 }
}
