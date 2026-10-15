"""Local preview of public/weekly with caching disabled:  python3 "weekly/Project Data/serve_site.py"  then open http://127.0.0.1:8765/weekly/"""
import http.server, os
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "public"))
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate"); self.send_header("Expires", "0")
        super().end_headers()
    def log_message(self, *a): pass
print("serving public/ at http://127.0.0.1:8765/weekly/", flush=True)
http.server.ThreadingHTTPServer(("127.0.0.1", 8765), H).serve_forever()
