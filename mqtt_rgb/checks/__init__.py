import paho.mqtt.client as mqtt
import argparse


class Check():

    description = NotImplemented

    def build_args(self):
        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument('-x', type=int)
        parser.add_argument('-y', type=int)
        parser.add_argument('--prefix', type=str, default="unicorn")
        parser.add_argument('--mqtt-host', default="localhost")
        parser.add_argument('--mqtt-port', type=int, default=1883)
        return parser

    def _run(self):
        raise NotImplemented

    def run(self):
        self.parser = self.build_args()
        self.args = self.parser.parse_args()
        self._run()

    def set_pixel(self, x, y, r, g, b):

        payload = json.dumps({
            'r': r,
            'g': g,
            'b': b
        })

        client = mqtt.Client()
        client.single(
            "/".join(self.args.prefix, str(x), str(y)),
            payload=payload,
            retain=True,
            hostname=self.args.mqtt_host,
            port=self.args.mqtt_port
        )
