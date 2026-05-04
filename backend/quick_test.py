import urllib.request
try:
    r = urllib.request.urlopen('http://127.0.0.1:5000/app.html', timeout=5)
    print("SUCCESS: 200 OK")
    print("Content-length:", len(r.read()))
    print("\nServer is working correctly!")
except urllib.error.HTTPError as e:
    print("FAIL: HTTP", e.code)
except Exception as e:
    print("FAIL:", e)
