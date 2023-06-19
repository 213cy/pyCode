"""mp4 player http server
https://github.com/freelamb/simple_http_server
"""

import os
import argparse
import signal
import shutil
import mimetypes
from html import escape
from io import BytesIO  # , StringIO


from urllib.parse import quote , unquote
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler as F12toviewproto


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

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

    def log_request(self, code='-', size='-'):
        # 127.0.0.1 - - [02/Apr/2023 15:32:39] "GET /%5B%5D/9.mp4 HTTP/1.1" 206 -
        print('request from: {}:{}'.format( *self.client_address) )
        print(unquote( self.raw_requestline.decode())[0:-2] ,'(\\r\\n)')
        if "Range" in self.headers:
            # print(self.headers.keys())
            print('Range:', self.headers['Range'])
        print('response status code:' ,code,'[{}]'.format(self.log_date_time_string()))

    def do_HEAD(self):
        print(30*'='+' HEAD Response Done! ')

    def do_POST(self):
        print(30*'='+' POST Response Done! ')

    def do_GET(self):
        """Serve a GET request."""
        path_file = os.path.normpath(self.directory+unquote(self.path))
        if os.path.isdir(path_file):
            self.send_dir(path_file)
        elif path_file.endswith('.mp4'):

            if "Range" in self.headers:
                self.send_mp4(path_file)
            else:
                # self.send_player(path_file)
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()

                self.wfile.write(b'<video controls autoplay>')
                self.wfile.write(b'<source src="%s"' % self.path.encode())
                self.wfile.write(b' type="video/mp4"></video>')
                # self.wfile.write(b'<video src="%s" controls></video>' % self.path.encode())

        else:
            self.send_file(path_file)

        print(30*'='+' GET Response Done! ')


    def send_mp4(self, mp4):
        N = 32
        READ_BUFFER_SIZE = 64*1024

        try:
            f = open(mp4, 'rb')
        except IOError:
            self.send_error(404, "File not found <by me>")

        self.send_response(206, "Partial Content")
        self.send_header("Content-Type", 'video/mp4')

        fs = os.fstat(f.fileno())
        filesize = fs[6]
        # filesize = os.path.getsize(mp4)
        # print(os.path.getsize(mp4),filesize)
        s, e = self.headers['range'].split('bytes=')[-1].split('-')
        start = int(s)
        if e:  # == '1' :
            end = int(e)
        else:
            # window下的chrome 请求的range形式总为 'x-' ,就是不给结束字节的位置
            # 服务器自由决定发送的长度,这对服务器友好
            # 这里默认的长度是  N*READ_BUFFER_SIZE
            end = min(start+N*READ_BUFFER_SIZE-1, filesize-1)

        # end = min(start+N*READ_BUFFER_SIZE-1, filesize-1)

        bytes_left = end-start+1
        debugdataA = bytes_left
        self.send_header("Content-Length", str(bytes_left))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", "bytes %d-%d/%d" %
                         (start, end, filesize))
        self.send_header("Content-Transfer-Encoding", "binary")
        self.send_header("Connection", "close")
        # self.send_header("Connection", "keep-alive")
        self.end_headers()

        f.seek(start)

        # for k in range(N):
        #     buf = f.read(READ_BUFFER_SIZE)
        #     self.wfile.write(buf)
        #     self.wfile.flush()

        while bytes_left > 0:
            bytes_read = min(READ_BUFFER_SIZE, bytes_left)
            buf = f.read(bytes_read)
            try:
                self.wfile.write(buf)
                self.wfile.flush()
            except Exception as e:
                # ios下的safari 请求的range形式总为 'x-filelastbyte' ,
                # 就是结束字节的位置始终为文件最后一个字节
                # 服务器接到的任务总是要尽量多的传输文件内容
                # 而客户端会根据情况中断连接,这尽量提高了传输效率,
                # 代价是服务器在客户端的忽悠下频繁处理异常??
                print(e)
                print(debugdataA, bytes_left, debugdataA-bytes_left, bytes_read)
                f.close()
                return
            bytes_left -= bytes_read

        f.close()

    def send_file(self, file):
        try:
            f = open(file, 'rb')
        except IOError:
            self.send_error(404, "File not found <by me>")
            return

        self.send_response(200)
        base, ext = os.path.splitext(file)
        content_type = self.extensions_map.get(
            ext.lower(), 'application/octet-stream')
        self.send_header("Content-type", content_type)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()

        shutil.copyfileobj(f, self.wfile)
        f.close()

    def send_dir(self, dir):
        try:
            list_dir = os.listdir(dir)
        except os.error:
            self.send_error(404, "No permission to list directory <by me>")

        list_dir.sort(key=lambda a: a.lower())
        f = BytesIO()
        display_path = escape(unquote(self.path))
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(b"<html>\n<title>file list</title>\n")
        f.write(b"<body>\n<h2>Directory listing for %s</h2>\n" %
                display_path.encode())
        f.write(b"[%s]" % self.directory.encode())
        f.write(b"<hr>\n<ul>\n")
        for name in list_dir:
            fullname = os.path.join(dir, name)
            if os.path.isdir(fullname):
                f.write(b'<li><a href="%s/">%s/.</a>\n'
                        % (quote(name).encode(), escape(name).encode()))
            else:
                f.write(b'<li><a href="%s">%s</a>\n'
                        % (quote(name).encode(), escape(name).encode()))
        f.write(b"</ul>\n</body>\n</html>\n")

        length = f.tell()

        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-Length", str(length))
        self.end_headers()

        shutil.copyfileobj(f, self.wfile)
        f.close()


def signal_handler(signal, frame):
    print("You choose to stop me.")
    exit()


def main():
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', '-d', default=os.getcwd(),
                        help='Specify alternative directory '
                        '[default:current directory]')
    args = parser.parse_args()
    print(args)

    args.directory = 'F:\\lover\\video'
    httpHandle = type('dummyhandler', (SimpleHTTPRequestHandler,),
                      {'directory': args.directory})

    # 127.0.0.1 只能用于本机'localhost',无法向网络中发送数据,也无法接收网络数据
    # 0.0.0.0 表示'网络中的本机' 可以用于局域网访问
    # httpd = HTTPServer(('127.0.0.1', 8000), httpHandle)
    httpd = HTTPServer(('0.0.0.0', 8000), httpHandle)

    print("server_version: " + httpHandle.server_version +
          ", python_version: " + httpHandle.sys_version)
    print("Serving http on:  http://0.0.0.0:8000/", httpd.socket.getsockname())
    print(33*'=')
    httpd.serve_forever()


if __name__ == '__main__':
    main()
