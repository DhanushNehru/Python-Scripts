import cgi
import http.server
import socketserver
import os
from pywebcopy import save_webpage

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "index.html"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
        })
        url = form.getvalue('submitButton')
        urlN = 'https://' + str(url) +'/'
        isdir = os.path.isdir(url)
        if not isdir:
            kwargs = {'project_name': url}
            save_webpage(
                url=urlN,
                project_folder='./',
                **kwargs
            )
        path =  url + "/" + url + "/index.html"
        self.send_response(301)
        self.send_header('Location', path)
        self.end_headers()
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

PORT = 7000
s = socketserver.TCPServer(("127.0.0.1", PORT), RequestHandler)
s.serve_forever()