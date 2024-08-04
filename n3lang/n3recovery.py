from n3utils import colorize_swap


def n3c_recovery(width, count, ones, pos, tool, change_tool, verbose=0) -> str:
    data = [1] * ones + [0] * (width - ones)
    input_count = count
    input_change_tool = change_tool
    while count + change_tool > 0:
        if verbose > 0:
            print(f"pos={pos}, count={count}, tool={tool}, " + \
                  f"change_tool={change_tool}, data={data}")
        if tool == 0:
            exist_exchange = False
            exist_pos = 0
            for i in range(pos, width - 1):
                if (data[i] == 1) and (data[i + 1] == 0):
                    exist_exchange = True
                    exist_pos = i
                    break
            if not exist_exchange:
                tool = 1
                change_tool -= 1
                pos = 0
                continue
            else:
                pos = exist_pos
            message = f"{colorize_swap(data, pos, pos + 1)} -> "
            data[pos], data[pos + 1] = data[pos + 1], data[pos]
            message += f"{colorize_swap(data, pos, pos + 1)}"
            if verbose > 0:
                print(message)
            count -= 1
            pos += 1
        elif tool == 1:
            exist_exchange = False
            exist_pos = 0
            for i in range(pos, width - 1):
                if (data[i] == 1) and (data[i + 2] == 0):
                    exist_exchange = True
                    exist_pos = i
                    break
            if not exist_exchange:
                tool = 0
                change_tool -= 1
                pos = 0
                continue
            else:
                pos = exist_pos
            message = f"{colorize_swap(data, pos, pos + 2)} -> "
            data[pos], data[pos + 2] = data[pos + 2], data[pos]
            message += f"{colorize_swap(data, pos, pos + 2)}"
            if verbose > 0:
                print(message)
            count -= 1
            pos += 2
    return "".join(map(str, data))

# if pos == width - 1:
#     pos = 0
# elif data[pos] == 1:
#     if pos == width - 1:
#         tool = 0
#         change_tool -= 1
#     elif data[pos + 2] == 1:
#         if data[pos + 1] == 1:
#             pos += 2
#         else:
#             pass
#     else:
#         message = f"{colorize_swap(data, pos, pos + 2)} -> "
#         data[pos], data[pos + 2] = data[pos + 2], data[pos]
#         message += f"{colorize_swap(data, pos, pos + 2)}"
#         if verbose > 0:
#             print(message)
#         count -= 1
#         pos += 2
# else:
#     pos += 1
