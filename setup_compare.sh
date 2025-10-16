#!/bin/bash
echo ""
echo "=========================================="
echo "  🧩 UTL Compare Endpoint Setup Wizard"
echo "=========================================="
echo ""
echo "Odaberi backend tip:"
echo "1) Python (Vercel .py handler)"
echo "2) Node/TypeScript (Vercel .ts handler)"
echo ""
read -p "Upiši 1 ili 2 i pritisni Enter: " CHOICE
echo ""

# Kreiraj api folder ako ne postoji
mkdir -p api

if [ "$CHOICE" == "1" ]; then
    echo "➡️  Kreiram Python endpoint /api/compare.py..."
    cat > api/compare.py << 'PYEOF'
import json

def handler(request):
    """
    Vercel Python Serverless Function
    Endpoint: /api/compare
    """
    result = {
        "ok": True,
        "runtime": "python",
        "endpoint": "/api/compare",
        "message": "Python function alive"
    }
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
    }
PYEOF

    cat > requirements.txt << 'REQEOF'
# Add Python packages here if needed later
REQEOF

    git add api/compare.py requirements.txt
    git commit -m "add: Python /api/compare endpoint"
    git push

    echo ""
    echo "✅ Python endpoint kreiran!"
    echo "Testiraj: https://tvoj-projekt.vercel.app/api/compare"
    echo ""

elif [ "$CHOICE" == "2" ]; then
    echo "➡️  Kreiram Node/TS endpoint /api/compare.ts..."
    cat > api/compare.ts << 'TSEOF'
import type { VercelRequest, VercelResponse } from '@vercel/node';

export default async function handler(req: VercelRequest, res: VercelResponse) {
  res.status(200).json({
    ok: true,
    runtime: 'node',
    endpoint: '/api/compare',
    message: 'Node/TS function alive'
  });
}
TSEOF

    cat > tsconfig.json << 'TSCEOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "moduleResolution": "Node",
    "lib": ["ES2020", "DOM"],
    "esModuleInterop": true,
    "strict": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "outDir": "dist"
  },
  "include": ["api/**/*.ts", "src/**/*.ts", "src/**/*.tsx", "types/**/*.d.ts"]
}
TSCEOF

    echo "18" > .nvmrc

    mkdir -p types
    cat > types/papaparse.d.ts << 'DTEOF'
declare module 'papaparse';
DTEOF

    git add api/compare.ts tsconfig.json .nvmrc types/papaparse.d.ts
    git commit -m "add: Node/TS /api/compare endpoint"
    git push

    echo ""
    echo "✅ Node/TypeScript endpoint kreiran!"
    echo "Testiraj: https://tvoj-projekt.vercel.app/api/compare"
    echo ""

else
    echo "❌ Nevažeći unos. Pokreni skriptu ponovno i upiši 1 ili 2."
fi
