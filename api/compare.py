from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import parse_qs, urlparse

METRICS = ["f1_score", "latency_ms", "false_positive_rate", "efficiency"]

MOCK_DATA = [
    {"domain": "Healthcare", "baseline": {"f1_score": 0.85, "latency_ms": 120}, "utl": {"f1_score": 0.92, "latency_ms": 95}},
    {"domain": "Finance", "baseline": {"f1_score": 0.78, "latency_ms": 150}, "utl": {"f1_score": 0.88, "latency_ms": 110}},
    {"domain": "Legal", "baseline": {"f1_score": 0.82, "latency_ms": 135}, "utl": {"f1_score": 0.89, "latency_ms": 100}},
]

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            metric = params.get('metric', ['f1_score'])[0]
            
            response = {"ok": True, "metric": metric, "domains": MOCK_DATA}
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())
