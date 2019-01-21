from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import urllib

class MainRequestHandler(BaseHTTPRequestHandler):
    """
    The request handler for the admin panel webpage
    It reads incoming logs from the Database Updater
    """

    def set_manager_dict(self, d):
        self.manager_dict = d

    def set_store_ids(self, d):
        self.store_ids = d

    def not_found(self):
        self.send_response(404)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "Not found \n Path: {}".format(self.path)
        self.wfile.write(bytes(message, "utf8"))

    def serve_static(self, header_type):
        base_path = 'admin_panel'
        #f = open(self.path[1:])
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

            elif self.path.startswith('/data-request'):
                self.send_response(200)

                self.send_header('Content-type','text/html')
                self.end_headers()

                store_id = int(self.path[14:])
                data = self.manager_dict[store_id]

                data_string = ''
                for l in data:
                    data_string += "<li>{}</li>".format(l)
                    
                self.wfile.write(bytes(data_string, "utf8"))

            elif self.path == ('/init-store-list'):
                self.send_response(200)

                self.send_header('Content-type','text/html')
                self.end_headers()

                data_string = ''
                for k, v in self.store_ids.items():
                    data_string += "<li data-id='{}'>{}</li>".format(k, v)
                    
                self.wfile.write(bytes(data_string, "utf8"))

            else:
                self.not_found()


        except IOError:
            self.not_found()
"""
def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, MainRequestHandler)
  print('running server...')
  httpd.serve_forever()
"""
 