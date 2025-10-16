cd /c/Users/.../Livefeed_Hazard

cat > api/test.py << 'EOF'
def handler(request):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': '{"ok": true, "message": "Python API radi!", "test": "success"}'
    }
EOF