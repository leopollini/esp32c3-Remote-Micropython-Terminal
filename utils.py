from sh1106_oled import oled

class vars :
    up = False
    connected = False
    PI_ADDR = None

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
        oled.text(f"{vars.PI_ADDR}",-50,0)