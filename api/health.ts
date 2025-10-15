import type { VercelRequest, VercelResponse } from '@vercel/node'
import { fetchMetrics } from './utils/csv-adapter'
import { generateSummary } from './utils/claude-client'

export default async function handler(_req: VercelRequest, res: VercelResponse){
  const checks = await Promise.allSettled([
    fetchMetrics(),
    generateSummary('f1_score', [], 'brief')
  ])
  const csvOk = checks[0].status === 'fulfilled'
  const claudeOk = checks[1].status === 'fulfilled'

  const status = (!csvOk && !claudeOk) ? 503 : 200
  res.status(status).json({
    ok: csvOk && claudeOk,
    timestamp: new Date().toISOString(),
    components: [
      { name:'CSV',    status: csvOk ? 'ok':'fail' },
      { name:'Claude', status: claudeOk ? 'ok':'fail' }
    ]
  })
}
