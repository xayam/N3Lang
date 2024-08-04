import math

from n3utils import colorize_swap, get_sum_width, list_bool_to_str


def n3c_recovery(width,
                 false_operation,
                 count,
                 ones,
                 position,
                 tool_change,
                 verbose=0) -> str:
    best = [1] * ones + [0] * (width - ones)
    data = best[:]
    if false_operation:
        return list_bool_to_str(best)
    limit = 2 ** math.ceil(get_sum_width(width - 1))
    input_change_tool = tool_change
    for tool in [0, 1]:
        while (count + tool_change > 0) and (tool_change > - limit):
            if verbose > 0:
                print(f"c={count} o={ones} p={position} t={tool} " +
                      f"e={tool_change}, current={data}")
            if tool == 0:
                exist_exchange = False
                exist_pos = 0
                for i in range(position, width - 1):
                    if (data[i] == 1) and (data[i + 1] == 0):
                        exist_exchange = True
                        exist_pos = i
                        break
                if not exist_exchange:
                    tool = 1
                    tool_change -= 1
                    position = input_change_tool - tool_change + 1
                    continue
                else:
                    position = exist_pos
                message = f"{colorize_swap(data, position, position + 1)} -> "
                data[position], data[position + 1] = data[position + 1], data[position]
                message += f"{colorize_swap(data, position, position + 1)}"
                if verbose > 0:
                    print(message)
                count -= 1
                position += 1
            elif tool == 1:
                exist_exchange = False
                exist_pos = 0
                for i in range(position, width - 1):
                    if (data[i] == 1) and (data[i + 2] == 0):
                        exist_exchange = True
                        exist_pos = i
                        break
                if not exist_exchange:
                    tool = 0
                    tool_change -= 1
                    position = input_change_tool - tool_change + 1
                    continue
                else:
                    position = exist_pos
                message = f"{colorize_swap(data, position, position + 2)} -> "
                data[position], data[position + 2] = data[position + 2], data[position]
                message += f"{colorize_swap(data, position, position + 2)}"
                if verbose > 0:
                    print(message)
                count -= 1
                position += 2
        if (count == 0) and (tool_change == 0):
            return list_bool_to_str(data)
        data = best[:]
    return ""

# if position == width - 1:
#     position = 0
# elif data[position] == 1:
#     if position == width - 1:
#         tool = 0
#         tool_change -= 1
#     elif data[position + 2] == 1:
#         if data[position + 1] == 1:
#             position += 2
#         else:
#             pass
#     else:
#         message = f"{colorize_swap(data, position, position + 2)} -> "
#         data[position], data[position + 2] = data[position + 2], data[position]
#         message += f"{colorize_swap(data, position, position + 2)}"
#         if verbose > 0:
#             print(message)
#         count -= 1
#         position += 2
# else:
#     position += 1
