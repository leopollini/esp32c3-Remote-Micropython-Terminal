# import connect
from utils import vars, utils
from sh1106_oled import oled
import time
import connect


try:
    time.sleep(5)
except KeyboardInterrupt:
    ...

oled.fill(1)
oled.fill(0)

# time.sleep(2)

connect.connect()
vars.up = True
utils.printStatus()

import remoteExecutor


serv = remoteExecutor.RemoteExecutorServer()
serv.serverUp()

while True:
    time.sleep(1000)
