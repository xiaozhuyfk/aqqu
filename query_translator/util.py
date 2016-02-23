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

correct_set = [
    "when was oxygen discovered",
    "who designed the parthenon",
    "who was 8 mile directed by",
    "when was facebook launched",
    "who was titanic directed by",
    "who is the ceo of savealot",
    "what is europe 's area",
    "where was omarion born",
    "what is yahoo!'s slogan",
    "who created the far side",
    "when was walmart founded",
    "who designed pac-man",
    "who invented koolaid",
    "what causes syphilis",
    "who started starbucks",
    "what team does mike babcock coach",
    "what is the nutty professor rated",
    "what team does alan butcher coach",
    "what is the area of south america",
    "how many religions use the bible",
    "what was henry viii's royal line",
    "when was the sony nex-5 released",
    "how thick is the aletsch glacier",
    "who published the amazing spider-man",
    "what armed forces does thailand have",
    "who was charlie_s angels produced by",
    "when was the printing press invented",
    "what is the theme song of full house",
    "what product lines does ipod include",
    "how many rna codons does glycine have",
    "how many employees does nintendo have",
    "what spirits are produced in kentucky",
    "what is ashok malhotra's bowling pace"
]

unidentified = [
    "when was 300 released",
    "when was barbie launched",
    "who founded the red cross",
    "what causes prostate cancer",
    "what are the celtic languages",
    "how many people practice karate",
    "what is jerry seinfeld religion",
    "what is the population of europe",
    "what are some hotels in vancouver",
    "how many awards did big daddy win",
    "how many tv channels does nbc own",
    "what is the state flower of alaska",
    "what is the highest drop on stealth",
    "how many stores are in nittany mall",
    "what is currency code for uk currency",
    "how many seasons of seinfeld are there",
    "when did easy aces stop being produced",
    "how many countries is spanish spoken in",
    "what musicians have died of lung cancer",
    "how many people died in hurricane wilma",
    "what team does richard hamilton play for",
    "how many countries use the spanish peseta",
    "who produced sabotage by the beastie boys",
    "what bridges go over the san francisco bay",
    "what other titles does 13 going on 30 have",
    "what are the neighborhoods in new york city",
    "what animal does marscapone cheese come from",
    "what is the population estimated in the world",
    "how many monarchs are from the house of tutor",
    "what was the cost of building the magnum xl-200",
    "who was the editor in chief of die welt in 2000",
    "what is the lcd screen resolution of a nikon d80",
    "how many people ride the london underground daily",
    "how many runs does the thunder ridge ski area have",
    "who used to be quarterback for the green bay packers",
    "how many speeches have been given about world war ii",
    "when did john j. raskob own the empire state building",
    "what german athletes have participated in the olympics",
    "how many people played in the 2010 fifa world cup final",
    "on how many projects was james walker a design engineer",
    "what is the genre of the skeptics' guide to the universe",
    "what versions of mac os x is mozilla firefox compatible with",
    "when was the construction of new steubenville bridge finished",
    "what sport did scott anderson play in the 1992 summer olympics",
    "how many players are in the current roster of the new york mets",
    "how many wins did the philadelphia eagles have in the 2008 nfl season",
    "how many engineers worked on the design and construction of the plymouth breakwater"
]

test_file = "error.log"


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
