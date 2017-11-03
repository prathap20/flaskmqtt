# coding=utf-8
import json
import eventlet
import requests


from flask import Flask,request,render_template,jsonify
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = ''
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'iot.eclipse.org'
#app.config['MQTT_BROKER_URL'] = '127.0.0.1'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap =Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pushData', methods=['POST'])
def push_data():
    dev_id = request.json.get('dev_id')
    hardware_serial = request.json.get('hardware_serial')
    downlink_url = request.json.get('downlink_url')
    payload_raw = request.json.get('payload_raw')
    #if more hex value like string
    value = int(payload_raw.decode('base64').encode('hex')[-2:], 16)
    #if single hex value
    #value = int(payload_raw.decode('base64').encode('hex'),16)
    print 'VALUE INT: %s'%value
    data = {'topic':'abc','message':value}
    json_str = json.dumps(data)
    handle_publish(json_str)
    return jsonify(message='pushed '+str(value)+' success'), 200

@app.route('/sendData', methods=['POST'])
def send_data():
    dev_id = request.json.get('dev_id')
    payload_raw = request.json.get('payload_raw')
    value = '{0:02x}'.format(payload_raw).decode('hex').encode('base64')
    print 'VALUE BASE64 :%s' % value
    data = {'dev_id':dev_id,'payload_raw':value}
    #response = requests.post(url='http://172.16.0.154:2021/pushData', json = data)
    response = requests.post(url='https://prathap.localtunnel.me/pushData', json = data)
    #response = requests.post(url='ENTER URL', json = data)
    if response.status_code == requests.codes.ok:
        return jsonify(message='sent '+str(value)+' successfully'), 200
    else:
        return jsonify(message='ERROR NOT SENT'), 500


@socketio.on('publish')
def handle_publish(json_str):
    data=json.loads(json_str)
    mqtt.publish(data['topic'], data['message'])


@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic = message.topic,
        payload = message.payload.decode()
    )
    socketio.emit('mqtt_message', data=data)


@mqtt.on_log()
def handle_logging(client,userdata, level, buf):
    print (level,buf)

if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000))
    socketio.run(app,host='0.0.0.0', port=2021, use_reloader=True, debug=True)
    #socketio.run(app)