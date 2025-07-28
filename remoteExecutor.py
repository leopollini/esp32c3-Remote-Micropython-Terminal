import socket
import asyncio
import sys
from Timeout import Timeout

PORT = 22
ESP_NAME = "0.0.0.0"
CONN_TIMEOUT_SEC = 60
# CHANGE_IO = False

class RemoteExecutorServer:
    def __init__(self) -> None:
        self.server = None

    async def beginLoop(self, do_block) -> None:
        self.server = await asyncio.start_server(handleClient, ESP_NAME, PORT)
        print(f"initialized server at port {PORT}")

        if do_block:
            while True:
                await asyncio.sleep(1000)
        # async with self.server:
        #     await self.server.serve_forever()

    def serverUp(self, do_block = False):
        asyncio.run(self.beginLoop(do_block))


        

# one of theese for each connection
class Clienter:
    count = 0
    ids = 0

    def __init__(self, reader, writer) -> None:
        self.reader = reader
        self.writer = writer
        self.id = Clienter.ids
        self.timer = None
        self.context = {'print': self.custom_print}
        Clienter.count += 1
        Clienter.ids += 1
        print(f"connection {self.id} created")
    
    def __del__(self):
        self.writer.close()
        Clienter.count -= 1
        print(f"connection {self.id} concluded")


    def custom_print(self, *args, sep=' ', end='\n'):
        try:
            output = sep.join(str(arg) for arg in args) + end
            self.writer.write(output.encode() if isinstance(output, str) else output)

        except Exception as e:
            self.writer.write('[print error: {}]'.format(e))
    
    #this script grants only two levels of context
    async def start_terminal(self):
        self.sendWelcome()
        multiline_cmd = []
        inner_context = False
        while True:
            msg = await self.recv()
            if msg == None:     # client has disconnected. Conclude coroutine
                break
            msg = msg.strip()
            print(f"Executing {msg}")
            multiline_cmd.append(msg)
            if inner_context and msg != "":
                self.send("... ")
                continue
            inner_context = False
            command = "\n\t".join(multiline_cmd)
            try:
                # print(f"trying '{command}'")
                compile(command, "<stdin>", "exec")
            except SyntaxError as e:
                # print(e.__class__, e)
                if ":" not in command:
                    raise e
                self.send("... ")
                inner_context = True
                continue
            except BaseException as e:
                print(e.__class__, e)
                multiline_cmd = []

            try:
                exec(command, self.context)
            except BaseException as e:
                print(e.__class__, e)
            finally:
                multiline_cmd = []
            self.send(">>> ")
            print("Done")
            


    def sendWelcome(self):
        print(f"New client. Id: {self.id}")
        self.send("Welcome to " + ESP_NAME + "'s micropython ambient.\n")
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
        self.send(f"\n#####\nConnection timed out. You have been kicked from {ESP_NAME}.\n#####\n")
        self.__del__()  # called here because is not called before coroutine end.

    async def recv(self):
        async with Timeout(CONN_TIMEOUT_SEC, self.send_final_msg):
            rec = (await self.reader.readline()).decode()
            if rec == None or rec == "":
                return None
            # self.send("OK")
            return rec
        return None
        
        

async def handleClient(reader, writer):
    await Clienter(reader, writer).start_terminal()





    # def timeoutDetect(self):

    #     async def timer(sec):
    #         timer_finished = False
    #         try:
    #             print("timer started")
    #             await asyncio.sleep(sec)
    #             timer_finished = True
    #             print("timer ended")
    #         except asyncio.CancelledError:
    #             print("timer reset")
    #         if timer_finished:
    #             raise TimeoutError("Connection timed out!")
            
    #     if self.timer != None:
    #         self.timer.cancel()
    #     self.timer = asyncio.create_task(timer(CONN_TIMEOUT_SEC))