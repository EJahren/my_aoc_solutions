from collections import defaultdict

houses = defaultdict(lambda: 0)

for i in range(1, 1000000):
    delivered = 0
    for j in range(i, 1000000, i):
        if delivered >= 50:
            break
        houses[j] += i * 11
        delivered += 1

for house, presents in houses.items():
    if presents > 29000000:
        print(house)
        break
