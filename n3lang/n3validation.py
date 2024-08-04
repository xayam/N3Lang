import math
import pprint
import sys

import n3lang.n3recovery
from n3sort import n3c_sort
from n3utils import colorize_bool, get_n3sort_values, get_sum_width, list_to_str, progress


def n3c_validation():
    verbose = 0
    # print(get_annotation())
    print(f"Decompressing...")
    width = 0
    # while True:
    for width in range(3, 4):
        # [8, 32, 512, 65536]
        # width += 1
        results0 = dict()
        results1 = dict()
        for d in range(2 ** width):
            s = f"{d:{width}b}".replace(" ", "0")
            arr = [int(char) for char in s]
            data = arr[:]
            if verbose > 0:
                print("Compressing...")
            result0, result1 = n3c_sort(data, verbose)
            results0[s] = f"f={result0['false_operation']} c={result0['count']} o={result0['ones']} " + \
                          f"p={result0['position']} e={result0['tool_change']}"
            results1[s] = f"f={result0['false_operation']} c={result1['count']} o={result1['ones']} " + \
                          f"p={result1['position']} e={result1['tool_change']}"
        # print(results0)
        # print(results1)
        r0 = dict()
        for k, v in results0.items():
            if not r0.__contains__(v):
                r0[v] = []
            r0[v].append(k)
        r1 = dict()
        for k, v in results1.items():
            if not r1.__contains__(v):
                r1[v] = []
            r1[v].append(k)
        result = dict()
        index = -1
        conflict = 0
        pprint.pprint(r0)
        # pprint.pprint(r1)
        # result = r0.copy()
        for i in r0:
            index += 1
            if len(r0[i]) == 1:
                result[i] = r0[i][0]
            else:
                conflict += 1
                # reverse = index
                # for j in r1:
                #     reverse -= 1
                #     # if (len(r1[j]) == 1) and
                #     if reverse < 0:
                #         result[i] = r1[j][0]
        # pprint.pprint(result)
        # sys.exit()
        # len_result = len(result)
        # len_set_result = len(set(result.values()))
        # print(
        #     f"width={str(width).rjust(2, ' ')}",
        #     # f"len_result={str(len_result).rjust(6, ' ')}, ",
        #     # f"len_set_result={str(len_set_result).rjust(5, ' ')}"
        # )
        for k, v in result.items():
            keys = get_n3sort_values(k)
            if keys:
                # print(keys)
                false_operation, count, ones, position, tool_change = keys
                inputs = {
                    "width": width,
                    "false_operation": false_operation,
                    "count": count,
                    "ones": ones,
                    "position": position,
                    "tool_change": tool_change,
                    "verbose": 0
                }
                recovery = n3lang.n3recovery.n3c_recovery(**inputs)
                assertion = recovery == v
                variants = []
                for j in r1:
                    if v in r1[j]:
                        variants.append(j)
                if assertion:
                    print(f"{colorize_bool(assertion)} width={width} " + \
                          f"conflict={conflict} '{v}' -> '{k}' -> '{recovery}'")
                if not assertion:
                    # pass
                    # pprint.pprint(r0)
                    # pprint.pprint(r1)
                    # inputs["verbose"] = 1
                    # recovery = n3lang.n3recovery.n3c_recovery(**inputs)
                    false_operation, count, ones, position, tool_change = get_n3sort_values(variants[0])
                    inputs = {
                        "width": width,
                        "false_operation": false_operation,
                        "count": count,
                        "ones": ones,
                        "position": position,
                        "tool_change": tool_change,
                        "verbose": 1
                    }
                    recovery = n3lang.n3recovery.n3c_recovery(**inputs)
                    assertion = recovery == v
                    print(f"{colorize_bool(assertion)} width={width} " + \
                          f"conflict={conflict} '{v}' -> '{variants[0]}' -> '{recovery}'  +++")
                    sys.exit()


def main(degrees=None, verbose=0) -> str:
    if degrees is None:
        windows = [2 ** i - 1 for i in [1, 2, 3, 5, 9, 16]]
    else:
        windows = [2 ** i for i in degrees]
    result = ""
    index = 0
    for width in windows:
        index += 1
        summa = get_sum_width(width)
        summa = math.ceil(summa)
        max_count = 2 ** summa
        max_ones = width
        max_bits_key = summa + math.ceil(math.log2(max_ones + 1)) + 1
        percent = max_bits_key / width
        result += \
            f"index={str(index).rjust(1, ' ')}, " + \
            f"width={str(width).rjust(5, ' ')}, " + \
            f"summa={str(summa)[:3].rjust(2, ' ')}, " + \
            f"max_count={str(max_count).rjust(14, ' ')}, " + \
            f"max_ones={str(max_ones).rjust(5, ' ')}, " + \
            f"max_bits_key={str(max_bits_key).rjust(2, ' ')}, " + \
            f"percent={str(100 * percent)[:6].rjust(6, ' ')}%\n"
    if verbose > 0:
        print(result)
    return result


if __name__ == "__main__":
    # ? P(W)
    # P(W) = lim sum log2[x + 1], x = 1 to log2[y] as y->W
    # L = math.ceil(P(W)) + 1

    # main(degrees=[3, 9, 23, 55], verbose=1)

    # main(verbose=1)

    n3c_validation()

# results0 = {k: v for k, v in sorted(results0.items(), key=lambda i: i[1])}
# print(f"!!!!!!{len(results0)}, {len(set(results0.values()))}")
# results1 = {k: v for k, v in sorted(results1.items(), key=lambda i: i[1])}

# if verbose > 0:
#     print(origin_pars)
#     print(pars)
# for i in pars:
#     if pars[i] == pars[s]:
#         print(f"width={str(width).rjust(2, ' ')} | " + \
#               f"{str(int(s, 2)).rjust(2, ' ')} <-> " + \
#               f"{str(int(i, 2)).rjust(2, ' ' )} = " + \
#               f"'{s.rjust(31, ' ')}' <-> " + \
#               f"'{i.rjust(31, ' ')}' = '{pars[s]}'")
#         break

# for i in pars:
#     if (pars[i] == pars[s]) and (i != s):
#         print(f"w={str(width).rjust(2, ' ')} | " + \
#               f"{str(int(s, 2)).rjust(3, ' ')} <-> " + \
#               f"{str(int(i, 2)).rjust(3, ' ')} = " + \
#               f"'{s.rjust(9, ' ')}' <-> " + \
#               f"'{i.rjust(9, ' ')}' = '{pars[s]}'")
#         break

# print(result)
# print(
#     f"width={width}",
#     len(conflict), len(set(conflict)),
#     len(result), len(set(result.values()))
# )

# for step in [result0, result1]:
#     degrees, count, ones, zero, position, tool, tool_change = result0
#
#     pars[s] = f"c={count} o={ones} p={position} t={tool} e={tool_change}"
#     origin_pars = pars.copy()
#     pars = {k: v for k, v in sorted(pars.items(), key=lambda item: item[1])}
#
#     if count > max_count:
#         max_count = count
#     if tool_change > max_change_tool:
#         max_change_tool = tool_change
#     bits = 1
#     bits += math.ceil(math.log2(max_count + 1))
#     bits += math.ceil(math.log2(max_change_tool + 1))
#     bits += 2 * math.ceil(math.log2(width))
#     if bits > max_bits:
#         max_bits = bits
#     assertion = degrees == [1] * ones + [0] * zero
#     assert assertion
#     # print("Decompressing...")
#     # recovery = n3c_recovery(width, count, ones, position, tool, tool_change, 1)
#     recovery = arr
#     assertion = recovery == arr
#     len_pars = len(origin_pars)
#     len_set_pars = len(set(origin_pars.values()))
#     no_conflict = len_pars == len_set_pars
#     can_compress = max_bits <= width
#     if verbose > 0:
#         print(
#             f"{colorize_bool(no_conflict)} " +
#             f"{colorize_bool(can_compress)} " +
#             f"width={width}, arr={arr}, all={len_pars}, unique={len_set_pars}" +
#             f"{str(100 * (d + 1) / 2 ** width)[0:6].rjust(7, ' ')}%, " + \
#             # f"arr={arr}, recovery={recovery}, " + \
#             f"max_bits={max_bits}, max_count={max_count}, " + \
#             f"max_change_tool={max_change_tool}")
#     if not assertion:
#         print(f"{arr} -> {degrees} -> {recovery}")
#         print(f"{colorize(' ERROR ')} input != output")
#         sys.exit(1)
#     if not no_conflict:
#         if verbose > 0:
#             print(f"{colorize(' ERROR ')} Collision found")
#             print(origin_pars)
#             print(pars)
#         continue
