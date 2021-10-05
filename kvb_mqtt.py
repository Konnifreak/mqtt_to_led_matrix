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

def inti_matrix():
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.hardware_mapping = 'adafruit-hat'
    global matrix
    matrix = RGBMatrix(options = options)

def reset_matrix():
    matrix.Clear()
    offscreen_canvas.Clear()  

def print_led_matrix(Linie, message, Haltestelle):
 
    cyan = graphics.Color(0, 127, 127)

    global offscreen_canvas

    offscreen_canvas = matrix.CreateFrameCanvas()

    font_medium = graphics.Font()
    font_medium.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf")
    font_small = graphics.Font()
    font_small.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf")
    font_big = graphics.Font() 
    font_big.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/9x15.bdf")

    pos_scroll = 0
    t_end = time.time() + 60

    while time.time() < t_end:
    
        graphics.DrawText(offscreen_canvas, font_small, 0, 7, cyan, Linie)
        graphics.DrawText(offscreen_canvas, font_small, pos_scroll, 18, cyan, message)
        graphics.DrawText(offscreen_canvas, font_small, pos_scroll, 26, cyan, Haltestelle)

        pos_scroll -= 1

        if pos_scroll + len(message) == 0:
            pos_scroll = 64

        time.sleep(0.05)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


    print("End of Matrix")

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

    print_led_matrix(Linie, message, Haltestelle)
    reset_matrix()
    

def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        print_infos(msg)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    inti_matrix()
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()