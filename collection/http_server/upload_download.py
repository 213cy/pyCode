'''upload and download server'''
"""Simple HTTP Server With Upload.
This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.
https://github.com/freelamb/simple_http_server
"""

import os
import argparse
import signal

import shutil
import mimetypes
from html import escape
from io import BytesIO #, StringIO

from urllib.parse import quote
from urllib.parse import unquote
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler as F12toviewproto



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler with GET/HEAD/POST commands.
    This serves files from the current directory and any of its
    subdirectories. And can receive file uploaded
    by client.
    The GET/HEAD/POST requests are identical except that the HEAD
    request omits the actual contents of the file.
    """

    server_version = "server/version_in_Server_header_field"
    directory = 'os.getcwd()'

    mimetypes.init()  # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream',  # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
    })


    def do_GET(self):
        """Serve a GET request."""
        fd = self.send_head()
        if fd:
            shutil.copyfileobj(fd, self.wfile)
            fd.close()


    def do_HEAD(self):
        """Serve a HEAD request."""
        fd = self.send_head()
        if fd:
            fd.close()

    def do_POST(self):
        """Serve a POST request."""
        print('get post request from:', self.client_address)
        r, info = self.deal_post_data()
        print(info)
        f = BytesIO()
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(b"<html>\n<title>Upload Result Page</title>\n")
        f.write(b"<body>\n<h2>Upload Result Page</h2>\n")
        f.write(b"<hr>\n")
        if r:
            f.write(b"<strong>Success!</strong><br>")
        else:
            f.write(b"<strong>Failed!</strong><br>")
        f.write(info.encode('utf-8'))
        f.write(b"<hr><br><a href=\".\">back</a></body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            shutil.copyfileobj(f, self.wfile)
            f.close()

    def deal_post_data(self):
        boundary = self.headers["Content-Type"].split("=")[1].encode('utf-8')
        remain_bytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remain_bytes -= len(line)
        if boundary not in line:
            return False, "Content NOT begin with boundary"
        line = self.rfile.readline()
        remain_bytes -= len(line)
        
        fn = line.decode().split('filename="')[-1].split('"')[0]
        if not fn:
            return False, "Can't find out file (filename='"+fn+"')"
            
        fn = os.path.join(self.directory, fn)
        while os.path.exists(fn):
            fn += "_"
        line = self.rfile.readline()
        remain_bytes -= len(line)
        line = self.rfile.readline()
        remain_bytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return False, "Can't create file to write, do you have permission to write?"

        pre_line = self.rfile.readline()
        remain_bytes -= len(pre_line)
        while remain_bytes > 0:
            line = self.rfile.readline()
            remain_bytes -= len(line)
            if boundary in line:
                pre_line = pre_line[0:-1]
                if pre_line.endswith(b'\r'):
                    pre_line = pre_line[0:-1]
                out.write(pre_line)
                out.close()
                return True, "File upload to '%s' success!" % fn
            else:
                out.write(pre_line)
                pre_line = line
        return False, "Unexpect Ends of data."

    def send_head(self):
        """Common code for GET and HEAD commands.
        This sends the response code and MIME headers.
        Return value is either a file object (which has to be copied
        to the output file by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.
        """

        # abandon query parameters
        p = self.path.split('?', 1)[0]
        p = p.split('#', 1)[0]
        path = os.path.normpath(self.directory+unquote(p))
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        # ====================================================
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found <by me>")
            return None

        # Get a string form 'type/subtype' by the file's extension,
        # usable for a MIME Content-type header.
        base, ext = os.path.splitext(path)
        content_type = self.extensions_map.get(ext.lower(),'application/octet-stream')

        self.send_response(200)
        self.send_header("Content-type", content_type)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).
        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().
        """
        try:
            list_dir = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory <by me>")
            return None
        list_dir.sort(key=lambda a: a.lower())
        f = BytesIO()
        display_path = escape(unquote(self.path))
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(b"<html>\n<title>%s</title>\n" % self.directory.encode('utf-8'))
        f.write(b"<body>\n<h2>Directory listing for %s</h2>\n" % display_path.encode('utf-8'))
        f.write(b"<hr>\n")
        # 默认情况下，enctype的值是application/x-www-form-urlencoded,不能用于文件上传，
        # 只有使用了multipart/form-data，才能完整的传递文件数据。
        f.write(b"<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write(b"<input name=\"file\" type=\"file\"/>")
        f.write(b"<input type=\"submit\" value=\"upload\"/></form>\n")
        f.write(b"<hr>\n<ul>\n")
        for name in list_dir:
            fullname = os.path.join(path, name)
            display_name = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                display_name = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                display_name = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write(b'<li><a href="%s">%s</a>\n' % (quote(linkname).encode('utf-8'), escape(display_name).encode('utf-8')))
        f.write(b"</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f




def signal_handler(signal, frame):
    print("You choose to stop me.")
    exit()


def main():
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', '-d', default=os.path.expanduser('~')+'\\Desktop',
                    help='Specify alternative directory '
                    '[default:current directory]')
    args = parser.parse_args()
    print(args)

    # args.directory=os.getcwd()
    httpHandle = type('ccc',(SimpleHTTPRequestHandler,),{'directory':args.directory})

    httpd = HTTPServer( ('0.0.0.0', 8000), httpHandle)

    print("server_version: " + httpHandle.server_version + ", python_version: " + httpHandle.sys_version)
    print("Serving http on:  http://0.0.0.0:8000/",httpd.socket.getsockname())
    httpd.serve_forever()

if __name__ == '__main__':
    main()
