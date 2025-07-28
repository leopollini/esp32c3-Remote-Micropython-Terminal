import asyncio

class Timeout:
    class TimeoutError(BaseException):
        ...

    def __init__(self, delay, before_close):
        self.before_close = before_close
        self.delay = delay
        self._timeout_task = None
        # print("new timer")

    async def __aenter__(self):
        # print("entered")
        self._timeout_task = asyncio.current_task()
        self._killer = asyncio.create_task(self._timeout())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # print("exited")
        self._killer.cancel()
        return False  # propagate exception if any

    async def _timeout(self):
        await asyncio.sleep(self.delay)
        self.before_close()
        self._timeout_task.cancel()
        # print("timed out")
        # raise Timeout.TimeoutError()