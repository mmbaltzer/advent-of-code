def pt_1(topo_map):
    trailheads = get_trailheads(topo_map)

    trail_peaks = [get_trails_for_trailhead(topo_map, head) for head in trailheads]
    trailhead_scores = [len(set(peaks)) for peaks in trail_peaks]

    return sum(trailhead_scores)


def pt_2(topo_map):
    trailheads = get_trailheads(topo_map)

    trail_peaks = [get_trails_for_trailhead(topo_map, head) for head in trailheads]
    trailhead_scores = [len(peaks) for peaks in trail_peaks]

    return sum(trailhead_scores)


def get_trailheads(topo_map):
    trailheads = []
    for i in range(len(topo_map)):
        for j in range(len(topo_map[i])):
            if topo_map[i][j] == 0:
                trailheads.append((i, j))
    return trailheads


def get_trails_for_trailhead(topo_map, trailhead):
    peaks = []
    to_visit = [trailhead]

    while to_visit:
        x, y = to_visit.pop(0)
        # If this is a peak, add it to the list of peaks
        if topo_map[x][y] == 9:
            peaks.append((x,y))
            continue
            
        # Check each direction for a neighbor that is 1 higher
        directions = [(0, 1), 
                      (1, 0), 
                      (0, -1), 
                      (-1, 0)]
        for dx, dy in directions:
            neighbor = topo_map[x+dx][y+dy] if in_bounds(topo_map, x+dx, y+dy) else -1
            
            # If the neighbor is 1 higher, add it to the list of places to visit
            if neighbor - topo_map[x][y] == 1:
                to_visit.append((x+dx, y+dy))
    
    return peaks


def in_bounds(topo_map, x, y):
    return 0 <= x < len(topo_map) and 0 <= y < len(topo_map[0])


def parse_input(file):
    with open(file) as f:
        topo_map = [[int(loc) for loc in line.strip('\n')] for line in f.readlines()]
        return topo_map

def test_parse_input():
    topo = parse_input("input/day10_example.txt")
    expected = [8,9,0,1,0,1,2,3]

    assert topo[0] == expected

def test_get_trailheads():
    topo = parse_input("input/day10_example.txt")
    trailheads = get_trailheads(topo)
    expected = [(0, 2), (0, 4), (2, 4), (4, 6), (5, 2), (5, 5), (6, 0), (6, 6), (7, 1)]
    assert trailheads == expected

if __name__ == "__main__":
    topo_map = parse_input("input/day10.txt")
    # run tests
    test_parse_input()
    test_get_trailheads()

    # print solutions
    print(pt_1(topo_map))
    print(pt_2(topo_map))