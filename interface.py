from flask import Flask, render_template
from flask_socketio import SocketIO, send
import flask
from glob import glob
import subprocess
import atexit
import os
import signal
import webview
import sys
import threading
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

process_id = None


def kill():
    global process_id

    if process_id is not None:
        try:
            os.killpg(os.getpgid(process_id.pid), signal.SIGTERM)
        except AttributeError:
            os.kill(process_id.pid, signal.CTRL_C_EVENT)
        process_id.kill()


@app.route('/')
def index():
    return render_template('ui.html')


@app.route('/get_profiles')
def get_profiles():
    files = glob("config/*.json")
    files = [os.path.splitext(f)[0] for f in files]

    return flask.jsonify({"files": ','.join(files)})


@app.route('/read_settings')
def read_settings():
    with open("static/settings/interface_settings.json") as json_file:
        settings_json = json.load(json_file)

    profile = settings_json["current_profile"]

    with open(f"config/{profile}.json") as json_file:
        settings_json = json.load(json_file)



@socketio.on('message', namespace='/stream')
def stream(cmd):
    global process_id

    popen = subprocess.Popen("python -u libs/interface_helper.py --config_file config/Default.json", stdout=subprocess.PIPE, universal_newlines=True)
    process_id = popen

    unique_images_processed = set()
    for stdout_line in iter(popen.stdout.readline, ""):
        print(stdout_line)
        if "[HAL-SIGM]:bar:" in stdout_line:
            subdata = stdout_line.split(":")
            files_val = subdata[2]
            ret_vals = f"{len(unique_images_processed) + 1},{files_val}"
            subdata[2] = ret_vals

            unique_images_processed.add(stdout_line)
            send(':'.join(subdata), namespace='/stream')
        else:
            send(stdout_line, namespace='/stream')

    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

    popen.kill()

    return


def start_server():
    socketio.run(app, port=6969)


if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    window = webview.create_window("", "http://127.0.0.1:6969/", min_size=(800, 600))
    window.closing += kill
    webview.start(debug=True)

    # To kill any process spawned that is separate from the interface, e.g. joblib-related processes
    atexit.register(kill)
    sys.exit()
