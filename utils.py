from sh1106_oled import oled

class vars :
    up = False
    connected = False
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