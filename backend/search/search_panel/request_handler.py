from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import urllib

class MainRequestHandler(BaseHTTPRequestHandler):

    def set_search_interface(self, si):
        self.search_interface = si

    def not_found(self):
        self.send_response(404)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "Not found \n Path: {}".format(self.path)
        self.wfile.write(bytes(message, "utf8"))

    def serve_static(self, header_type):
        base_path = 'admin_panel'
        f = open(base_path + self.path)

        self.send_response(200)

        self.send_header('Content-type', header_type)
        self.end_headers()

        self.wfile.write(bytes(f.read(), "utf8"))
        f.close()
        return

    def do_GET(self):
        try:
            if self.path.endswith('.html'):
                self.serve_static('text/html')

            elif self.path.endswith('.css'):
                self.serve_static('text/css')

            elif self.path.endswith('.js'):
                self.serve_static('text/js')

            if self.path.startswith('query'):
                query_string = ''
                results = self.search_interface.search(query_string)

            else:
                self.not_found()


        except IOError:
            self.not_found()