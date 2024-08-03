import math
import sys

import matplotlib.pyplot as plt

from n3utils import progress, colorize_swap, colorize_bool, colorize


def n3c_sort(data: list, verbose=0) -> [list, int]:
    width = len(data)
    ones = 0
    for i in data:
        if i == 1:
            ones += 1
    best = [1] * ones + [0] * (width - ones)
    count = 0
    tool = 1
    change_tool = 0
    pos = width - 1
    while best != data:
        if verbose > 0:
            print(f"pos={pos}, count={count}, tool={tool}, " + \
                  f"change_tool={change_tool}, data={data}")
        if tool == 0:
            exist_exchange = False
            exist_pos = 0
            for i in list(range(pos, 0, -1)) + list(range(width - 1, -1, -1)):
                if (data[i] == 1) and (data[i - 1] == 0):
                    exist_exchange = True
                    exist_pos = i
                    break
            if not exist_exchange:
                tool = 1
                change_tool += 1
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
            exist_exchange = False
            exist_pos = 0
            for i in list(range(pos, 1, -1)) + list(range(width - 1, 1, -1)):
                if (data[i] == 1) and (data[i - 2] == 0):
                    exist_exchange = True
                    exist_pos = i
                    break
            if not exist_exchange:
                tool = 0
                change_tool += 1
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
    return data, count, ones, width - ones, pos, tool, change_tool

def n3c_recovery(width, count, ones, pos, tool, change_tool, verbose=0):
    data = [1] * ones + [0] * (width - ones)
    while count > 0:
        if verbose > 0:
            print(f"pos={pos}, count={count}, tool={tool}, " + \
                  f"change_tool={change_tool}, data={data}")
        if tool == 0:

            message = f"{colorize_swap(data, pos, pos + 1)} -> "
            data[pos], data[pos + 1] = data[pos + 1], data[pos]
            message += f"{colorize_swap(data, pos, pos + 1)}"
            if verbose > 0:
                print(message)
            count -= 1
            pos += 1
        elif tool == 1:
            if pos == width - 1:
                pos = 0
            elif data[pos] == 1:
                if pos == width - 1:
                    tool = 0
                    change_tool -= 1
                elif data[pos + 2] == 1:
                    if data[pos + 1] == 1:
                        pos += 2
                    else:
                        pass
                else:
                    message = f"{colorize_swap(data, pos, pos + 2)} -> "
                    data[pos], data[pos + 2] = data[pos + 2], data[pos]
                    message += f"{colorize_swap(data, pos, pos + 2)}"
                    if verbose > 0:
                        print(message)
                    count -= 1
                    pos += 2
            else:
                pos += 1
    return data


def validation():
    for width in [x for x in range(3, 10)]:
        no_conflict = True
        max_count = 0
        max_change_tool = 0
        max_bits = 1
        origin_pars = []
        pars = dict()
        s = ""
        print(s)
        for d in range(2 ** width):
            s = f"{d:{width}b}".replace(" ", "0")
            arr = [int(char) for char in s]
            data = arr[:]
            print("Compressing...")
            data, count, ones, zero, pos, tool, change_tool = n3c_sort(data, 1)
            pars[s] = f"count={count} ones={ones} pos={pos} tool={tool} exchange={change_tool}"
            origin_pars = pars.copy()
            pars = {k: v for k, v in sorted(pars.items(), key=lambda item: item[1])}

            if count > max_count:
                max_count = count
            if change_tool > max_change_tool:
                max_change_tool = change_tool
            bits = 1
            bits += math.ceil(math.log2(max_count + 1))
            bits += math.ceil(math.log2(max_change_tool + 1))
            bits += 2 * math.ceil(math.log2(width))
            if bits > max_bits:
                max_bits = bits
            assertion = data == [1] * ones + [0] * zero
            assert assertion
            # print("Decompressing...")
            # recovery = n3c_recovery(width, count, ones, pos, tool, change_tool, 1)
            recovery = arr
            assertion = recovery == arr
            len_pars = len(origin_pars)
            len_set_pars = len(set(origin_pars.values()))
            no_conflict = len_pars == len_set_pars
            can_compress = max_bits <= width
            print(
                f"{colorize_bool(no_conflict)} " + \
                f"{colorize_bool(can_compress)} " + \
                f"width={width}, arr={arr}, all={len_pars}, unique={len_set_pars}" + \
                f"{str(100 * (d + 1) / 2 ** width)[0:6].rjust(7, ' ')}%, " + \
                # f"arr={arr}, recovery={recovery}, " + \
                f"max_bits={max_bits}, max_count={max_count}, " + \
                f"max_change_tool={max_change_tool}")
            if not assertion:
                print(f"{arr} -> {data} -> {recovery}")
                print(f"{colorize(' ERROR ')} input != output")
                sys.exit(1)
            if not no_conflict:
                print(f"{colorize(' ERROR ')} Collision found")
                break
        if not no_conflict:
            print(origin_pars)
            print(pars)
            for i in pars:
                if pars[i] == pars[s]:
                    print(f"'{s}' <-> '{i}' = '{pars[s]}'")
                    break
            sys.exit(1)

if __name__ == "__main__":
    validation()
    sys.exit()
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
            picked_out, exchanges, one, zero = n3c_sort(data=inp)
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
            message = f"{str(100 * (d + 1)/2 ** window)[0:6].rjust(7, ' ')}% " + \
                      f"width={x}, max_bits={max_bits}, max_count={max_count}, " + \
                      f"max_one={max_one}, max_zero={max_zero}, " + \
                      f"percent={str(100 * max_bits / window)[0:6]}"
            progress(message=message)
            # plt.scatter(x, y)
            # plt.pause(0.05)
        print("")
