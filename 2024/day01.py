import numpy as np

def pt_1():
    lists = np.loadtxt('./input/day01a.txt')
    sorted_lists = np.sort(lists, axis=0)
    differences = abs(np.diff(sorted_lists))
    return np.sum(differences)

def pt_2():
    lists = np.loadtxt('./input/day01a.txt')
    similarity = []

    # For each value in the left list, compute a similarity score
    for value in lists[:,0]:
        # Count the times value occurs in the right list
        count = np.count_nonzero(lists[:,1] == value)
        # The similarity score for each value is the product of the value and the count
        similarity.append(value * count)

    return sum(similarity)


print(pt_1())
print(pt_2())