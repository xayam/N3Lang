import math
import matplotlib.pyplot as plt

from n3utils import progress, colorize_swap
from n3validation import n3c_validation


def n3c_sort(input_data: list, verbose=0) -> [list, int]:
    data = input_data[:]
    width = len(data)
    ones = 0
    for i in data:
        if i == 1:
            ones += 1
    best = [1] * ones + [0] * (width - ones)
    result = []
    for tool in [0, 1]:
        count = 0
        change_tool = 0
        pos = width - 1
        while best != data:
            if verbose > 0:
                print(f"pos={pos}, count={count}, tool={tool}, " +
                      f"change_tool={change_tool}, data={data}")
            if tool == 0:
                #  + list(range(width - 1, -1, -1))
                exist_exchange = False
                exist_pos = 0
                for i in range(pos, 0, -1):
                    if (data[i] == 1) and (data[i - 1] == 0):
                        exist_exchange = True
                        exist_pos = i
                        break
                if not exist_exchange:
                    tool = 1
                    change_tool += 1
                    pos = width - 1
                    continue
                else:
                    pos = exist_pos
                message = f"{colorize_swap(data, pos, pos - 1)} -> "
                data[pos], data[pos - 1] = data[pos - 1], data[pos]
                message += f"{colorize_swap(data, pos, pos - 1)}"
                if verbose > 0:
                    print(message)
                count += 1
                pos -= 1
            elif tool == 1:
                #  + list(range(width - 1, 1, -1))
                exist_exchange = False
                exist_pos = 0
                for i in range(pos, 1, -1):
                    if (data[i] == 1) and (data[i - 2] == 0):
                        exist_exchange = True
                        exist_pos = i
                        break
                if not exist_exchange:
                    tool = 0
                    change_tool += 1
                    pos = width - 1
                    continue
                else:
                    pos = exist_pos
                if data[pos - 2] == 0:
                    message = f"{colorize_swap(data, pos, pos - 2)} -> "
                    data[pos], data[pos - 2] = data[pos - 2], data[pos]
                    message += f"{colorize_swap(data, pos, pos - 2)}"
                    if verbose > 0:
                        print(message)
                    count += 1
                pos -= 2
        result.append((data, count, ones, width - ones, pos, tool, change_tool))
        data = input_data[:]
    return result[0], result[1]


def check():
    # TODO
    maximum = 32
    plt.figure(figsize=(4, 4))
    plt.axis([0, maximum, 0, maximum])
    for window in range(1, maximum + 1):
        max_count = 0
        max_one = 0
        max_zero = 0
        max_bits = 0
        for d in range(2 ** window):
            s = f"{d:{window}b}".replace(' ', '0')
            inp = [int(char) for char in s]
            picked_out, exchanges, one, zero = n3c_sort(inp)
            assert picked_out == [1] * one + [0] * zero
            if exchanges > max_count:
                max_count = exchanges
            if one > max_one:
                max_one = one
            if zero > max_zero:
                max_zero = zero
            bits = math.ceil(math.log2(max_count + 1))
            bits += math.ceil(math.log2(window))
            if bits > max_bits:
                max_bits = bits
            x = window
            y = max_count / window
            message = f"{str(100 * (d + 1) / 2 ** window)[0:6].rjust(7, ' ')}% " + \
                      f"width={x}, max_bits={max_bits}, max_count={max_count}, " + \
                      f"max_one={max_one}, max_zero={max_zero}, " + \
                      f"percent={str(100 * max_bits / window)[0:6]}"
            progress(message=message)
            plt.scatter(x, y)
            plt.pause(0.05)
        print("")


if __name__ == "__main__":
    n3c_validation()
