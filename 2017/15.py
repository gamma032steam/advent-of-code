d = 2147483647

def a_gen():
    a = 116
    fa = 16807 
    while True:
        a = (a * fa) % d
        if a % 4 == 0: yield a

def b_gen():
    b = 299
    fb = 48271
    while True:
        b = (b * fb) % d
        if b % 8 == 0: yield b

ag = a_gen()
bg = b_gen()

#k = 40000000
k = 5000000

c = 0
for _ in range(k):
    xa, xb = next(ag), next(bg)
    if xa & 0xFFFF == xb & 0xFFFF: c += 1

print(c)
