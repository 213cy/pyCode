"""
Remote python http server.
Execute Python commands remotely and send output back.
"""

import sys
from socket import socket, AF_INET, SOCK_STREAM
import io
import traceback
import webbrowser


PORT = 4127
BUFSIZE = 1024


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', PORT))
    s.listen(1)
    print('server is running...')
    while True:
        conn, (remotehost, remoteport) = s.accept()
        with conn:
            print('connection from', remotehost, remoteport)

            request = conn.recv(BUFSIZE)
            req = request.decode()
            # print(rep)
            command = req.split(' ')[1][1:]
            res = execute(command)

            resp = ("<html><body>"
                    "<h4>Execution of Python code throungh URL path</h4>"
                    "<p>Python code: </p><p>"+command+"</p>"
                    "<p>  >>> " + res.replace('\n', '<br />')  + "</p>"
                    "<hr />"
                    "<p>" + req.replace('\r\n', '<br />') + "</p>"
                    "</body></html>")

            # respo = "HTTP/1.1 200 OK\r\nContent-Length: "+str(len(resp))+"\r\n\r\n"+resp
            respo = "HTTP/1.1 200 OK\r\n\r\n"+resp

            # conn.send(respo.encode("ascii"))
            conn.send(respo.encode())
            # conn.close()


def execute(request):
    stdout = sys.stdout
    stderr = sys.stderr
    sys.stdout = sys.stderr = fakefile = io.StringIO()
    try:
        try:
            exec(request, {}, {})
        except:
            traceback.print_exc(100)
    finally:
        sys.stderr = stderr
        sys.stdout = stdout
    return fakefile.getvalue()

webbrowser.open(f"http://127.0.0.1:{PORT}/print(dir(list))")
try:
    main()
except KeyboardInterrupt:
    print("KeyboardInterrupt")
