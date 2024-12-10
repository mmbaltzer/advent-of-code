# Advent of Code Solutions
This directory contains Python solutions and guides for [Advent of Code 2024](https://adventofcode.com/2024). Thank you to the authors of that project for creating the challenges and competition.

These guides are provided for educational purposes well after any competitive solving has concluded. To comply with Advent of Code usage policies, I do not reproduce problem text or puzzle inputs, so you'll need to visit [the site](https://adventofcode.com/2024) for context.

## Day 01
#### Part One
First, let's summarize the text of the problem. If it is helpful to you, [write this summary as comments](#write-out-the-plan) to outline the structure of the solution steps.
For Day 01, you are given two lists of numbers and need to calculate the total distance between them.

The first lines of code written are to load the input data into variable(s). This puzzle asks you to compare two lists of integer values, so a reasonable data structure to choose for your solution is two Python `List`s of `int`s. For a more extensible data structure, you could instead create a 2-dimensional Python list. See [Getting Started](#getting-started) for guidance on parsing the input.

The problem text asks you to pair up the "smallest number in the left list with the smallest number in the right list..." You could translate this direction into code by finding smallest value from each list, comparing it to the smallest value from the other list, and so on
```python
def calculate_distances(left: List[int], right: List[int]):
    distances = []
    while len(left) > 0:
        min_left = min(left)
        min_right = min(right)

        distance = abs(min_left - min_right)
        distances.append(distance)
        # remove the two values which we have processed
        left.remove(min_left)
        right.remove(min_right)

    return distances
```

However, there is a [simplification](#simplifying-the-problem) available by sorting the lists *before* trying calculating the difference. If you sort, the nth largest element is in the nth index, so the above becomes
```python
def calculate_distances(left: List[int], right: List[int]):
    left.sort()
    right.sort()
    
    distances = []
    for i in range(len(left)):
        distance = abs(left[i] - right[i])
        distances.append(distance)
    
    return distances
```
This could optionally be made more concise with the use of a list comprehension. In reading the example, you can see that the distances in the problem definition are never negative, so we can take the absolue value of each distance before appending to the list.

Now that we have a list of the distances, we can compute the total distance which is the sum of all the pairs of distances.
```python
def pt_1(left, right):
    distances = calculate_distances(left, right)
    total_distance = sum(distances)
    return total_distance
```
#### Part Two
In Part Two, you are asked to calculate a similarity score for two lists. For each value in the left list, multiply it by the number of times it is found in the right list. The total similarity is the sum of the similarity scores for each value in the left list.

The data sctructure chosen in the previous part is still a good choice for this problem. In fact, the overall ask is very similar; however, instead of calculating the distance for each value in the left list, we are looking for the similarity score. We can simply replace the `calculate_distances` function from Part One with a new function, `calculate_scores`.

```python
def calculate_scores(left, right):
    scores = [value * right.count(value) for value in left]
    return scores

def pt_2(left, right):
    similarity_scores = calculate_scores(left, right)
    total_similarity = sum(similarity_scores)
    return total_similarity
```
I used a [list comprehension](https://docs.python.org/3.13/tutorial/datastructures.html#list-comprehensions), but this is functionally the same as writing a `for` loop.

#### Using `numpy`
The solution in [day01.py](day01.py) uses the `numpy` library. Built-in functions in that library automatically parse the input, calculate the differences, etc. See [Numpy Reference](https://numpy.org/doc/2.1/reference/routines.html) for detail on these functions. I use the `np.diff` function in place of a list comprehension as I find it more readable.

## Day 02
#### Part One
For Day 2, we are given a list of reports, and we must determine how many of the reports are safe.

Each report is a line of the input, and safety is calculated based on the difference between a sequence of integer "levels". Therefore, a 2D list of ints is a good choice for a data structure. Here is how we might structure our solution:
```python
def parse_input(filename):
    lines = open(filename).readlines()
    reports = [[int(num) for num in line.split()] for line in lines]
    return reports

def pt_1(reports):
    safe_reports = [is_safe(report) for report in reports]
    return safe_reports.count(True)
```
For each report, we need to check if it is safe to run. There is a list of conditions which make a report safe, so we can translate those into code as follows:
```python
def is_safe(report):
    # Calculate the differences between adjacent levels
    diffs = np.diff(report)
    # A report is safe if all levels increase by 1-3
    if np.all(diffs > 0) and np.all(diffs <= 3):
        return True
    # A report is safe if all levels decrease by 1-3
    if np.all(diffs < 0) and np.all(diffs >= -3):
        return True
    return False
```
Here we have an opportunity to simplify the problem. The conditions for a "safe" report are verbose because we have to consider if the report is ascending or descending. This layer of complexity can also be confusing to reason about when coding. However, this is simplified by reframing the problem: instead of having both ascending and descending reports, we can reverse the order of any descending reports. That way, we will have only to consider ascending reports when determining safety.

By adding a few lines of code, we can simplify the conditionals as follows:
```python
def is_safe(report):
    diffs = np.diff(report)

    # if the report is in descending order, reverse it
    if sum(diffs < 0) > 1:
        report.reverse()
        diffs = np.diff(report)

    # A report is safe if all levels increase by 1-3
    return np.all(diffs > 0) and np.all(diffs <= 3)
```
#### Part Two
In Part Two, we are asked to find the reports which are safe or can be *made* safe by removing one level from the report.
```python
def pt_2(reports):
    safe_reports = [is_safe(report) or can_be_made_safe(report) for report in reports]
    return safe_reports.count(True)
```
A brute force solution is to try removing each level from a report to see if it is safe after removing it.
```python
def can_be_made_safe(report):
    # For each level in a report, check if the report is safe after removing that level
    for i in range(len(report)):
        edited_report = report[:i] + report[i+1:]
        if is_safe(edited_report):
            return True
    # Removing any one level did not make the report safe
    return False
```
You don't have to try removing every level in the report: you need only try removing the two levels involved in the *first* safety violation. If that does not make the report safe, nothing will. That solution is provided in [day02.py](day02.py).

## Day 03
#### Part One
This problem instructs you to find sequences of characters within a long string of characters. From those sequences, you need to extract two values and multiply them together.

The memory input is best kept in a string as it is alphanumeric. `regex` is a good tool for finding a pattern within a string.

First, determine the regex pattern of the sequence you are looking for. Use a tool like [regexr.com](regexr.com) or even an LLM. Use capturing groups to extract the values to be multiplied.

Now you can find all the instances that match your input pattern, multiply them, and sum those products.

```python
def pt_1(memory: str) -> int:
    regex_instructions = r'mul\((\d{1,3}),(\d{1,3})\)'
    instructions = re.findall(regex_instructions, memory)

    products = [int(a) * int(b) for a, b in instructions]
    return sum(products)
```

#### Part Two
Now there are three kinds of sequences to find in the memory string; use the regex OR `|` operator to find any of the three strings.

Once you have extracted the instructions from the memory string, you need to check which of the multiply operations to perform and which to skip. Loop over all the instructions, keeping a state variable to track whether `do()` or `dont()` was the most recently seen instruction.

```python
def interpret_instructions(instructions: List[str]) -> int:
    do_mul = True
    total = 0
    for instruction in instructions:
        # instruction is a mul instruction
        if instruction[0] and do_mul:
            total += int(instruction[0]) * int(instruction[1])
        # instruction matches "do()"
        elif instruction[2]: 
            do_mul = True
        # instruction matches "don't()"
        elif instruction[3]:
            do_mul = False
    return total
```

<!-- ## Day 04
#### Part One
```python
# Check right
if in_bounds(arr,i,j+3):
    search = [arr[i][j+k] for k in range(4)]
    if search == word:
        total += 1
```
This pattern can be repeated eight times in order to check each possible word orientation.

This does result in repetitive code, though it is quick to read. A less repetive solution is to parametrize the directions to check by creating a list of directions
```python
directions = [[0, 1], [0, -1], [-1, 0], [1, 0],   # right, left, up, down
              [1, 1], [1, -1], [-1, 1], [-1, -1]] # down-right, down-left, up-right, up-left
```

#### Part Two -->

## Day 10
#### Part One
The problem asks you to find the number of valid trails in a map. A trail starts at 0 and increases monotonically by one until it is height 9, its peak. You are asked for a trail score calculated using the number of peaks that can be reached from each trailhead.

This is a search problem in two dimensions: you are asked to find paths through a 2-dimensional space.

For this problem, we can use an integer array to store the topographical map. This will be helpful in accessing specific coordinates in the map and comparing the values of adjacent locations.

Knowing the above, we can begin writing the solution. As with every problem, we must write some code to parse the input text into our desired data structure. See `parse_input()` in [day10.py](day10.py).

From the problem, we are asked to find the trails for each trailhead in order to calculate their scores. We can begin to write out the structure of the solution as follows:
```python
def pt_1(topo_map) -> int:
    trailheads = get_trailheads(topo_map)
    trail_peaks = [get_trails_for_trailhead(topo_map, head) for head in trailheads]
    ...
```
These two methods will have the bulk of code, so let's implement them next. In order to get the trailheads, we can loop over every element of the topographic map and check if it is equal to zero. We need to store the coordinates of the trailheads so that we can use them as the starting points of our trail searches.
```python
def get_trailheads(topo_map):
    trailheads = []
    for i in range(len(topo_map)):
        for j in range(len(topo_map[i])):
            if topo_map[i][j] == 0:
                trailheads.append((i, j))
    return trailheads

def test_get_trailheads():
    topo = parse_input("input/day10_example.txt")
    trailheads = get_trailheads(topo)
    expected = [(0, 2), (0, 4), (2, 4), (4, 6), (5, 2), (5, 5), (6, 0), (6, 6), (7, 1)]
    assert trailheads == expected
```
At the solutions become more complex, unit testing the functions becomes very useful. I included a test that uses the example input.

`get_trails_for_trailhead` is a path searching function. The input, a topographical map, can be modeled as a graph data structure, where each level is a node and there are up to four branches (left, right, up, down). The most common algorithms for searching a graph is breadth-first search and depth-first search. To implement a breadth-first search, we start at the root of our graph (the trailhead), and add each of the possible directions to walk to a queue of locations "to-visit". Then we take the location at the top of the queue, find the possible directions from *that* spot, and add the possibilities to the queue. We need to check each node that is taken off the queue to see if it is the destination we are trying to reach.

```python
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
```

Though we are thinking about this map as a graph, we do not need to worry about cycles because of the constraint that the path increase by 1 at each position. This makes loops in the path impossible.

With these functions implemented, we can finish by calculating the score for each trailhead. Note that in the searching function, the coordinates of hte peak are added to a list, but they might be added more than once if there is more than one path to the peak. To account for this, we can create a set of the peak coordinates, and find the length of the set when calculating the score.

```python
def pt_1(topo_map):
    trailheads = get_trailheads(topo_map)

    trail_peaks = [get_trails_for_trailhead(topo_map, head) for head in trailheads]
    trailhead_scores = [len(set(peaks)) for peaks in trail_peaks]

    return sum(trailhead_scores)
```

#### Part Two
In part two, the score calculation has changed slightly. In part one, the score of a trailhead was equal to the number of peaks you could reach from it. In part two, the score of a trailhead is the number of paths to peaks you can take.

The solution in Part One is already structured to return a list of paths to peaks from the BFS function. So we only need to remove the set operation in order to calculate this new score.

```python

def pt_2(topo_map):
    trailheads = get_trailheads(topo_map)

    trail_peaks = [get_trails_for_trailhead(topo_map, head) for head in trailheads]
    trailhead_scores = [len(peaks) for peaks in trail_peaks]

    return sum(trailhead_scores)
```

# Appendix
## Getting Started
The first step to solving all Advent of Code challenges is to store a variable with the puzzle input. It is possible to paste the input directly into a variable assignment,
```python
input = [1, 2, 3, 4]
```
but it is easier in the long-term to have an input parsing pattern that you follow. 
It is convenient to store puzzle input in a separate file, so that you can 

## Problem Solving Strategies
### Write out the plan
### Understand the Example
### Simplifying the problem