import asyncio
from Timeout import Timeout
from utils import vars
from sh1106_oled import oled

# CHANGE_IO = False

async def handleClient(reader, writer):
    await Clienter(reader, writer).start_terminal()

class RemoteExecutorServer:
    sleeper_task = None
    up = False
    
    def __init__(self) -> None:
        self.server = None

    async def beginLoop(self, do_block) -> None:
        self.server = await asyncio.start_server(handleClient, vars.ESP_NAME, vars.PORT)
        print(f"initialized server at vars.PORT {vars.PORT}")

        # async with self.server:
        #     await self.server.serve_forever()

    def serverUp(self, do_block = False):
        asyncio.run(self.beginLoop(do_block))
        RemoteExecutorServer.up = True
        if do_block:
            RemoteExecutorServer.sleepForever()

    @staticmethod
    async def sleeper():
        RemoteExecutorServer.sleeper_task = asyncio.current_task()
        while True:
            await asyncio.sleep(1000)

    @staticmethod
    def sleepForever():
        oled.text("Srv activ", 0, 20)
        oled.text(f"Port {vars.PORT}", 0, 30)
        try:
            asyncio.run(RemoteExecutorServer.sleeper())
        except BaseException as e:
            oled.fill(1)
            oled.fill(0)
            oled.text("Serv down", 0, 0)
            # raise(e)

    @staticmethod
    def closeServers():
        RemoteExecutorServer.up = False
        if RemoteExecutorServer.sleeper_task:
            RemoteExecutorServer.sleeper_task.cancel()

# one of theese for each connection
class Clienter:
    count = 0
    ids = 0

    def __init__(self, reader, writer) -> None:
        self.reader = reader
        self.writer = writer
        self.id = Clienter.ids
        self.timer = None
        self.context = {'print': self.custom_print, "close_server": RemoteExecutorServer.closeServers}
        Clienter.count += 1
        Clienter.ids += 1
        print(f"connection {self.id} created")
    
    def __del__(self):
        self.writer.close()
        Clienter.count -= 1
        print(f"connection {self.id} concluded")
        self.writer.close()
        self.reader.close()


    def custom_print(self, *args, sep=' ', end='\n'):
        try:
            output = sep.join(str(arg) for arg in args) + end
            self.writer.write(output.encode() if isinstance(output, str) else output)

        except Exception as e:
            self.writer.write('[print error: {}]'.format(e))
    
    async def start_terminal(self):
        self.sendWelcome()
        command = ""
        context_depth = 0
        self.importStuff()
        while True:
            msg = await self.recv()
            if msg == None:     # client has disconnected. Conclude coroutine
                break
            msg = msg.strip()
            print(f"Executing {msg}, conetxt depth = {context_depth}")
            command += ("\n" + ("\t" * context_depth) + msg if context_depth != 0 else msg)
            if context_depth > 0:
                if msg != "":
                    if msg[-1] == ":":
                        context_depth += 1
                    self.send("..." * context_depth + " ")
                    continue
                context_depth -= 1
            if context_depth != 0:
                self.send("..." * context_depth + " ")
                continue
            try:
                # print(f"trying '{command}'")
                compile(command, "<stdin>", "exec")
            except SyntaxError as e:
                # print(e.__class__, e)
                if command.strip()[-1] != ":":
                    self.custom_print(e.__class__, e)
                    command = ""
                    self.send(">>> ")
                    print("Done")
                    continue
                self.send("... ")
                context_depth = 1
                continue
            except BaseException as e:
                self.custom_print(e.__class__, e)
                command = ""

            try:
                exec(command, self.context)
            except BaseException as e:
                self.custom_print(e.__class__, e)
            finally:
                command = ""
            self.send(">>> ")
            print("Done")
            
    def importStuff(self):
        for cmd in vars.DEFAULT_AUTOIMPORT_LIST:
            try:
                exec(cmd, self.context)
            except:
                ...
            

    def sendWelcome(self):
        print(f"New client. Id: {self.id}")
        self.send("Welcome to " + vars.ESP_NAME + "'s micropython ambient.\n")
        self.send(">>> ")

    def send(self, msg):
        try:
            if isinstance(msg, str):
                msg = msg.encode()
            self.writer.write(msg)
        except BaseException as e:
            print("Send Failed: {e}")

    # this is executed after the timeout of the connection, and after this the coroutine is closed and the client is lost.
    def send_final_msg(self):
        self.send(f"\n#####\nConnection timed out. You have been kicked from {vars.ESP_NAME}.\n#####\n")
        print(f"Closing connection {self.id} because of timeout")
        self.__del__()  # called here because is not called before coroutine end.

    async def recv(self):
        async with Timeout(vars.CONN_TIMEOUT_SEC, self.send_final_msg):
            rec = (await self.reader.readline()).decode()
            if rec == None or rec == "":
                return None
            # self.send("OK")
            return rec
        return None
        