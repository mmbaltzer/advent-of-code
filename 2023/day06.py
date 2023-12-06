import numpy as np
input_string = open('2023/data/day06.txt').read()

class Race:
    def __init__(self, time, distance):
        self.time = time
        self.distance = distance

def parse_input(input_string):
    times = input_string.split('\n')[0].split()[1:]
    distances = input_string.split('\n')[1].split()[1:]

    return [Race(int(times[i]), int(distances[i])) for i in range(len(times))]

def find_ways_to_win(race):
    """
    this is a system of 3 equations: where t_1 is travel time and t_2 is button hold time
    d = v * t_1
    v = t_2
    t = t_1 + t_2 = race.time

    we want to know about the solutions where d > race.distance
    therefore, race.distance < v * t_1
    race.distance < t_2 * t_1 by substitution
    t_2 ^2 - t*t_2 + race.distance < 0
    the solutions to this quadratic formula are the boundaries (exclusive)
    of the range of t_2 values that result in beating the record
    """
    roots = np.roots([1, -race.time, race.distance])
    # the record-setting options is the number of integers between the roots
    n_options = np.floor(max(roots)-0.0001) - np.ceil(min(roots)+0.0001) + 1
    return n_options

def pt1():
    # parse input string into race object
    races = parse_input(input_string)
    # for each race length find out how many ways to beat the record
    ways_to_win = [find_ways_to_win(race) for race in races]
    # multiply the nways to beat each record
    solution = np.prod(ways_to_win)
    return solution

def pt2():
    races = [Race(47707566, 282107911471062)]
    # for each race length find out how many ways to beat the record
    ways_to_win = [find_ways_to_win(race) for race in races]
    # multiply the nways to beat each record
    solution = np.prod(ways_to_win)
    return solution

print(pt1())
print(pt2())