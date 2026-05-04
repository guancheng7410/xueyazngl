"""
Blood Pressure Guardian - Minimal Standalone Server
Zero dependencies, pure Python standard library only.
Serves static files + provides a basic API endpoint.
"""
import http.server
import socketserver
import os
import sys
import json
import urllib.parse
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
PORT = 5000

print("=" * 50)
print("  Blood Pressure Guardian Server")
print(f"  Static root: {PROJECT_ROOT}")
print(f"  Port: {PORT}")
print("=" * 50)

class BPHandler(http.server.SimpleHTTPRequestHandler):
    """Serves static files from project root + API endpoints."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROJECT_ROOT, **kwargs)
    
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == '/api/health':
            self._json({'status': 'ok', 'service': 'BP Guardian', 'time': datetime.datetime.now().isoformat()})
        elif path == '/api/debug':
            files = os.listdir(PROJECT_ROOT) if os.path.exists(PROJECT_ROOT) else []
            html_files = [f for f in files if f.endswith('.html')]
            self._json({
                'project_root': PROJECT_ROOT,
                'html_files': html_files,
                'all_files': files,
                'note': 'This is a minimal debug endpoint',
            })
        elif path == '/api/auth/login':
            self._json({'openid': 'demo', 'id': 1, 'nickname': 'Demo User'}, 201)
        elif path == '/api/family/groups' and parsed.query:
            self._json({'id': 1, 'name': 'My Family'})
        elif path.startswith('/api/'):
            self._json({'data': [], 'note': 'No data yet - minimal API mode'})
        else:
            super().do_GET()
    
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''
        
        if path == '/api/auth/login':
            try:
                data = json.loads(body) if body else {}
            except:
                data = {}
            self._json({
                'id': 1,
                'openid': data.get('openid', 'demo'),
                'nickname': data.get('nickname', 'User'),
                'phone': data.get('phone', ''),
                'role': data.get('role', 'child'),
            }, 201)
        elif path == '/api/family/groups':
            try:
                data = json.loads(body) if body else {}
            except:
                data = {}
            self._json({
                'id': 1,
                'name': data.get('name', 'My Family'),
                'invite_code': 'DEMO01',
            }, 201)
        elif path.startswith('/api/family/groups/') and path.endswith('/parents'):
            try:
                data = json.loads(body) if body else {}
            except:
                data = {}
            self._json({
                'id': 1,
                'name': data.get('name', 'Parent'),
                'age': data.get('age', 65),
                'gender': data.get('gender', 'male'),
            }, 201)
        elif path.startswith('/api/medications'):
            self._json({'id': 1, 'name': 'Demo Med', 'times': ['08:00', '18:00']}, 201)
        elif path.startswith('/api/blood-pressure'):
            self._json({'id': 1, 'systolic': 120, 'diastolic': 80}, 201)
        elif path.startswith('/api/logs/generate-daily'):
            self._json({'message': 'Generated 0 logs', 'count': 0})
        elif path.startswith('/api/'):
            self._json({'status': 'ok', 'note': 'Minimal API - demo mode'})
        else:
            self.send_error(404)
    
    def do_PUT(self):
        self._json({'status': 'ok'})
    
    def do_DELETE(self):
        self._json({'status': 'ok'})
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        self.end_headers()
    
    def _json(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def log_message(self, format, *args):
        print(f"{self.address_string()} {format % args}")


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main():
    global PORT
    
    # Try to kill existing process on port
    import subprocess
    try:
        r = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, shell=True)
        for line in r.stdout.split('\n'):
            if f':{PORT}' in line and 'LISTENING' in line:
                parts = line.strip().split()
                pid = parts[-1]
                print(f"[!] Found old server PID={pid} on port {PORT}, killing...")
                subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True, shell=True)
                import time
                time.sleep(2)
                break
    except Exception as e:
        print(f"[!] Could not auto-kill: {e}")
    
    # Try multiple ports
    for p in [PORT, PORT+1, PORT+2]:
        try:
            server = ReusableTCPServer(('0.0.0.0', p), BPHandler)
            PORT = p
            break
        except OSError:
            print(f"[!] Port {p} busy, trying {p+1}...")
            continue
    else:
        print("[ERROR] No available port!")
        return
    
    print(f"\n  Server running on http://localhost:{PORT}")
    print(f"  Project root: {PROJECT_ROOT}")
    print(f"\n  Press Ctrl+C to stop\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")


if __name__ == '__main__':
    main()
