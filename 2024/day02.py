import numpy as np

def pt_1(reports):
    safe_reports = [is_safe(report) for report in reports]
    return safe_reports.count(True)

def pt_2(reports):
    safe_reports = [is_safe(report) or can_be_made_safe(report) for report in reports]
    return safe_reports.count(True)

def is_safe(report):
    diffs = np.diff(report)

    # if the report is in descending order, reverse it
    if sum(diffs < 0) > 1:
        report.reverse()
        diffs = np.diff(report)

    if np.all(diffs > 0) and np.all(diffs <= 3):
        return True

    return False

def can_be_made_safe(report):
    diffs = np.diff(report)

    # if the report is in descending order, reverse it
    if sum(diffs < 0) > 1:
        report.reverse()
        diffs = np.diff(report)

    # If the report is already safe, return True
    if is_safe(report):
        return True
    
    # Find the level differences that violate the safety condition
    invalid = np.logical_or(diffs > 3, diffs <= 0)
    
    # If levels a and b resulted in a difference greater than 3 or less than 1, try removing level a
    # then try removing level b

    # Check if report is safe after removing level a
    exclude_index = np.where(invalid)[0][0]
    edited_report = report[:exclude_index] + report[exclude_index+1:]
    if is_safe(edited_report):
        return True

    # Check if report is safe after removing level b
    exclude_index = np.where(invalid)[0][0] + 1
    edited_report = report[:exclude_index] + report[exclude_index+1:]
    
    return is_safe(edited_report)
    

def parse_input(filename):
    lines = open(filename,'r').readlines()
    reports = [[int(level) for level in line.split()] for line in lines]
    return reports


if __name__ == '__main__':
    reports = parse_input('./input/day02a.txt')

    print(pt_1(reports))
    print(pt_2(reports))