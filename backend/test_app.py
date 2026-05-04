import sys
sys.path.insert(0, '.')

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting Flask application...")
    print("Routes registered:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule.rule} {list(rule.methods)}")

    print("\nTrying to start server...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
