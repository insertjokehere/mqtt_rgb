import paho.mqtt.client as mqtt
import time
import json
import unicornhat as unicorn
import argparse
import signal
import sys


class App():

    def _init_unicorn(self):
        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(self.args.rotation)
        unicorn.brightness(0.2)
        time.sleep(1)

    def on_term(self, *args, **kwargs):
        unicorn.off()
        self.client.disconnect()
        sys.exit(0)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("{}/pixel/#".format(self.args.prefix))
        self.client.subscribe("{}/brightness".format(self.args.prefix))

    def on_message(self, client, userdata, msg):

        if msg.topic.startswith("{}/pixel".format(self.args.prefix)):
            self.on_pixel_message(client, userdata, msg)
        elif msg.topic == "{}/brightness".format(self.args.prefix):
            self.on_brightness_message(client, userdata, msg)

    def on_brightness_message(self, client, userdata, msg):
        try:
            unicorn.brightness(float(msg.payload.decode('utf-8')))
            unicorn.show()
        except Exception as e:
            print("Failed to update brightness: {}".format(e))

    def on_pixel_message(self, client, userdata, msg):

        _, x, y = msg.topic.rsplit("/", 2)

        try:
            colour = json.loads(msg.payload.decode('utf-8'))

            unicorn.set_pixel(int(x), int(y),
                              int(colour['r']), int(colour['g']), int(colour['b']))
        except:
            print("Failed to decode payload for pixel {},{}".format(x, y))

        unicorn.show()

    def _connect(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(self.args.mqtt_host, self.args.mqtt_port, 60)

    def _run(self):
        self.client.loop_forever()

    def build_args(self):
        parser = argparse.ArgumentParser(description='MQTT to Unicorn bridge')
        parser.add_argument('--brightness', type=float, help="This setting is not used anymore")
        parser.add_argument('--rotation', type=int, default=0)
        parser.add_argument('--prefix', type=str, default="unicorn")
        parser.add_argument('--mqtt-host', default="localhost")
        parser.add_argument('--mqtt-port', type=int, default=1883)
        return parser

    def run(self):
        self.parser = self.build_args()
        self.args = self.parser.parse_args()
        self._init_unicorn()
        signal.signal(signal.SIGTERM, self.on_term)
        self._connect()
        self._run()

if __name__ == "__main__":
    App().run()
