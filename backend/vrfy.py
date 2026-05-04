import urllib.request, sys
r = urllib.request.urlopen('http://127.0.0.1:5000/app.html', timeout=10)
print('OK', r.status)
sys.exit(0 if r.status == 200 else 1)
