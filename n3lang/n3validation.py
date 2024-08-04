import n3lang.n3recovery
from n3sort import n3c_sort
from n3utils import colorize_bool, colorize, get_n3sort_values


def n3c_validation():
    verbose = 0
    # print(get_annotation())
    print(f"Decompressing...")
    for width in [x for x in range(1, 7)]:
        no_conflict = True
        max_count = 0
        max_change_tool = 0
        max_bits = 1
        pars = dict()
        results0 = dict()
        results1 = dict()
        for d in range(2 ** width):
            s = f"{d:{width}b}".replace(" ", "0")
            arr = [int(char) for char in s]
            data = arr[:]
            if verbose > 0:
                print("Compressing...")
            result0, result1 = n3c_sort(data, verbose)
            results0[s] = f"c={result0[1]} o={result0[2]} " + \
                          f"p={result0[4]} t={result0[5]} e={result0[6]}"
            results1[s] = f"c={result1[1]} o={result1[2]} " + \
                          f"p={result1[4]} t={result1[5]} e={result1[6]}"
            # for step in [result0, result1]:
            #     data, count, ones, zero, pos, tool, change_tool = result0
            #
            #     pars[s] = f"c={count} o={ones} p={pos} t={tool} e={change_tool}"
            #     origin_pars = pars.copy()
            #     pars = {k: v for k, v in sorted(pars.items(), key=lambda item: item[1])}
            #
            #     if count > max_count:
            #         max_count = count
            #     if change_tool > max_change_tool:
            #         max_change_tool = change_tool
            #     bits = 1
            #     bits += math.ceil(math.log2(max_count + 1))
            #     bits += math.ceil(math.log2(max_change_tool + 1))
            #     bits += 2 * math.ceil(math.log2(width))
            #     if bits > max_bits:
            #         max_bits = bits
            #     assertion = data == [1] * ones + [0] * zero
            #     assert assertion
            #     # print("Decompressing...")
            #     # recovery = n3c_recovery(width, count, ones, pos, tool, change_tool, 1)
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
            #         print(f"{arr} -> {data} -> {recovery}")
            #         print(f"{colorize(' ERROR ')} input != output")
            #         sys.exit(1)
            #     if not no_conflict:
            #         if verbose > 0:
            #             print(f"{colorize(' ERROR ')} Collision found")
            #             print(origin_pars)
            #             print(pars)
            #         continue
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
        conflict = []
        for i in r0:
            result[r0[i][0]] = i
            for j in r0[i][1:]:
                for k in r1:
                    if j in r1[k]:
                        result[j] = k
                        conflict.append(f"{j}_{k}")
                        break
        # print(result)
        # print(
        #     f"width={width}",
        #     len(conflict), len(set(conflict)),
        #     len(result), len(set(result.values()))
        # )
        for k, v in result.items():
            values = get_n3sort_values(v)
            if values:
                count, ones, pos, tool, change_tool = values
                params = {
                    "width": width,
                    "count": count,
                    "ones": ones,
                    "pos": pos,
                    "tool": tool,
                    "change_tool": change_tool,
                    "verbose": 0
                }
                recovery = n3lang.n3recovery.n3c_recovery(**params)
                # print(width, recovery)
                assertion = recovery == k
                print(f"{colorize_bool(assertion)} width={width} | {k} -> '{v}' -> {recovery}")
                if not assertion:
                    params["verbose"] = 1
                    n3lang.n3recovery.n3c_recovery(**params)
                assert assertion
                # break
        if not no_conflict:
            pass


if __name__ == "__main__":
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
