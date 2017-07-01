import paho.mqtt.client as mqtt
import time
import json
import unicornhat as unicorn


class App():

    def _init_unicorn(self):
        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(0)
        unicorn.brightness(0.5)
        time.sleep(1)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("unicorn/#")

    def on_message(self, client, userdata, msg):

        _, x, y = msg.topic.split("/")
        colour = json.loads(msg.payload)

        unicorn.set_pixel(int(x), int(y),
                          int(colour['r']), int(colour['g']), int(colour['b']))
        unicorn.show()

    def _connect(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect("localhost", 1883, 60)

    def _run(self):
        self.client.loop_forever()

    def run(self):
        self._init_unicorn()
        self._connect()
        self._run()

if __name__ == "__main__":
    App().run()
