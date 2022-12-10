import math
movelist = open('2022/data/day09.txt', 'r').read().split('\n')

def cartesian(p1, p2):
    sum_sq =  (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2
    return math.sqrt(sum_sq)

def update_knot(lead, trail, move):
    new_lead = move_knot(lead, move)

    if cartesian(new_lead, trail) >= 2:
        if abs(move[0]) + abs(move[1]) > 1:
            if cartesian(new_lead, move_knot(trail, move)) == 1:
                next_knot_move = move
            else:
                next_knot_move = [(x-y)//2 for x, y in zip(new_lead, trail)]
        else: 
            next_knot_move = measure_move(trail, lead)
    else:
        next_knot_move = [0, 0]
    
    return new_lead, next_knot_move

def move_knot(knot, move):
    return [sum(x) for x in zip(knot, move)]

def measure_move(knot_origin, knot_destination):
    return [ x - y for x, y in zip(knot_destination, knot_origin)]

def move_all_knots(knots, move):
    n_knots = len(knots)
    next_knot_move = move
    
    for i in range(n_knots-1):
        knots[i], next_knot_move = update_knot(knots[i], knots[i+1], next_knot_move)
    # move last knot
    knots[n_knots-1] = move_knot(knots[n_knots-1], next_knot_move)
    
    return knots

move_map = {
    'R': [0,1],
    'L': [0, -1],
    'U': [1, 0],
    'D': [-1, 0]
}

def locations_visited(moves, n_knots):
    locations = set()
    knots = [[0,0] for _ in range(n_knots)]

    for move in moves:
        knots = move_all_knots(knots, move)
        locations.add(tuple(knots[n_knots - 1]))

    return locations

moves_encoded = [[e.split()[0], int(e.split()[1])] for e in movelist]
moves = []
for line in moves_encoded:
    for _ in range(line[1]):
        moves.append(move_map[line[0]])

# part a 5695
print(len(locations_visited(moves, 2)))
# part b 2434
print(len(locations_visited(moves, 10)))
