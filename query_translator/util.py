"""
A few simple utitlity functions.

Copyright 2015, University of Freiburg.

Elmar Haussmann <haussmann@cs.uni-freiburg.de>

"""
from itertools import tee, izip

test_set = ["what movie did danny devito win an award for in 1981",
            "when did japan end as a musical group",
            "what sort of weave is used to make tweed",
            "what bicycle models does raleigh manufacture",
            "how many writing systems are used in japanese",
            "what characters were on the cover of batman #1",
            "how many episodes of taylor made piano were there",
            "who is the present newscaster on cbs evening news",
            "did the big bang exhibit at the science museum cost money",
            "in what season of stargate sg-1 is the episode show and tell",
            "how many beers come a can",
            "what are the christian holidays",
            "what are the texts of taoism",
            "in 1982 who were the primetieme emmy award for comedy series nominees",
            "what year was the album decade released",
            "how many countries are in south america",
            "what area did the meiji constitution govern",
            "what is the collection of postcards called",
            "how was pluto discovered",
            "how many people practice buddhism",
            "how many students are there at the university of iceland",
            "how many libretti did wagner write",
            "how many other names is ron glass known by",
            "what was the american past about",
            "who completed mozart_s requiem",
            "when gatorade was first developed",
            "what are the theme areas at disneyland",
            "how many films has tim burton produced",
            "how many politicians have served in the us navy",
            "what are some object-oriented programming languages",
            "what are the books in the chronicles of narnia series",
            "what decision did manny pacquiao vs. timothy bradley end with"]


def edit_distance(s1, s2, compare_lower = True):
    s1 = s1.lower()
    s2 = s2.lower()
    if len(s1) < len(s2):
        return edit_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def triplewise(iterable):
    a, b, c = tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return izip(a, b, c)


# Read a file
# filename is the path of the file, string type
# returns the content as a string
def readFile(filename, mode = "rt"):
    # rt stands for "read text"
    fin = contents = None
    try:
        fin = open(filename, mode)
        contents = fin.read()
    finally:
        if (fin != None): fin.close()
    return contents


# Write 'contents' to the file
# 'filename' is the path of the file, string type
# 'contents' is of string type
# returns True if the content has been written successfully
def writeFile(filename, contents, mode = "wt"):
    # wt stands for "write text"
    fout = None
    try:
        fout = open(filename, mode)
        fout.write(contents)
    finally:
        if (fout != None): fout.close()
    return True


if __name__ == '__main__':
    print edit_distance('this is a house', 'this is not a house')
