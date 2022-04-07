
import enum


dist = 2503
#dist = 1000

if __name__ == "__main__":
    with open('./input/14.txt') as f:
        data = f.read().splitlines()
        reindeers = []
        for line in data:
            words = line.split(" ")
            reindeers.append((words[0], int(words[3]), int(words[6]), int(words[13])))

        best, best_deer = 0, ""
        for name, speed, time, rest in reindeers:
            full_increments, rem = divmod(dist, time + rest)
            #print(full_increments)
            my_dist = speed * time * full_increments
            my_dist += speed * min(time, rem)
            if my_dist > best:
                best = my_dist
                best_deer = name

        #print(best, best_deer)
        dists = [0] * len(reindeers)
        points = [0] * len(reindeers)
        for clock in range(dist):
            for i, stats in enumerate(reindeers):
                name, speed, time, rest = stats
                if clock % (time + rest) < time:
                    dists[i] += speed 

            best, best_idx = -1, -1
            for i, position in enumerate(dists):
                if position > best:
                    best = position
                    best_idx = i

            points[best_idx] += 1
        print(dists)
        print(points)