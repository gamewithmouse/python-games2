import datetime



class Logger:
    def __init__(self) -> None:
        pass
    def debug(self, msg):
        print(f"[{self._datetime()}] [DEBUG] {msg}")

    def info(self, msg):
        print(f"[{self._datetime()}] [INFO] {msg}")
    def warn(self, msg):
        print(f"[{self._datetime()}] [WARNING] {msg}")
    def error(self, msg):
        print(f"[{self._datetime()}] [ERROR] {msg}")

    def _datetime(self):
        dt = datetime.datetime.now()
        return dt.strftime("%Y/%m/%d:%H:%M:%S")