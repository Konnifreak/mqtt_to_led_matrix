import paho.mqtt.client as mqtt
import json
#from rgbmatrix import RGBMatrix, RGBMatrixOptions

broker= "mqtt_host_ip"
port = 1883
topic = "KVB_status/#"

#def init_led_matrix():
#    options = RGBMatrixOptions()
#    options.rows = 32
#    options.cols = 64
#    options.chain_length = 1
#    options.parallel = 1
#    options.hardware_mapping = 'adafruit-hat' 

def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client("Raspi_test")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def print_infos(msg):
    payload = json.loads(msg.payload.decode())
    Linie = payload["Linie"]
    message = payload["message"]
    Haltestelle = payload["stations"]
    print(Linie)
    print(message)
    print(Haltestelle)
    

def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        print_infos(msg)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()