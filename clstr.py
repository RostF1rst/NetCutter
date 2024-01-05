def red(txt: str | int | float) -> str:
    return f'\033[31m{txt}\033[00m'


def green(txt: str | int | float) -> str:
    return f'\033[32m{txt}\033[00m'


def yellow(txt: str | int | float) -> str:
    return f'\033[33m{txt}\033[00m'


def blue(txt: str | int | float) -> str:
    return f'\033[34m{txt}\033[00m'


def magenta(txt: str | int | float) -> str:
    return f'\033[35m{txt}\033[00m'


def cyan(txt: str | int | float) -> str:
    return f'\033[36m{txt}\033[00m'


def light_gray(txt: str | int | float) -> str:
    return f'\033[37m{txt}\033[00m'


def dark_gray(txt: str | int | float) -> str:
    return f'\033[90m{txt}\033[00m'


def light_red(txt: str | int | float) -> str:
    return f'\033[91m{txt}\033[00m'


def light_green(txt: str | int | float) -> str:
    return f'\033[92m{txt}\033[00m'


def light_yellow(txt: str | int | float) -> str:
    return f'\033[93m{txt}\033[00m'


def light_blue(txt: str | int | float) -> str:
    return f'\033[94m{txt}\033[00m'


def light_magenta(txt: str | int | float) -> str:
    return f'\033[95m{txt}\033[00m'


def light_cyan(txt: str | int | float) -> str:
    return f'\033[96m{txt}\033[00m'


def white(txt: str | int | float) -> str:
    return f'\033[97m{txt}\033[00m'
