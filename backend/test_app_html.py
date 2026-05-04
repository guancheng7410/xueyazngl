import urllib.request
import sys

try:
    r = urllib.request.urlopen('http://127.0.0.1:5000/app.html', timeout=5)
    content = r.read().decode('utf-8')
    print("STATUS:", r.status)
    print("LENGTH:", len(content))
    print("FIRST_100:", content[:100])
except Exception as e:
    print("ERROR:", str(e))
