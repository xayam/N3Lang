from n3utils import colorize_swap


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


if __name__ == "__main__":
    pass
