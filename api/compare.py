from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

METRICS = ["f1_score", "latency_ms", "false_positive_rate", "efficiency"]

MOCK_DATA = [
    {"domain": "Healthcare", "baseline": {"f1_score": 0.85}, "utl": {"f1_score": 0.92}},
    {"domain": "Finance", "baseline": {"f1_score": 0.78}, "utl": {"f1_score": 0.88}},
    {"domain": "Legal", "baseline": {"f1_score": 0.82}, "utl": {"f1_score": 0.89}},
]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        params = parse_qs(parsed_path.query)
        metric = params.get('metric', ['f1_score'])[0]
        
        response_data = {
            "ok": True,
            "metric": metric,
            "domains": MOCK_DATA,
            "timestamp": "2025-10-16T12:00:00Z"
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        return