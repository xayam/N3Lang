from n3compress import compress, decompress
from n3utils import colorize_bool, progress


def main(_data: str) -> [list, list]:
    w = len(_data)
    print(f"Current width = {w}")
    arr = [int(char) for char in _data]
    result, percent, bits, max_count, max_one = \
        compress(
            arr,
            printable=False,
            verbose=1
        )
    print(
        f"result={result}, percent={percent}, " +
        f"bits={bits}, max_count={max_count}, max_one={max_one}"
    )
    r = []
    # now not work
    # r = decompress(
    #         _width=w,
    #         _count=max_count,
    #         _one=max_one
    # )
    return arr, r


if __name__ == "__main__":
    data = "011000100111"
    i, o = main(data)
    print(f"Input data for compress: {i}")
    print(f"Output decompress data: {o}")
