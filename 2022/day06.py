signal = open('2022/data/day06.txt', 'r').read()

marker = []
count = 0
while len(marker) < 14 and len(signal) > 0:
    next_char = signal[count]
    count += 1
    while next_char in marker:
        marker.pop(0)
    marker.append(next_char)

# part a
print(count)