import sys

import colorama


def progress(message: str) -> None:
    sys.stdout.write("\r" + message)
    sys.stdout.flush()


def colorize_bool(data: bool) -> str:
    message = colorama.Fore.BLACK
    if data:
        message += colorama.Back.GREEN + f"{data} "
    else:
        message += colorama.Back.RED + f"{data}"
    message += colorama.Style.RESET_ALL
    return message


def colorize(data) -> str:
    message = colorama.Fore.BLACK
    message += colorama.Back.RED + f"{data}"
    message += colorama.Style.RESET_ALL
    return message


def colorize_swap(data: list, from_pos: int, to_pos: int) -> str:
    message = ""
    position = 0
    for d in data:
        if position in [from_pos, to_pos]:
            message += colorize(d)
        else:
            message += str(d)
        position += 1
    return message


def fredkin_gate(_a, _b, _c):
    new_b = (_b & ~_a) | (_c & _a)
    new_c = (_c & ~_a) | (_b & _a)
    return _a, new_b, new_c


def sign_of_subtraction_of_two_one_bits(_a, _b):
    control = _b & 1
    _, _, less = fredkin_gate(control, _a, ~_b & 1)
    return 1 - less
