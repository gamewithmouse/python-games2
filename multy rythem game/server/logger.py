import datetime

class Logger:

    def __init__(self) -> None:
        pass
    def debug(self, message):
        print(f"[{datetime.datetime.today()}] [DEBUG] {message}")
    def info(self, message):
        print(f"[{datetime.datetime.today()}] [INFO] {message}")
    def warn(self, message):
        print(f"[{datetime.datetime.today()}] [WARNING] {message}")
    def error(self, message):
        print(f"[{datetime.datetime.today()}] [ERROR] {message}")
    def critical(self, message):
        print(f"[{datetime.datetime.today()}] [CRITICAL] {message}")        