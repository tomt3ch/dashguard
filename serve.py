#!/usr/bin/env python3
"""Local HTTPS server for DashGuard V9.

Run:
  python3 serve.py

Then open the shown https://IP:8443 URL on your iPhone in Safari.
"""
import http.server, ssl, socket, os, subprocess, sys

PORT = 8443

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Permissions-Policy', 'geolocation=*')
        self.send_header('Cache-Control', 'no-store, max-age=0')
        super().end_headers()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    finally:
        s.close()

local_ip = get_ip()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('cert.pem'):
    print("Generating self-signed certificate...")
    cmd = [
        'openssl','req','-x509','-newkey','rsa:2048',
        '-keyout','key.pem','-out','cert.pem','-days','365','-nodes',
        '-subj',f'/CN={local_ip}',
        '-addext',f'subjectAltName=IP:{local_ip},IP:127.0.0.1'
    ]
    subprocess.run(cmd, check=True)

httpd = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('cert.pem', 'key.pem')
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

print("\nDashGuard V9 Map Only")
print("=====================")
print(f"Open on iPhone Safari: https://{local_ip}:{PORT}")
print("Accept the certificate warning: Advanced -> Proceed")
print("Ctrl-C to stop.\n")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
