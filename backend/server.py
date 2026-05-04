import sys, os, time, socket, subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_run.log')

def w(msg):
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg, flush=True)

w("=== Server starting ===")
w(f"Python: {sys.executable}")
w(f"CWD: {os.getcwd()}")

def kill_port():
    try:
        r = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, shell=True)
        killed = False
        for line in r.stdout.split('\n'):
            if ':5000' in line and 'LISTENING' in line:
                parts = line.strip().split()
                pid = parts[-1]
                w(f"Killing PID {pid} on port 5000")
                subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True, shell=True)
                killed = True
        if not killed:
            w("No process on port 5000")
    except Exception as e:
        w(f"kill_port error: {e}")

kill_port()
time.sleep(1)

try:
    w("Importing create_app...")
    from app import create_app
    w("App created")
    
    from app import create_app
    app = create_app()
    
    route_list = []
    for rule in app.url_map.iter_rules():
        methods = sorted(rule.methods - {'HEAD', 'OPTIONS'})
        route_list.append(f"  {rule.rule} {methods}")
    w(f"Routes ({len(route_list)}):\n" + '\n'.join(route_list))
    
    w("Starting server on 0.0.0.0:5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
except Exception as e:
    import traceback
    tb = traceback.format_exc()
    w(f"ERROR: {e}\n{tb}")
    time.sleep(10)
