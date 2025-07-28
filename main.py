# import connect
from utils import vars, utils
from sh1106_oled import oled
import time
import connect

# AVOID_MICROPYTHONS_CTRLC = True

# if AVOID_MICROPYTHONS_CTRLC:
#     try:
#         time.sleep(5)
#     except KeyboardInterrupt:
#         ...

def main():
    oled.fill(1)
    oled.fill(0)
    oled.fill(1)
    oled.fill(0)


    connect.connect()
    vars.up = True
    oled.fill(0)
    utils.printStatus()

    if not vars.connected:
        oled.text("No serv", 0, 30)
        exit()

    import remoteExecutor


    serv = remoteExecutor.RemoteExecutorServer()
    serv.serverUp(True)

    print("main concluded")

if vars.AUTOSTART_SERVER:
    main()
    while vars.AUTORESTART_SERVER:
        main()

# while True:
#     await asyncio.sleep(100)
