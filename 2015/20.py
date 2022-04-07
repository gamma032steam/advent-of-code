input = 29000000

# house = [0] * (input // 10)

# for i in range(1, input // 10):
#     for j in range(i, input // 10, i):
#         house[j] += i * 10

# for i, h in enumerate(house):
#     if h >= input:
#         print(i)
#         break

house = [0] * (input // 11)

for i in range(1, input // 11):
    x = i
    for k in range(50):
        if x >= len(house): break
        house[x] += i * 11
        x += i


for i, h in enumerate(house):
    if h >= input:
        print(i)
        break