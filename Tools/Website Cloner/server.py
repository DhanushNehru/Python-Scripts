import cgi
import http.server
import socketserver
import os
from pywebcopy import save_webpage

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "index.html"
        try:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode("utf-8")

        # Parse the URL from the form submission
        form = cgi.parse_qs(post_data)
        url = form.get("submitButton", [""])[0]

        if not url:
            self.send_error(400, "Bad Request: URL is missing")
            return

        urlN = "https://" + url.strip("/")
        project_folder = os.path.join('./cloned_sites', url.replace("https://", "").replace("http://", ""))

        if not os.path.isdir(project_folder):
            os.makedirs(project_folder, exist_ok=True)
            try:
                save_webpage(
                    url=urlN,
                    project_folder=project_folder,
                    project_name=url.replace("https://", "").replace("http://", "")
                )
            except Exception as e:
                self.send_error(500, f"Error cloning website: {e}")
                return

        path = os.path.join(project_folder, "index.html")
        if not os.path.isfile(path):
            self.send_error(404, "Cloned page not found")
            return

        self.send_response(301)
        self.send_header("Location", "/" + path)
        self.end_headers()


PORT = 7000
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("127.0.0.1", PORT), RequestHandler) as s:
    s.allow_reuse_address = True
    print(f"Server running on http://127.0.0.1:{PORT}")
    s.serve_forever()
