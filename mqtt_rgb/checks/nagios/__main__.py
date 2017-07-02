import subprocess
import json
import subprocess

from .. import Check

NAG_RESULT_OK = 0
NAG_RESULT_WARNING = 1
NAG_RESULT_CRITICAL = 2
NAG_RESULT_UNKNOWN = 3


class NagiosCheck(Check):

    description = "Run an Nagios script"

    RESULT_MAP = {
        NAG_RESULT_OK: (0, 255, 0),
        NAG_RESULT_WARNING: (0, 128, 0),
        NAG_RESULT_CRITICAL: (255, 0, 0),
        NAG_RESULT_UNKNOWN: (0, 0, 255)
    }

    def build_args(self):
        parser = super().build_args()
        parser.add_argument('--script', type=str)
        parser.add_argument('nagios_args', nargs=argparse.REMAINDER)
        return parser

    def _run(self):
        result = subprocess.call([self.check_command] + self.args.nagios_args)
        self.set_pixel(self.args.x, self.args.y, *NagiosCheck._map_result(result))

    @staticmethod
    def _map_result(cls, result):
        try:
            return cls.RESULT_MAP[result]
        except KeyError:
            return (255, 0, 0)


if __name__ == "__main__":
    NagiosCheck().run()
