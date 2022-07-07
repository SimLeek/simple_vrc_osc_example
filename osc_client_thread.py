# https://github.com/ChilloutCharles/bci-workshop

import threading
import time

from collections import defaultdict
from pythonosc.udp_client import SimpleUDPClient


class osc_client_thread(threading.Thread):
    def __init__(self, send_rate, ip, port):
        threading.Thread.__init__(self)

        # osc client
        self.osc_client = SimpleUDPClient(ip, port)

        # rolling average dictionaries
        self.target_value_dict = defaultdict(float)

        # threading stuff
        self.send_rate = send_rate
        self.exit_flag = False

    def set_message(self, osc_path, value):
        self.target_value_dict[osc_path] = value

    def run(self):
        print("Running OSC Client")

        while not self.exit_flag:
            # calculate rolling averages
            for osc_path in self.target_value_dict:
                target_value = self.target_value_dict[osc_path]
                self.osc_client.send_message(osc_path, target_value)

            time.sleep(self.send_rate)

        print("Stopping OSC Client")

    def stop(self):
        self.exit_flag = True

    def __del__(self):
        self.stop()
