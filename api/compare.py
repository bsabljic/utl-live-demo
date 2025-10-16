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
