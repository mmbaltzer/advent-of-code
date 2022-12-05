stacks_string, movements = open('2022/data/day05.txt', 'r').read().split('\n\n')

class Move:
    def __init__(self, origin, destination, n):
        self.origin = origin
        self.destination = destination
        self.number = n

def move_crates(stacks, move):
    destination_stack = stacks[move.destination]
    origin_stack = stacks[move.origin]
    for _ in range(move.number):
        destination_stack.append(origin_stack.pop())

def move_crates_chunks(stacks, move):
    destination_stack = stacks[move.destination]
    origin_stack = stacks[move.origin]
    
    moving = []
    for _ in range(move.number):
        moving.append(origin_stack.pop())
    while moving:
        destination_stack.append(moving.pop())

def parse_move(move_string):
    words = move_string.split()
    return Move(int(words[3]) - 1, int(words[5]) - 1, int(words[1]))

stack_locations = {
    0: 1,
    1: 5,
    2: 9,
    3: 13,
    4: 17,
    5: 21,
    6: 25,
    7: 29,
    8: 33
}

stacks_arr = stacks_string.split('\n')
bottom_row = stacks_arr.pop()
n_stacks = int(bottom_row.strip()[-1])
stacks = [[] for _ in range(n_stacks)]

while stacks_arr:
    row = stacks_arr.pop()
    for stack_id, string_location in stack_locations.items():
        if row[string_location] != ' ':
            stacks[stack_id].append(row[string_location])

for move_string in movements.split('\n'):
    move = parse_move(move_string)
    move_crates_chunks(stacks, move)

result = ''
for s in stacks:
    result = result + s.pop()

print(result)