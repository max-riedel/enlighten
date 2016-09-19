import cgi
import posixpath
import threading
import http.server
import socketserver
import subprocess
import os
import urllib.parse

__author__ = 'max'

# import main

PORT = 80
httpd = None

source = None
htdocs_path = os.path.realpath(os.path.realpath(__file__) + '/../../htdocs/')


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        global source
        string = "Hello there! I am " + threading.current_thread().name
        string += "<br>"
        string += "You just sent me:<br>"
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST"}
        )
        for item in form.list:
            string += "%s=%s" % (item.name, item.value)

        val = int(form.list[0].value, 16)
        source.color = (val >> (8 * 2), (val >> 8) & 0xFF, val & 0xFF)
        self.wfile.write(bytes(string, "utf-8"))

    def translate_path(self, path):
        """
        Changes webservers document root to htdocs
        :param path: path from HTTP query string
        :return: full path of file / directory to serve
        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        path = htdocs_path + "/" + path  # os.getcwd() retuns the directory of the main executable unless changed before
        return path


# def do_GET(self):
#     """Serve a GET request."""
#     """
#     f = self.send_head()
#     if f:
#         self.copyfile(f, self.wfile)
#         f.close()
#     """
#     string = "Hello there! I am " + threading.current_thread().name
#     self.wfile.write(bytes(string, "utf-8"))
#     #return True


def log_message(self, format, *args):
    """
    Silent the logs
    :param self:
    :param format:
    :param args:
    :return:
    """
    pass


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""


def init(source_local):
    global source
    source = source_local
    httpd = ThreadedHTTPServer(('', PORT), MyHandler)
    httpd_thread = threading.Thread(target=httpd.serve_forever)

    httpd_thread.start()
    # Finding out the IP is not trivial. But its worth a try!
    try:
        ip = subprocess.check_output("hostname -I", shell=True).split(b'\n')[0].decode('ascii').strip()
    except:
        ip = "localhost"
    print("Server running! Check out http://" + str(ip) + ':' + str(PORT))
