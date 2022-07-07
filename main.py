import time
import math

# https://github.com/ChilloutCharles/bci-workshop
from osc_client_thread import osc_client_thread
from osc_server_thread import osc_server_thread


class OSC_Path:
    MOUTH = "/avatar/parameters/VRCEmote"  # 0-16
    # MOUTH = '/avatar/parameters/Hat'  # hat on/off bool for a certain avatar
    # MOUTH = '/avatar/parameters/emit'  # emission percentage for a certain avatar


avatar_weights = {
    OSC_Path.MOUTH: 0,
}

if __name__ == "__main__":
    # OSC threads
    ip = "127.0.0.1"
    send_port = 9000
    recv_port = 9001
    # fwd_port = 9002
    send_rate = 0.001
    osc_client = osc_client_thread(send_rate, ip, send_port)
    osc_server = osc_server_thread(ip, recv_port)

    try:
        osc_server.start()
        osc_client.start()

        while True:
            openness = math.sin(time.time() % math.pi) * 16.0
            print(openness, end="\r")
            osc_client.set_message(OSC_Path.MOUTH, int(round(openness)))
    except KeyboardInterrupt:
        print("\nClosing!")
    finally:
        osc_client.stop()
        osc_server.stop()

        osc_client.join()
        osc_server.join()
