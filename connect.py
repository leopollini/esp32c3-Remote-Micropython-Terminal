import network
import time
import ujson as json
from utils import vars
import os
import sys

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

def try_connection(ssid, password) -> bool:
    vars.oled.text("Cong", 0, 10)
    sta_if.connect(ssid, password)
    time.sleep(0.1)

    print('Connecting to Wi-Fi', end='')
    try:
        i = 4 * 8
        for j in range(0, 30):       # 15 s timeout
            vars.oled.text(".", i, 10)
            i += 3
            print('.', end='')
            time.sleep(0.5)
            if sta_if.isconnected():
                vars.connected = True
                break
        return vars.connected
    except KeyboardInterrupt as e:
        vars.oled.fill(0)
        vars.oled.text("Exiting...", 0, 15)
        sys.exit()
    except Exception as e:
        print(e.__class__, e)
        vars.oled.fill(0)
        vars.oled.text("Conn fail", 0, 0)
        print("Connection failed!")
        # time.sleep(1)
        sys.exit()
        
def connect():
    vars.oled.fill(0)
    vars.connected = False
    vars.oled.text("scanning", 0,0)
    try:
        f = open("WIFI_CODES.json", "r")
        wifi_connections = json.load(f)
    except:
        print("bad wifi config file")
        vars.oled.text("Bad conf", 0, 10)
        sys.exit()
    available_connections = sta_if.scan()

    if available_connections.count == 0:
        print("No available connections.", sta_if.ifconfig()[0])
        vars.oled.text("No conn.", 0, 10)
        time.sleep(2)
        
    for net in available_connections:
        vars.oled.fill(0)
        ssid = net[0].decode('utf-8')
        print(f"trying wifi {ssid}")
        passwords = wifi_connections.get(ssid, None)
        if not passwords:
            print("\tNot registered")
            continue
        for pw in passwords:
            vars.oled.fill(0)
            vars.oled.text("found", 0, 0)
            if try_connection(ssid, pw):
                break
        if vars.connected:
            print("Connected to wifi!")
            break
        print("Wrong password. Next connection", sta_if.ifconfig()[0])
        vars.oled.text("bad pw.", 0, 10)
        time.sleep(0.5)
    


    vars.oled.text("Done!", 0, 20)

    if not vars.connected:
        print("Could not connect to wifi. (wifi not registered or bad password)")

    time.sleep(0.5)

    vars.PI_ADDR = sta_if.ifconfig()[0]
    