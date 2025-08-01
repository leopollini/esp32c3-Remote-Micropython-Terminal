from sh1106_oled import oled
from time import sleep

class vars :
    up = False
    connected = False
    sta_if = None
    oled = oled
    PI_ADDR = None
    PORT = 22
    ESP_NAME = "0.0.0.0"
    CONN_TIMEOUT_SEC = 60
    DEFAULT_AUTOIMPORT_LIST = ["from sh1106_oled import oled", "from utils import vars, utils"]
    AUTOSTART_SERVER = True
    AUTORESTART_SERVER = False

class utils :
    @staticmethod
    def printBegin() :
        oled.fill(0)
        oled.text(f"Connecting...",0,0)
        oled.show()

    @staticmethod
    def printStatus() :
        oled.fill(0)
        # oled.text(f"Up: {vars.up}",0,0)
        # oled.text(f"Cn: {vars.connected}",0,00)
        oled.text(f"{vars.PI_ADDR}",0,0)
        oled.text(f"{vars.PI_ADDR}",-48,10)

    @staticmethod
    def flashText(text, times = 20):
        oled.fill(0)
        for i in range(0,times):
            x = 0
            for char in text:
                oled.text(str(char), x % 72, 10 * (x // 72), auto_show=False)
                x += 8
            oled.show()
            sleep(1)
            oled.fill(1)
            sleep(1)
            oled.fill(0)