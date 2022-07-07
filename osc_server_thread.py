# https://github.com/ChilloutCharles/bci-workshop
import threading

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


def info_handler(*args):
    print("Received OSC data. Printing args:")
    for arg in args:
        print("\t " + str(arg))


class osc_server_thread(threading.Thread):
    def __init__(self, ip, recv_port):
        threading.Thread.__init__(self)

        dispatcher = Dispatcher()
        dispatcher.set_default_handler(info_handler)
        self.osc_server = BlockingOSCUDPServer((ip, recv_port), dispatcher)

    def run(self):
        print("Running OSC Server")
        self.osc_server.serve_forever()
        print("Stopping OSC Server")

    def stop(self):
        self.osc_server.shutdown()

    def __del__(self):
        self.stop()


if __name__ == "__main__":
    server = osc_server_thread("127.0.0.1", 9001)
    server.start()
    server.osc_server.shutdown()
