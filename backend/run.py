import sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())
from server import w
from app import create_app
try:
    app = create_app()
    w("=== Server starting ===")
    w("App created successfully")
    route_list = []
    for rule in app.url_map.iter_rules():
        methods = sorted(rule.methods - {'HEAD', 'OPTIONS'})
        route_list.append(f"  {rule.rule} {methods}")
    w(f"Routes ({len(route_list)}):\n" + '\n'.join(route_list))
    w("Starting server on 0.0.0.0:5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
except Exception as e:
    import traceback
    w(f"ERROR: {e}\n{traceback.format_exc()}")
    input("Press Enter to exit...")
