UTL Live Demo — Vercel Python API Fix
====================================

Files included
--------------
1) vercel.json
   - Forces Python runtime for /api/*.py (python3.11)
   - Keeps Vite build (npm run build -> dist)
   - Rewrites: /api/* goes to serverless, everything else to /index.html

2) requirements.txt
   - Add your Python deps here (currently: requests).

How to use
----------
A) Quick merge (recommended)
   1. Copy `vercel.json` to repo root (same level as package.json).
   2. Copy `requirements.txt` to repo root.
   3. Commit & push:
        git add vercel.json requirements.txt
        git commit -m "Force Python runtime for API + add requirements"
        git push
   4. In Vercel: Redeploy -> tick "Clear build cache".

B) Optional: sanity-test Python function
   - Ensure you have /api/index.py or /api/compare.py with a `handler(request)` function that returns (body, status_code, headers) or a dict.
