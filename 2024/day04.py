from typing import List

def pt_1(puzzle: List[str]) -> int:

    words_found = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            words_found += check_xmas(puzzle, i, j)

    return words_found
    

def check_xmas(arr, i, j):
    if arr[i][j] != 'X':
        return 0
    
    word = ['X', 'M', 'A', 'S']
    total = 0
    # Check right
    if in_bounds(arr,i,j+3):
        search = [arr[i][j+k] for k in range(4)]
        if search == word:
            total += 1
    
    # Check left
    if in_bounds(arr,i,j-3):
        search = [arr[i][j-k] for k in range(4)]
        if search == word:
            total += 1
    
    # Check down
    if in_bounds(arr,i+3,j):
        search = [arr[i+k][j] for k in range(4)]
        if search == word:
            total += 1

    # Check up
    if in_bounds(arr,i-3,j):
        search = [arr[i-k][j] for k in range(4)]
        if search == word:
            total += 1
    
    # Check down-right
    if in_bounds(arr,i+3,j+3):
        search = [arr[i+k][j+k] for k in range(4)]
        if search == word:
            total += 1
        
    # Check down-left
    if in_bounds(arr,i+3,j-3):
        search = [arr[i+k][j-k] for k in range(4)]
        if search == word:
            total += 1
    
    # Check up-right
    if in_bounds(arr,i-3,j+3):
        search = [arr[i-k][j+k] for k in range(4)]
        if search == word:
            total += 1
    
    # Check up-left
    if in_bounds(arr,i-3,j-3):
        search = [arr[i-k][j-k] for k in range(4)]
        if search == word:
            total += 1

    return total


def pt_2(puzzle: str) -> int:
    words_found = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            words_found += check_x_mas(puzzle, i, j)
    return words_found

def check_x_mas(arr, i, j):
    if arr[i][j] != 'A':
        return 0
    
    corners = [[i+1, j+1], 
               [i+1, j-1], 
               [i-1, j+1], 
               [i-1, j-1]]
    
    if all([in_bounds(arr, x, y) for x, y in corners]):
        search = [arr[x][y] for x, y in corners]
        if any([search == ['M', 'M', 'S', 'S'],
                search == ['M', 'S', 'M', 'S'],
                search == ['S', 'M', 'S', 'M'],
                search == ['S', 'S', 'M', 'M']]):
            return 1
    return 0

def in_bounds(arr, i, j):
    return i < len(arr) and j < len(arr[i]) and i >= 0 and j >= 0

def parse_input(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
        return text.split('\n')

if __name__ == '__main__':
    puzzle = parse_input('./input/day04_example.txt')

    print(pt_1(puzzle))
    print(pt_2(puzzle))