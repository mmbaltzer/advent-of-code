rs = open('2022/data/day03_rucks.txt', 'r').read().split('\n')

def priority(l):
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'

    if uppercase.find(l) > 0:
        return uppercase.find(l) + 1 + 26
    else:
        return lowercase.find(l) + 1

score = 0
for ruck in rs:
    c1 = ruck[:len(ruck)//2]
    c2 = ruck[len(ruck)//2:]

    i = 0
    while(i < len(c1)):
        if c1[i] in c2:
            score += priority(c1[i])
            i = len(c1)
        else:
            i += 1

part_a = score



# part b
score = 0
i = 0
while (i < len(rs)):
    c1, c2, c3 = rs[i:i+3]
    i += 3
    j = 0
    while (j < len(c1)):
        if c1[j] in c2 and c1[j] in c3:
            score += priority(c1[j])
            j = len(c1)
        else:
            j += 1

part_b = score
print(part_b)