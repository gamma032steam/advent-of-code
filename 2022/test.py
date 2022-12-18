x = 0
for i in range(1000000000000):
    if i % (1000000000000 / 500) == 0: print(i)
    x += 1

print(x)