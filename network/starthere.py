
import requests
r=requests.get('https://www.httpbin.org/get')
print(r.status_code)
print(r.content.decode())


