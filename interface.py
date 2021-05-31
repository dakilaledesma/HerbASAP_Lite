from flask import Flask, render_template
from flask_socketio import SocketIO, send
import subprocess
import atexit
import flask
import os
import signal
import webview
import sys
import threading
import time
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

process_id = None

class Api:
    def __init__(self):
        self._window = None

    def set_window(self, window):
        self._window = window

    def quit(self):
        window.destroy()

    def minimize(self):
        window.minimize()

    def change_title(self):
        """changes title every 3 seconds"""
        popen = subprocess.Popen("python -u cli.py --interface", stdout=subprocess.PIPE, universal_newlines=True)

        unique_images_processed = set()
        for stdout_line in iter(popen.stdout.readline, ""):
            window.set_title(stdout_line)

        popen.stdout.close()
        return_code = popen.wait()
        popen.kill()
        del popen

        # for i in range(1, 100):
        #     time.sleep(1)
        #     window.set_title('New Title #{}'.format(i))


def kill():
    global process_id
    try:
        os.killpg(os.getpgid(process_id.pid), signal.SIGTERM)
    except AttributeError:
        os.kill(process_id.pid, signal.CTRL_C_EVENT)
    process_id.kill()


@app.route('/')
def index():
    return render_template('ui.html')


@socketio.on('message', namespace='/stream')
def stream(cmd):
    global process_id

    popen = subprocess.Popen("python -u cli.py --interface", stdout=subprocess.PIPE, universal_newlines=True)
    process_id = popen

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
    window = webview.create_window("", "http://127.0.0.1:6969/", min_size=(800, 600), js_api=api)
    window.closing += kill
    webview.start(debug=True)
    api.set_window(window)

    atexit.register(kill)

    sys.exit()
