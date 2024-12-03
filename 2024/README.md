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