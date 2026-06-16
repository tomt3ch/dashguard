#!/usr/bin/env python3
"""DashGuard local HTTPS server — run this, then open the URL on your iPhone."""
import http.server, ssl, socket, os, sys

PORT = 8443

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"  [{self.address_string()}] {args[0]} {args[1]}")
    def end_headers(self):
        # Required for GPS on iPhone over local HTTPS
        self.send_header('Permissions-Policy', 'geolocation=*')
        super().end_headers()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
local_ip = s.getsockname()[0]
s.close()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('cert.pem'):
    print("Generating self-signed certificate…")
    os.system(
        f'openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem '
        f'-days 365 -nodes -subj "/CN={local_ip}" '
        f'-addext "subjectAltName=IP:{local_ip},IP:127.0.0.1" 2>/dev/null'
    )
    print("Certificate created.\n")

httpd = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('cert.pem', 'key.pem')
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

print("╔══════════════════════════════════════════════╗")
print("║        DashGuard — local HTTPS server        ║")
print("╠══════════════════════════════════════════════╣")
print(f"║  Open on your iPhone (Safari):               ║")
print(f"║  https://{local_ip}:{PORT:<5}                  ║")
print("╠══════════════════════════════════════════════╣")
print("║  ⚠  Tap Advanced → Proceed to accept cert    ║")
print("║  📍 GPS needs HTTPS — this handles it        ║")
print("║  🔇 Keep phone off silent for voice alerts   ║")
print("╚══════════════════════════════════════════════╝")
print("\n  Ctrl-C to stop.\n")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
