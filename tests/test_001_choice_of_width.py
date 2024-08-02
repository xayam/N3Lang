import winsound
from n3compress import n3c_sort
from n3utils import progress, colorize_bool

import functools
import matplotlib.pyplot as plt


def difficult():
    try:
        width = int(input("Input WIDTH, default 0 for infinity process: "))
    except ValueError:
        width = 0
        print(f"[INFO]| WIDTH set to {width} ")
    assert width >= 0
    if width == 0:
        current = 1
    else:
        current = width
    plt.axis([0, 32, 0, 10])
    while True:
        bits_ = []
        max_bits_ = 0
        max_count_ = 0
        max_percent_ = 0
        results_ = True
        c = 0
        for limit in range(0, 2 ** current):
            c += 1
            arr = [int(char) for char in f"{limit:{current}b}".replace(" ", "0")]
            result, _, bits, max_count, _ = n3c_sort(arr, False)
            results_ = results_ and result
            _warning = colorize_bool(results_)
            bits_.append(bits)
            if bits > max_bits_:
                max_bits_ = bits
            if max_count > max_count_:
                max_count_ = max_count
            percent_ = 100 * max_bits_ / current
            if percent_ > max_percent_:
                max_percent_ = percent_
            format_percent = str(max_percent_)[0:6]
            if max_percent_ < 100:
                format_percent = " " + format_percent
            if max_percent_ == 0.:
                format_percent = " " + format_percent
            format_percent = format_percent.ljust(7, '0')
            message = f"{_warning} | "
            message += f"{str(100 * (limit + 1) / (2 ** current))[0:6].rjust(7, ' ')}% | "
            message += f"width = {str(current).rjust(2, ' ')} | "
            message += f"max_bits_ = {str(max_bits_).rjust(2, ' ')} | "
            message += f"max_count_ = {str(max_count_).rjust(3, ' ')} | "
            message += f"compressing = {format_percent}% | "
            progress(message)
        print("")
        # result = functools.reduce(lambda a, b: a and b, results_)
        plt.scatter(current, max_count_/current)
        plt.pause(0.05)
        if width > 0:
            break
        current += 1


def main():
    difficult()


if __name__ == "__main__":
    main()
    winsound.Beep(2500, 5000)
