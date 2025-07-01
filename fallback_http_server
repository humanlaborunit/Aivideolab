from http.server import SimpleHTTPRequestHandler, HTTPServer

class FallbackHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"This is the fallback HTTP server. Your main UI likely crashed.")

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 3000), FallbackHandler)
    print("🛟 Fallback HTTP server running on port 3000...")
    server.serve_forever()