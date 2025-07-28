import network
import time
import socket
from sh1106_oled import oled
from utils import vars
from WIFI_CODES import ssid, password

def connect():
    oled.fill(0)
    oled.text("Cong", 0, 0)

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    time.sleep(0.1)

    print('Connecting to Wi-Fi', end='')
    i = 4 * 8
    try:
        while not sta_if.isconnected():
            oled.text(".", i, 0)
            i += 8
            if i > 80:
                i = 4 * 8
                oled.text("    ", i, 0)
            print('.', end='')
            time.sleep(0.5)
    except:
        oled.fill(0)
        oled.text("Conn fail", 0, 0)
        print("Connection failed!")
        time.sleep(1)
        return
        # machine.reset()
        

    print('\nConnected! IP:', sta_if.ifconfig()[0])
    vars.connected = True
    oled.text("Done!", 0, 10)

    time.sleep(0.5)

    vars.PI_ADDR = sta_if.ifconfig()[0]

connect()
    