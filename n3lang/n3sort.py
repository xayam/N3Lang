import matplotlib.pyplot as plt

from n3utils import progress


def n3c_sort(data: list) -> [list, int]:
    width = len(data)
    ones = 0
    for i in inp:
        if i == 1:
            ones += 1
    best = [1 for _ in range(ones)] + [0 for _ in range(width - ones)]
    count = 0
    flag = False
    while best != data:
        for t in range(width - 1):
            for _ in range(data[t + 1]):
                data[t], data[t + 1] = data[t + 1], data[t]
                count += 1
            if best == data:
                flag = True
                break
        if flag:
            break
        for t in range(1, width - 1):
            for _ in range(data[t + 1]):
                data[t - 1], data[t + 1] = data[t + 1], data[t - 1]
                count += 1
            if best == data:
                flag = True
                break
        if flag:
            break
        if count > 2 ** width:
            raise Exception("ERROR! count > 2 ** width")
    return data, count, ones, width - ones


if __name__ == "__main__":
    maximum = 32
    plt.figure(figsize=(4, 4))
    plt.axis([0, maximum, 0, maximum])
    for window in range(1, maximum):
        max_count = 0
        max_one = 0
        max_zero = 0
        for d in range(2 ** window):
            s = f"{d:{window}b}".replace(' ', '0')
            inp = [int(char) for char in s]
            picked_out, exchanges, one, zero = n3c_sort(data=inp)
            if exchanges > max_count:
                max_count = exchanges
                max_one = one
                max_zero = zero
            x = window
            y = max_count / window
            message = f"width={x}, max_count={max_count}, " + \
                      f"max_one={max_one}, max_zero={max_zero}, " + \
                      f"max_count/width={str(y)[0:10]}"
            progress(message=message)
            plt.scatter(x, y)
            plt.pause(0.05)
        print("")
