# server.py

import http.server
import socketserver

PORT = 8000
DIRECTORY = 'templates/ssr'  # Pfad zum dist-Ordner deiner Angular-Anwendung

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving Angular app at http://localhost:{PORT}")
    httpd.serve_forever()
