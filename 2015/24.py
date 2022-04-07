from functools import reduce
def pick(results, current_sum, current_used, weights, target, i, bad):
    if bad and len(results) > 1: return
    if i in bad:
         pick(results, current_sum, current_used, weights, target, i + 1, bad)

    if current_sum == target:
        results.append(set(current_used))
        return

    if current_sum > target:
        return 

    if i >= len(weights): return
    # either take or don't take i
    used = current_used
    used.add(i)
    pick(results, current_sum + weights[i], used, weights, target, i + 1, bad)
    used.remove(i)
    pick(results, current_sum, used, weights, target, i + 1, bad)


if __name__ == "__main__":
    with open('./input/24.txt') as f:
        data = f.read().splitlines()
        total = sum([int(w) for w in data])
        target = total / 3
        print(target)

        res = []
        d = [int(w) for w in data]
        d.sort(reverse=True)
        pick(res, 0, set(), tuple(d), target, 0, set())
        print(res)
        

        # filter out cands that rem can't divide up
        new_cands = []
        for cand in res:
            res_2 = []
            pick(res_2, 0, set(), tuple(d), target, 0, set(cand))
            if res_2 == []: continue
            new_cands.append(cand)

        print([[d[e] for e in c] for c in new_cands])
        
        min_len = min([len(s) for s in new_cands])
        final_cand = []
        for cand in new_cands:
            if len(cand) == min_len: final_cand.append(cand)

        print(final_cand)
        final_cand = ([[d[e] for e in c] for c in final_cand])
        sizes = [reduce(lambda x, y: x * y, z) for z in final_cand]
        sizes.sort()
        print(sizes)
        print(sizes[0])

