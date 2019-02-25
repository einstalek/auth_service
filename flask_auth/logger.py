import time


class Logger:
    @staticmethod
    def log(text):
        print(time.strftime("%Y-%m-%d %H:%M:%S"), text)

