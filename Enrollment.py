"""
FALL 2022
October 11, 2022:
CS 210, Professor: Michal Young
Week 3, Project 3
Author: Steven Sanchez-Jimenez
Project: Enrollment analysis
"""
import doctest
import csv


def read_csv_column(path: str, field: str) -> list[str]:
    """Read one column from a CSV file with headers into a list of strings.

    >>> read_csv_column("data/test_roster.csv", "Major")
    ['DSCI', 'CIS', 'BADM', 'BIC', 'CIS', 'GSS']
    """
    c = []
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for i in reader:
            c.append(i[field])
    return c


def counts(column: list[str]) -> dict[str, int]:
    """Returns a dict with counts of elements in column.

    >>> counts(["dog", "cat", "cat", "rabbit", "dog"])
    {'dog': 2, 'cat': 2, 'rabbit': 1}
    """
    c = {}
    for i in column:
        if i in c:
            c[i] += 1
        else:
            c[i] = 1
    return c


def read_csv_dict(path: str, key_field: str, value_field: str) -> dict[str, dict]:
    """Read a CSV with column headers into a dict with selected
    key and value fields.

    >>> read_csv_dict("data/test_programs.csv", key_field="Code", value_field="Program Name")
    {'ABAO': 'Applied Behavior Analysis', 'ACTG': 'Accounting', 'ADBR': 'Advertising and Brand Responsibility'}
    """
    l = {}
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for i in reader:
            key = i[key_field]
            val = i[value_field]
            l[key] = val
    return l


def items_v_k(d: dict) -> list[tuple]:
    """
    returns a list of tuples for i, v
    >>> items_v_k({'z': 2, 'a': 3, 'n': 4, 'r': 5})
    [(2, 'z'), (3, 'a'), (4, 'n'), (5, 'r')]
    """
    t = []
    for i, v in d.items():
        values = (v, i)
        t.append(values)
    return t



def main():
    doctest.testmod()
    majors = read_csv_column("data/roster_selected.csv", "Major")
    counts_by_major = counts(majors)
    program_names = read_csv_dict("data/programs.csv", "Code", "Program Name")
    # --- Next line replaces several statements
    by_count = items_v_k(counts_by_major)
    # ---
    by_count.sort(reverse=True)  # From largest to smallest
    for count, code in by_count:
        program = program_names[code]
        print(count, program)


if __name__ == "__main__":
    main()
