import urllib.request

results = []

test_urls = [
    'http://127.0.0.1:5000/',
    'http://127.0.0.1:5000/app.html',
    'http://127.0.0.1:5000/manifest.json',
    'http://127.0.0.1:5000/sw.js',
    'http://127.0.0.1:5000/api/health',
]

for url in test_urls:
    try:
        r = urllib.request.urlopen(url, timeout=5)
        results.append(f"OK  {url}  ->  {r.status}")
    except urllib.error.HTTPError as e:
        results.append(f"ERR {url}  ->  HTTP {e.code}")
    except Exception as e:
        results.append(f"ERR {url}  ->  {type(e).__name__}: {e}")

with open('test_result.txt', 'w') as f:
    f.write('\n'.join(results))
print("Done")
