strategy = open('2022/data/day02_strategy.txt', 'r')

def score_of_b(a, b):
    beats = {
        'X': 'B',
        'Y': 'C',
        'Z': 'A'
    }
    ties = {
        'X': 'A',
        'Y': 'B',
        'Z': 'C'
    }
    scores = {
        'X': 1,
        'Y': 2,
        'Z': 3
    }
    score_win = 6
    score_draw = 3

    if (a == beats[b]):
        return scores[b]
    elif (a == ties[b]):
        return scores[b] + score_draw
    else:
        return scores[b] + score_win

def play_by_b(a, b):
    b_loses = {
        'A': 'Z',
        'B': 'X',
        'C': 'Y'
    }
    b_ties = {
        'A': 'X',
        'B': 'Y',
        'C': 'Z'
    }
    b_wins = {
        'A': 'Y',
        'B': 'Z',
        'C': 'X'
    }
    if b == 'X':
        return b_loses[a]
    if b == 'Y':
        return b_ties[a]
    else:
        return b_wins[a]


strat = [s.split(' ') for s in strategy.read().split('\n')]
# part a
part_a = sum([score_of_b(a,b) for a, b in strat])

# part b
# for a, b in strat:
#     print(play_by_b(a,b))
#     print(score_of_b(a, play_by_b(a, b)))
all_scores = [score_of_b(a, play_by_b(a, b)) for a, b in strat]
part_b = sum(all_scores)