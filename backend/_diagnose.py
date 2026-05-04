import sys, os, json

os.chdir(os.path.dirname(os.path.abspath(__file__)))

sys.stderr.write("=== FULL DIAGNOSTIC ===\n")

sys.stderr.write(f"Python: {sys.executable} {sys.version}\n")
sys.stderr.write(f"CWD: {os.getcwd()}\n")

sys.path.insert(0, os.getcwd())

try:
    from app import create_app
    sys.stderr.write("[OK] Imported create_app\n")
except Exception as e:
    sys.stderr.write(f"[FAIL] Import: {e}\n")
    import traceback; traceback.print_exc()
    sys.exit(1)

try:
    app = create_app()
    sys.stderr.write("[OK] create_app() succeeded\n")
except Exception as e:
    sys.stderr.write(f"[FAIL] create_app: {e}\n")
    import traceback; traceback.print_exc()
    sys.exit(1)

sys.stderr.write(f"Routes registered:\n")
all_routes = {}
for rule in app.url_map.iter_rules():
    methods = sorted(rule.methods - {'HEAD', 'OPTIONS'})
    all_routes[rule.rule] = methods
    sys.stderr.write(f"  {rule.rule} -> {methods}\n")

result = {
    'routes': all_routes,
    'has_root': '/' in all_routes,
    'has_api_debug': '/api/debug' in all_routes,
    'has_api_health': '/api/health' in all_routes,
    'total_routes': len(all_routes),
    'python': sys.executable,
}

with open('test_result.json', 'w') as f:
    json.dump(result, f, indent=2)
sys.stderr.write(f"\nResult written to test_result.json\n")
sys.stderr.write(f"Has /api/debug: {result['has_api_debug']}\n")
sys.stderr.write(f"Has /: {result['has_root']}\n")
sys.stderr.write("=== DONE ===\n")
