cat > api/test.py << 'EOF'
def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': '{"ok": true, "message": "Python radi!", "version": 2}'
    }
EOF