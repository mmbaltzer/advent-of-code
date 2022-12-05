pairs = open('2022/data/day04.txt', 'r').read().split('\n')

def get_bounds_from_assignment(assignment):
    lower, upper = assignment.split('-')
    return {'upper': int(upper), 'lower': int(lower)}

count_redundant = 0
count_overlap = 0
for pair in pairs:
    a1, a2 = pair.split(',')
    elf1, elf2 = get_bounds_from_assignment(a1), get_bounds_from_assignment(a2)
    if (elf1['upper'] - elf2['upper']) * (elf1['lower'] - elf2['lower']) <= 0:
        count_redundant += 1
    
    if (elf1['upper'] >= elf2['lower']) and (elf1['lower'] <= elf2['upper']):
        count_overlap += 1
    elif (elf2['upper'] >= elf1['lower']) and (elf2['lower'] <= elf1['upper']):
        count_overlap += 1
        
# part 1
print(count_redundant)
print(count_overlap)