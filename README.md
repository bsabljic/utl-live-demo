# UTL Live Demo (Vercel + Blob + Claude-ready)

This project is a serverless-first demo:
- CSV feed via Vercel Blob (or GitHub raw)
- API `/api/compare` computes deltas and (optionally) calls Claude for executive summaries
- React frontend renders CompareBar with "Powered by Claude" summaries
- KV-backed rate-limit; graceful fallbacks (mock summary; degraded banner)

## 1) One-time setup
- Create a new Vercel project; link this repo.
- In Vercel: Storage -> create **KV**.
- Upload CSV once to Blob (see below) or set GitHub raw URL.

### Env vars (Vercel -> Project Settings -> Environment Variables)
```
ANTHROPIC_API_KEY=sk-ant-...                # optional
CSV_PUBLIC_URL=https://blob.vercel-storage.com/utl-metrics.csv
KV_URL=kv://...                              # from Vercel KV
SLACK_WEBHOOK=https://hooks.slack.com/services/... (optional)
DEPLOY_SECRET=super-secret-deploy-token      (optional)
```

## 2) CSV upload to Blob (optional)
```
npm i -g vercel
vercel login
vercel blob put data/utl-metrics.csv --name utl-metrics.csv --public
# set CSV_PUBLIC_URL to the returned public URL
```

## 3) Local dev
```
npm i
vercel dev
# http://localhost:3000 (UI)
# http://localhost:3000/api/compare?metric=f1_score&sum=brief
```

## 4) Deploy
```
vercel --prod
curl "https://<app>.vercel.app/api/health"
curl "https://<app>.vercel.app/api/compare?metric=f1_score&sum=full"
```

## 5) Frontend
- React + Vite; API base is relative `/api`, no CORS needed on Vercel.

## 6) Notes
- If `ANTHROPIC_API_KEY` missing: summaries use mock text (no errors).
- If CSV unreachable: API falls back to mock data and sets `X-Data-Source: fallback`; UI shows banner.
