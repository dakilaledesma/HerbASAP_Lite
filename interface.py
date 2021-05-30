from flask import Flask, render_template
from flask_socketio import SocketIO, send
import subprocess
import flask
import webview
import sys
import threading
import time
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


class Api:
    def __init__(self):
        self._window = None

    def set_window(self, window):
        self._window = window

    def quit(self):
        window.destroy()

    def minimize(self):
        window.minimize()


@app.route('/')
def index():
    return render_template('ui.html')


@app.route('/dummy')
def dummy():
    return ""


@socketio.on('message', namespace='/stream')
def stream(cmd):
    popen = subprocess.Popen("python -u cli.py --interface", stdout=subprocess.PIPE, universal_newlines=True)

    unique_images_processed = set()
    for stdout_line in iter(popen.stdout.readline, ""):
        print(stdout_line)
        if "[HAL-SIGM]:bar:" in stdout_line:
            subdata = stdout_line.split(":")
            files_val = subdata[2].split(",")[1]
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

    api = Api()
    window = webview.create_window("HerbASAP Lite", "http://127.0.0.1:6969/", min_size=(800, 600), frameless=True,
                                   easy_drag=False, js_api=api)
    webview.start(debug=True)
    api.set_window(window)

    sys.exit()
