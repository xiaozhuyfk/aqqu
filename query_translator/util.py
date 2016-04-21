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

wq_index = [
    79,
    103,
    112,
    149,
    151,
    157,
    221,
    226,
    238,
    257,
    260,
    260,
    263,
    268,
    273,
    280,
    310,
    318,
    328,
    332,
    333,
    336,
    352,
    361,
    363,
    390,
    391,
    392,
    415,
    457,
    458,
    471,
    492,
    497,
    512,
    518,
    536,
    552,
    566,
    577,
    579,
    588,
    607,
    615,
    640,
    646,
    688,
    719,
    724,
    733,
    770,
    776,
    807,
    809,
    820,
    830,
    846,
    859,
    860,
    878,
]

wq_test = [
    "who plays billy elliot?",
    "when do world war ii end?",
    "where is denmark situated?",
    "what team is raul ibanez on?",
    "what was dr seuss real name?",
    "who did shaq first play for?",
    "who won the 2000 fa cup final?",
    "what does british colony mean?",
    "where did joseph's family live?",
    "where is chesapeake bay bridge?",
    "where does houston dynamo play?",
    "where does houston dynamo play?",
    "what did james chadwick invent?",
    "where was the assyrian homeland?",
    "when does jewish new year start?",
    "what to do in rome october 2012?",
    "what team is reggie bush on 2011?",
    "who won the battle of gettysburg?",
    "who did the voice for lola bunny?",
    "what is spoken in czech republic?",
    "when was father chris riley born?",
    "what animal represents california?",
    "who did richard nixon run against?",
    "when did florida marlins join mlb?",
    "where do ireland play rugby union?",
    "what countries does england border?",
    "where did kevin love go to college?",
    "what countries are in the uk yahoo?",
    "when was michael jordan at his best?",
    "who does michael keaton play in cars?",
    "who does brian dawkins play for 2011?",
    "who are the colorado representatives?",
    "what age did william penn get married?",
    "what language did they speak in ghana?",
    "what are serena williams achievements?",
    "what kind of currency does mexico use?",
    "what is monta ellis career high points?",
    "where does the zambezi river originate?",
    "what city and state is yale located in?",
    "what language do people speak in brazil?",
    "what year did adam morrison get drafted?",
    "which country was justin bieber born in?",
    "what is the name of airport in new york?",
    "what country did benito mussolini govern?",
    "what is the percentage of youth in uganda?",
    "what did napoleon bonaparte do as emperor?",
    "what did dmitri mendeleev discover in 1869?",
    "who is meredith gray married to in real life?",
    "where did the battle of passchendaele happen?",
    "who did ricky martin started his career with?",
    "who plays caesar flickerman in the hunger games?",
    "what percent of people are overweight in the uk?",
    "when did president theodore roosevelt take office?",
    "what year was the first miss america pageant held?",
    "what does the sun in the philippine flag represent?",
    "what countries require travel visas for us citizens?",
    "what countries have english as their official language?",
    "what role did alexander hamilton play in the constitution?",
    "what are the 7 countries that are part of central america?",
    "what did anton van leeuwenhoek contribute to our knowledge of cells?"
]

test_file = "testresult/feature_test.log"

rank_error = [
    "who is the present newscaster on cbs evening news",
    "what year was the album decade released",
    "when was the construction of new steubenville bridge finished",
    "what is the lcd screen resolution of a nikon d80"
]

rank_pos = [5, 1, 1, 1]

rm_error = [
    "who produced sabotage by the beastie boys",
    "what other titles does 13 going on 30 have"
]

er_error = [
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
    "when was 300 released",
    "who founded the red cross",
    "how many awards did big daddy win",
    "what is the state flower of alaska",
    "what is the highest drop on stealth",
    "what is currency code for uk currency",
    "how many countries is spanish spoken in",
    "what musicians have died of lung cancer",
    "how many monarchs are from the house of tutor",
    "who was the editor in chief of die welt in 2000",
    "what sport did scott anderson play in the 1992 summer olympics"
]


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



import pysftp

def sftp_get(remote_path, local_path):
    with pysftp.Connection('boston-cluster.lti.cs.cmu.edu',
                           username='hongyul',
                           password='Wdsfzyd106@') as sftp:
        sftp.get(remotepath = remote_path, localpath = local_path)

def sftp_get_d(remote_path, local_path):
    with pysftp.Connection('boston-cluster.lti.cs.cmu.edu',
                           username='hongyul',
                           password='Wdsfzyd106@') as sftp:
        sftp.get_d(remote_path, local_path)

def sftp_get_r(remote_path, local_path):
    with pysftp.Connection('boston-cluster.lti.cs.cmu.edu',
                           username='hongyul',
                           password='Wdsfzyd106@') as sftp:
        sftp.get_r(remote_path, local_path)

def sftp_put(local_path, remote_path):
    with pysftp.Connection('boston-cluster.lti.cs.cmu.edu',
                           username='hongyul',
                           password='Wdsfzyd106@') as sftp:
        sftp.put(local_path, remote_path)

def sftp_put_d(local_path, remote_path):
    with pysftp.Connection('boston-cluster.lti.cs.cmu.edu',
                           username='hongyul',
                           password='Wdsfzyd106@') as sftp:
        sftp.put_d(local_path, remote_path)

def sftp_put_r(local_path, remote_path):
    with pysftp.Connection('boston-cluster.lti.cs.cmu.edu',
                           username='hongyul',
                           password='Wdsfzyd106@') as sftp:
        sftp.put_r(local_path, remote_path)

def sftp_execute(command):
    with pysftp.Connection('boston-cluster.lti.cs.cmu.edu',
                           username='hongyul',
                           password='Wdsfzyd106@') as sftp:
        sftp.execute("cd aqqu; " + command)

def sftp_listdir(remote_path):
    with pysftp.Connection('boston-cluster.lti.cs.cmu.edu',
                           username='hongyul',
                           password='Wdsfzyd106@') as sftp:
        return sftp.listdir(remote_path)

import os

def get_bows():
    path = "/home/hongyul/bow.txt"
    for filename in os.listdir("/home/hongyul/aqqu/testresult/bow"):
        content = filename + "\n"
        writeFile(path, content, "a")

def get_dumps():
    path = "/data/dump.txt"
    for filename in os.listdir("/data/dump"):
        content = filename + "\n"
        writeFile(path, content, "a")

def test():
    d = set()
    for line in readFile("../testresult/relation_fail.log").split("\n"):
        if line == "":
            continue
        if line not in d:
            d.add(line)
    print d
    print len(d)

import subprocess
def kstem(stem):
    cmd = ['java',
           '-classpath',
           'kstem.jar',
           'org.lemurproject.kstem.KrovetzStemmer',
           '-w',
           stem]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    out, err = p.communicate()
    return out.split(" ")[1][:-1]


if __name__ == '__main__':
    #print edit_distance('this is a house', 'this is not a house')
    #sftp_get("/home/hongyul/Python-2.7.11.tgz", "/Users/Hongyu1/Desktop/Python.tgz")
    #sftp_get_r("/home/hongyul/query", "/Users/Hongyu1/Desktop")
    #sftp_put("/Users/Hongyu1/Desktop/Python.tgz", "/home/hongyul/haha.tgz")
    #print sftp_execute("../init_env/bin/python indri.py name_of_collection_activity")
    #print sftp_listdir("/home/hongyul/")
    #get_filenames()
    #sftp_put("/data/dump.tar.gz", "/home/hongyul/aqqu/testresult/dump")
    test()
