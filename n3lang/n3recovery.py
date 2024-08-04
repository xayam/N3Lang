import math

from n3utils import colorize_swap, colorize_bool, get_sum_width, list_bool_to_str


def n3c_recovery(width,
                 false_operation,
                 count, ones,
                 pos,
                 change_tool,
                 verbose=0) -> str:
    best = [1] * ones + [0] * (width - ones)
    data = best[:]
    if false_operation:
        return list_bool_to_str(best)
    limit = 2 ** math.ceil(get_sum_width(width - 1))
    input_change_tool = change_tool
    for tool in [0, 1]:
        while (count + change_tool > 0) and (change_tool > - limit):
            if verbose > 0:
                print(f"c={count} o={ones} p={pos} t={tool} " +
                      f"e={change_tool}, current={data}")
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
                    pos = input_change_tool - change_tool + 1
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
                    # try:
                    if (data[i] == 1) and (data[i + 2] == 0):
                        exist_exchange = True
                        exist_pos = i
                        break
                    # except IndexError:
                    #     if verbose > 0:
                    #         print(f"{colorize_bool(False)} IndexError: pos={pos}, i={i}")
                    #     break
                if not exist_exchange:
                    tool = 0
                    change_tool -= 1
                    pos = input_change_tool - change_tool + 1
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
        if (count == 0) and (change_tool == 0):
            return list_bool_to_str(data)
        data = best[:]
    return ""

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
