import colorama
import winsound
import concurrent.futures as pool
from n3compress import compress
from n3utils import progress


# import functools
# import matplotlib.pyplot as plt


def main():
    try:
        width = int(input("Input maximum for WIDTH, default 0 for infinity process: "))
    except ValueError:
        width = 0
        print(f"[INFO]| WIDTH set to {width} ")
    assert width >= 0
    if width == 0:
        current = 1
    else:
        current = width
    # plt.axis([0, 32, 0, 150])
    while True:
        bits_ = []
        max_bits_ = 0
        max_count_ = 0
        max_percent_ = 0
        results_ = True
        max_workers = 1
        for limit in range(0, 2 ** current, max_workers):
            tasks = []
            for i in range(max_workers):
                if limit + i + 1 > 2 ** current:
                    continue
                arr = \
                    [int(char) for char in f"{(limit + i):{current}b}".replace(" ", "0")]
                tasks.append((limit + i, arr))
            answer = dict()
            responses = dict()
            with pool.ThreadPoolExecutor(max_workers=max_workers) as executor:
                for task in tasks:
                    params = {
                        "data": task[1],
                        "printable": False
                    }
                    answer[task[0]] = executor.submit(compress, **params)
                executor.shutdown()
                for num in answer:
                    responses[num] = answer[num].result()
            c = 0
            for num in responses:
                c += 1
                result, _, bits, max_count, _ = responses[num]
                results_ = results_ and result
                _warning = colorama.Fore.WHITE
                if results_:
                    _warning += colorama.Back.GREEN + f"{results_} "
                else:
                    _warning += colorama.Back.RED + f"{results_}"
                _warning += colorama.Style.RESET_ALL
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
                message += f"{str(100 * (limit + c) / (2 ** current))[0:6].rjust(7, ' ')}% | "
                message += f"width = {str(current).rjust(2, ' ')} | "
                message += f"max_bits_ = {str(max_bits_).rjust(2, ' ')} | "
                message += f"max_count_ = {str(max_count_).rjust(3, ' ')} | "
                message += f"compressing = {format_percent}% | "
                progress(message)
        print("")
        # result = functools.reduce(lambda a, b: a and b, results_)
        # plt.scatter(current, max(percents_))
        # plt.pause(0.05)
        if width > 0:
            break
        current += 1


if __name__ == "__main__":
    main()
    winsound.Beep(2500, 5000)
