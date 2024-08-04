import math
import pprint
import sys

import n3lang.n3recovery
from n3sort import n3c_sort
from n3utils import colorize_bool, get_n3sort_values, get_sum_width, list_to_str, progress


def n3c_validation():
    verbose = 1
    # print(get_annotation())
    # print(f"Decompressing...")
    for width in range(1, 7):
        # [8, 32, 512, 65536]
        results = dict()
        for d in range(2 ** width):
            s = f"{d:{width}b}".replace(" ", "0")
            arr = [int(char) for char in s]
            data = arr[:]
            if verbose > 0:
                print(f"Compressing...\n")
            values = n3c_sort(data, verbose)
            values["width"] = width
            values["verbose"] = 1
            values.__delitem__("data")
            values.__delitem__("zeros")
            recovery = n3lang.n3recovery.n3c_recovery(**values)
            assertion = recovery == s
            print(f"{colorize_bool(assertion)} width={width} " + \
                  f"'{s}' -> '{recovery}'")
            assert assertion


def main(degrees=None, verbose=0) -> str:
    if degrees is None:
        windows = [2 ** i - 1 for i in [1, 2, 3, 5, 9, 16]]
    else:
        windows = [2 ** i for i in degrees]
    result = ""
    index = 0
    for width in windows:
        index += 1
        summa = get_sum_width(width)
        summa = math.ceil(summa)
        max_count = 2 ** summa
        max_ones = width
        max_bits_key = summa + math.ceil(math.log2(max_ones + 1)) + 1
        percent = max_bits_key / width
        result += \
            f"index={str(index).rjust(1, ' ')}, " + \
            f"width={str(width).rjust(5, ' ')}, " + \
            f"summa={str(summa)[:3].rjust(2, ' ')}, " + \
            f"max_count={str(max_count).rjust(14, ' ')}, " + \
            f"max_ones={str(max_ones).rjust(5, ' ')}, " + \
            f"max_bits_key={str(max_bits_key).rjust(2, ' ')}, " + \
            f"percent={str(100 * percent)[:6].rjust(6, ' ')}%\n"
    if verbose > 0:
        print(result)
    return result


if __name__ == "__main__":
    # ? P(W)
    # P(W) = lim sum log2[x + 1], x = 1 to log2[y] as y->W
    # L = math.ceil(P(W)) + 1

    # main(degrees=[3, 9, 23, 55], verbose=1)

    # main(verbose=1)

    n3c_validation()
