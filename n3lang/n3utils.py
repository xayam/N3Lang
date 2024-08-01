import sys

import colorama


def progress(message: str) -> None:
    sys.stdout.write("\r" + message)
    sys.stdout.flush()


def colorize_bool(data: bool) -> str:
    _warning = colorama.Fore.WHITE
    if data:
        _warning += colorama.Back.GREEN + f"{data} "
    else:
        _warning += colorama.Back.RED + f"{data}"
    _warning += colorama.Style.RESET_ALL
    return _warning


def fredkin_gate(_a, _b, _c):
    new_b = (_b & ~_a) | (_c & _a)
    new_c = (_c & ~_a) | (_b & _a)
    return _a, new_b, new_c


def sign_of_subtraction_of_two_one_bits(_a, _b):
    control = _b & 1
    _, _, less = fredkin_gate(control, _a, ~_b & 1)
    return 1 - less
