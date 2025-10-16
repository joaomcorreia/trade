import http.server
import socketserver
import os

# Change to the project directory
os.chdir("C:/projects/trade")

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

Handler = MyHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🌐 Test server running at http://localhost:{PORT}")
    print(f"📄 Open: http://localhost:{PORT}/test_dashboard.html")
    print("💡 Press Ctrl+C to stop")
    httpd.serve_forever()