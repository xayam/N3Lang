import math

from n3compress import compress, decompress
from n3utils import colorize_bool, progress


def main(_data: str, verbose=1) -> [list, list]:
    w = len(_data)
    if verbose > 0:
        print(f"Current width = {w}")
    arr = [int(char) for char in _data]
    result, percent, bits, max_count, max_one = \
        compress(
            arr,
            printable=False,
            verbose=verbose
        )
    if verbose > 0:
        print(
            f"result={result}, percent={percent}, " +
            f"bits={bits}, max_count={max_count}, max_one={max_one}"
        )
    r = decompress(
            _width=w,
            _count=max_count,
            _one=max_one,
            printable=False,
            verbose=verbose
    )
    return arr, r


if __name__ == "__main__":
    # for data in ["0110", "1001"]: # ["101011"]:# ["011000100111", "111111000000"]:
    for width in range(1, 5):
        for data in range(2 ** width):
            arr = f"{data:{width}b}".replace(" ", "0")
            i, o = main(arr, verbose=0)
            res = o == i
            if not res:
                i, o = main(arr, verbose=1)
                print("Result: " + colorize_bool(i == o))
                print(f"Input data for compress: {i}")
                print(f"Output decompress data: {o}")
                print("")
