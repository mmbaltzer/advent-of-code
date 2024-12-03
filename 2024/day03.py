import regex as re
from typing import List

def pt_1(memory: str) -> int:
    regex_instructions = r'mul\((\d{1,3}),(\d{1,3})\)'
    instructions = re.findall(regex_instructions, memory)

    products = [int(a) * int(b) for a, b in instructions]
    return sum(products)

def pt_2(memory: str) -> int:
    regex_instructions = r'mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don\'t\(\))'
    instructions = re.findall(regex_instructions, memory)
    score = interpret_instructions(instructions)
    return score

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

def parse_input(file_path):
    with open(file_path, 'r') as f:
        return f.read()

if __name__ == '__main__':
    memory = parse_input('./input/day03.txt')

    print(pt_1(memory))
    print(pt_2(memory))