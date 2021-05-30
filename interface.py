from flask import Flask, render_template
from flask_socketio import SocketIO, send
import flask
import webview
import sys
import threading
import time
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('ui.html')


@socketio.on('message', namespace='/stream')
def stream(cmd):
    import subprocess

    popen = subprocess.Popen("python -u cli.py --interface", stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        print(stdout_line)
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

    webview.create_window("HerbASAP Lite", "http://127.0.0.1:6969/", min_size=(800, 600))
    webview.start(debug=True)
    sys.exit()