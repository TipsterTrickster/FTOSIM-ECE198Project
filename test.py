size = 3

for n in range((size // 2)): # swaps bars on U BR & F faces
    for j in range(n + 1):
        print(j ** 2 - 1 - n * 2)