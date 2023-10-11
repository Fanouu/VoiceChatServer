from colorama import Style, Fore
class Logger:
    prefix = []

    def __init__(self, prefix=None):
        if prefix is None:
            prefix = ["Server Thread"]
        self.prefix = prefix

    def getPrefix(self):
        prefix = ""
        for p in self.prefix:
            prefix = prefix + f"[{p}]"

        return prefix

    def send(self, COLOR, level, text: str):
        print(COLOR + self.getPrefix() + level + ":" + Style.RESET_ALL, str(text))

    def warning(self, text: str):
        self.send(Fore.RED, "[WARNING]", text)

    def notice(self, text: str):
        self.send(Fore.BLUE, "[NOTICE]", text)

    def info(self, text: str):
        self.send(Fore.GREEN, "[INFO]", text)

    def debug(self, text: str):
        self.send(Fore.YELLOW, "[DEBUG]", text)