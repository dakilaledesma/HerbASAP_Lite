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

_cli = None

@app.route('/')
def index():
    return render_template('ui.html')


@app.route('/load')
def load_interface():
    import cli
    from cli import process
    return_string = """
    <div class="row">
        <div class="column left">
            <br>
            <img style="max-width: 70%; height: auto;" src="../static/images/icon_a.png" alt="HerbASAP Logo">
        </div>
        <div class="column middle">
            hey hey
        </div>
        <div class="column right">
            <p id="consoleout"></p>
        </div>
    </div>
    """

    return flask.jsonify({"return_string": return_string})


@socketio.on('message', namespace='/stream')
def stream(cmd):
    import subprocess

    popen = subprocess.Popen("python -u cli.py", stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        print(stdout_line)
        send(stdout_line, namespace='/stream')
        # yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def start_server():
    socketio.run(app, port=6969)
    # app.run(host='0.0.0.0', port=6969)


if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window("HerbASAP Lite", "http://127.0.0.1:6969/", min_size=(800, 600))
    webview.start()
    sys.exit()