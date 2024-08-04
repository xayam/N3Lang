from n3utils import colorize_swap


def n3c_recovery(width, count, ones, pos, tool, change_tool, verbose=0) -> str:
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
    return "".join(map(str, data))
