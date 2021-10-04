import datetime
import time
import os
import paho.mqtt.client as mqtt
import json
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

broker= "192.168.178.32"
port = 1883
topic = "KVB_status/#"

class kvb_matrix(object):
    def __init__(self):
        super(kvb_matrix, self).__init__()
    def reset_matrix(self):
        self.matrix.Clear()
        offscreen_canvas.Clear()  

    def init_led_matrix(self):
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat' 

        self.matrix = RGBMatrix(options = options)

        white = graphics.Color(255, 255, 255)
        gray = graphics.Color(127, 127, 127)
        green = graphics.Color(0, 150, 0)
        yellow = graphics.Color(127, 127, 0)
        red = graphics.Color(150, 0, 0)
        blue = graphics.Color(0, 0, 150)
        magenta = graphics.Color(127, 0, 127)
        cyan = graphics.Color(0, 127, 127)
        dim = graphics.Color(10, 10, 10)

        global offscreen_canvas

        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()

        width = 128
        height = 64
        font_medium = graphics.Font()
        font_medium.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf")
        font_small = graphics.Font()
        font_small.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf")
        font_big = graphics.Font() 
        font_big.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/9x15.bdf")

        graphics.DrawText(offscreen_canvas, font_small, 0, 0, cyan, "text")

        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

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
    my_kvb_matrix = kvb_matrix()
    my_kvb_matrix.init_led_matrix()
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()