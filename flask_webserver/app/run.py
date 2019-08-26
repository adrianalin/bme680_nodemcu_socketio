from flask import Flask, render_template, Response, session, request
from flask_socketio import SocketIO
import eventlet
import json
import datetime
import time
import random
# If eventlet or gevent are used, then monkey
# patching the Python standard library is
# normally required to force the message
# queue package to use coroutine friendly
# functions and classes.
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

clients = []


@app.route('/')
def index():
    """
    Serve a JS page that upgrades you to a websocket.
    """
    return render_template('index.html')


@socketio.on('connect')
def on_connect():
    print('Client connected. ', request.sid)
    clients.append(request.sid)


@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected: ', request.sid)
    clients.remove(request.sid)


@socketio.on('my event')
def handle_my_event(json):
    print('received message from js_client', json)


@socketio.on('bme680_data')
def handle_bme680_data(data):
    temperature, pressure, humidity, gas = data.split(',')
    dict_data = {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'temperature': float(temperature),
        'pressure': float(pressure),
        'humidity': float(humidity),
        'gas': float(gas),
    }
    print('received data: ' + json.dumps(dict_data) + ' ' + request.sid)
    for client in clients:
        if client != request.sid:
            socketio.emit('js_client', json.dumps(dict_data), room=client)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
