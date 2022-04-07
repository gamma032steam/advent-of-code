if __name__ == "__main__":
    with open('./input/5.txt') as f:
        data = f.read().splitlines()

        res = 0
        vowels = 'aeiou'
        other = ["ab", "cd", "pq", "xy"]
        for word in data:
            v_count = 0
            for c in word:
                if c in vowels: v_count += 1
            if v_count < 3: continue

            found = False
            for i in range(len(word) - 1):
                if word[i] == word[i+1]:
                     found = True
                     break

            if not found: continue

            bad = False
            for o in other:
                if o in word: 
                    bad = True
                    break
            if bad: continue
            res += 1

        print(res)

        res = 0
        out = set()
        for word in data:
            found = False
            for i in range(len(word) -2):
                if word[i] == word[i+2]:
                     found = True
                     break
            if not found: continue

            found = False
            for i in range(len(word)-1):
                pair = word[i] + word[i+1]
                for j in range(i+2,len(word)-1):
                    cnd = word[j] + word[j+1]
                    if pair == cnd: found = True

            if not found: continue

            # pairs = dict()
            # found = False
            # for i in range(len(word) - 1):
            #     x = word[i] + word[i+1]
            #     if x in pairs and i - pairs[x] >= 2: 
            #         print(x)
            #         found = True
            #         break
            #     pairs[x] = i
            # if not found: continue
            out.add(word)
            res += 1
        
        out2 = set()
        for word in data:
            found = False
            for i in range(len(word) -2):
                if word[i] == word[i+2]:
                     found = True
                     break
            if not found: continue

            pairs = dict()
            found = False
            for i in range(len(word) - 1):
                x = word[i] + word[i+1]
                if x in pairs and i - pairs[x] >= 2: 
                    found = True
                    break
                pairs[x] = i
            if not found: continue
            out2.add(word)
            res += 1


        print(out - out2)