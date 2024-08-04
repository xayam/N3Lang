from typing import List

from n3utils import colorize_swap


def n3c_sort(input_data: List[int], verbose=0):
    data = input_data[:]
    width = len(data)
    ones = 0
    for i in data:
        if i == 1:
            ones += 1
    result = []
    best = [1] * ones + [0] * (width - ones)
    outputs = {
        "data": input_data,
        "false_operation": 1,
        "count": 0,
        "ones": ones,
        "zeros": width - ones,
        "position": 0,
        "tool_change": 0,
    }
    if best == data:
        return outputs, outputs
    for tool in [0, 1]:
        count = 0
        tool_change = 0
        position = width - 1
        last_use_position = position
        last_tool_position = position
        while best != data:
            if verbose > 0:
                print(f"c={count} o={ones} p={position} t={tool} " +
                      f"e={tool_change}, current={data}")
            if tool == 0:
                exist_exchange = False
                exist_pos = 0
                for i in range(position, 0, -1):
                    if (data[i] == 1) and (data[i - 1] == 0):
                        exist_exchange = True
                        exist_pos = i
                        break
                if not exist_exchange:
                    tool = 1
                    last_tool_position = position
                    tool_change += 1
                    position = width - 1
                    continue
                else:
                    position = exist_pos
                message = f"{colorize_swap(data, position, position - 1)} -> "
                data[position], data[position - 1] = data[position - 1], data[position]
                message += f"{colorize_swap(data, position, position - 1)}"
                last_use_position = position
                if verbose > 0:
                    print(message)
                count += 1
                position -= 1
            elif tool == 1:
                exist_exchange = False
                exist_pos = 0
                for i in range(position, 1, -1):
                    if (data[i] == 1) and (data[i - 2] == 0):
                        exist_exchange = True
                        exist_pos = i
                        break
                if not exist_exchange:
                    tool = 0
                    last_tool_position = position
                    tool_change += 1
                    position = width - 1
                    continue
                else:
                    position = exist_pos
                if data[position - 2] == 0:
                    message = f"{colorize_swap(data, position, position - 2)} -> "
                    data[position], data[position - 2] = data[position - 2], data[position]
                    message += f"{colorize_swap(data, position, position - 2)}"
                    last_use_position = position
                    if verbose > 0:
                        print(message)
                    count += 1
                position -= 2
        outputs = {
            "data": data,
            "false_operation": 0,
            "count": count - 1,
            "ones": ones,
            "zeros": width - ones,
            "position": last_use_position,
            "tool_change": tool_change,
        }
        result.append(outputs)
        data = input_data[:]
    return result


if __name__ == "__main__":
    pass
