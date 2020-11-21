import colorama
import logging

reset = colorama.Fore.RESET + colorama.Fore.WHITE + colorama.Style.BRIGHT
clrs = colorama.Fore
style = colorama.Style

logging.addLevelName(25, "SUCCESS")
logging.addLevelName(23, "OK")
logging.addLevelName(15,"DONE")

class logFilter(logging.Filter):
    def filter(self, record) -> int:
        record.levelnameCap = record.levelname.upper()
        return True


class formatter(logging.Formatter):
    levelColors = {
        "DEBUG": clrs.LIGHTBLACK_EX,
        "DONE":clrs.LIGHTBLACK_EX,
        "INFO": clrs.LIGHTGREEN_EX,
        "OK": clrs.GREEN,
        "SUCCESS": clrs.GREEN,
        "WARNING": clrs.YELLOW,
        "ERROR": clrs.RED,
        "CRITICAL": clrs.LIGHTRED_EX
        }

    def __init__(self, format):
        logging.Formatter.__init__(self, format)

    @staticmethod
    def formatString(string, color=clrs.WHITE, style_=style.NORMAL):
        return reset + style_ + color + string + reset



    def format(self, record: logging.LogRecord) -> str:
        lvl = record.levelname
        color = formatter.levelColors[lvl.upper()]

        record.levelnameCap = formatter.formatString(lvl.upper(), color, style.BRIGHT)
        record.levelname = formatter.formatString(
            (lambda: lvl.lower() if lvl not in ("OK", "SUCCESS") else lvl.upper())(),
            color)

        if record.funcName in ("__init__",):
            record.funcName = record.funcName.replace("_", '')

        record.name = f"[{record.name}]"
        record.threadName=formatter.formatString(record.threadName.lower().replace("thread","").capitalize(),
                                                 color=clrs.WHITE,
                                                 style_=style.BRIGHT)

        record.processName = formatter.formatString(record.processName.lower().replace("process", "").capitalize(),
                                                    color=clrs.LIGHTWHITE_EX)

        s = reset + logging.Formatter.format(self, record)
        return s


class logger(logging.Logger):
    FORMAT = "[%(processName)s:%(threadName)s:%(levelnameCap)s] %(name)s %(funcName)s - %(levelname)s: %(message)s\n"

    def __init__(self, name, *args):
        logging.Logger.__init__(self, name, logging.INFO)
        console = logging.StreamHandler()

        fmt = formatter(logger.FORMAT)
        # console.addFilter(logFilter())
        console.setLevel(0)
        console.setFormatter(fmt)

        self.addHandler(console)

    def done(self, msg='', *args, **kwargs):
        self._log(15, msg, args, **kwargs)

    def ok(self, msg='', *args, **kwargs):
        self._log(23, msg, args, **kwargs)

    def success(self, msg='', *args, **kwargs):
        self._log(25, msg, args, **kwargs)

    def getChild(self, suffix: str):
        n = ']['.join((self.name, suffix))
        return logger(n)
