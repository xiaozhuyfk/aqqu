"""
Provides a console based translation interface.

Copyright 2015, University of Freiburg.

Elmar Haussmann <haussmann@cs.uni-freiburg.de>

"""

import subprocess
import operator
import sys
from query_translator.util import readFile, writeFile
from collections import Counter
import random


index = "/bos/tmp6/indexes/ClueWeb12_B13_index/"

PARAM_FORMAT = '''
<parameters>
    <index>/bos/tmp6/indexes/ClueWeb12_B13_index</index>
    <count>10</count>
    <trecFormat>true</trecFormat>
    %s
</parameters>
'''

QUERY_FORMAT = '''
    <query>
        <type>indri</type>
        <number>%d</number>
        <text>%s</text>
    </query>
'''

DUMP_QUERY_FORMAT = "#uw20(#1(%s) #1(%s))"

pair_dir = "/home/hongyul/aqqu/testresult/dumpaqqu/"
query_dir = "/home/hongyul/aqqu/testresult/queryaqqu/"
bow_dir = "/home/hongyul/aqqu/testresult/bowaqqu/"
long_bow_dir = "/home/hongyul/aqqu/testresult/bowlong/"
short_bow_dir = "/home/hongyul/aqqu/testresult/bowshort/"

internals = {}
vectors = {}

relations = [
    "discovery_technique",
    "languages",
    "name_of_collection_activity",
    "works_in_this_series"
]

fail_chars = [
    "'",
    '"',
    "&",
    "!",
    "@",
    "$",
    "%",
    "^",
    "*",
    "_",
    "+",
    "=",
    "|",
    "\\",
    "?",
    "/",
    "~",
    "`",
    "[",
    "]",
    "{",
    "}",
    ",",
    ".",
    ";",
    ":",
    "#"
]

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

def dumpindex(args):
    cmd = ['../bin/dumpindex', index]
    cmd.extend(args)
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    out, err = p.communicate()
    return out

def dumpindex_get_internal_id(external):
    if (external in internals):
        internal = interals[external]
    else:
        internal = dumpindex(['di', 'docno', external])[:-1]
    return internal

def dumpindex_get_external_id(internal):
    external = dumpindex(['dn', internal])[:-1]
    return external

def dumpindex_get_document_text(internal):
    text = dumpindex(['dt', internal])[:-1]
    return text

def dumpindex_get_document_data(internal):
    data = dumpindex(['dd', internal])[:-1]
    return data

def dumpindex_get_document_vector(internal):
    if (internal in vectors):
        vector = vectors[internal]
    else:
        vector = dumpindex(['dv', internal])[:-1]
    return vector

def indri_run_query(query_file):
    print "IndriRunQuery", query_file
    cmd = ["../bin/IndriRunQuery", query_file]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    out, err = p.communicate()
    return out[:-1]

def fetch_document_bow(internal, e1, e2):
    print "Fetching BOW for document %s with query (%s, %s)" % (internal, e1, e2)
    bow_long = Counter()
    bow_short = Counter()
    vector = dumpindex_get_document_vector(internal)
    lines = vector.split("\n")
    terms = []
    for line in lines[5:]:
        if (not line[0].isdigit()):
            continue
        tokens = line.split(" ")
        term = tokens[2]
        terms.append(term)

    shorts = []
    longs = []
    entities1 = [kstem(stem) for stem in e1.split(" ")]
    entities2 = [kstem(stem) for stem in e2.split(" ")]

    i = 0
    while i < len(terms):
        term = terms[i]
        if (term == entities1[0]) and (entities2[0] in terms[i: i+21]):
            index = terms[i: i+21].index(entities2[0])
            short_sentence = terms[i: i+index+1]
            long_sentence = terms[max(0, i-5): i+index + 6]
            shorts.append(short_sentence)
            longs.append(long_sentence)
            i += index
        elif (term == entities2[0]) and (entities1[0] in terms[i:i+21]):
            index = terms[i:i+21].index(entities1[0])
            short_sentence = terms[i:i+index+1]
            long_sentence = terms[max(0, i-5): i+index+6]
            shorts.append(short_sentence)
            longs.append(long_sentence)
            i += index
        i += 1

    for i in xrange(len(shorts)):
        l = longs[i]
        s = shorts[i]
        for term in l:
            if (term == "[OOV]") or (term in entities1) or (term in entities2):
                continue
            bow_long[term] += 1
        for term in s:
            if (term == "[OOV]") or (term in entities1) or (term in entities2):
                continue
            bow_short[term] += 1

    return (bow_long, bow_short)

def fetch_documents(query_file):
    trec = indri_run_query(query_file)
    if (trec == ""):
        return []

    documents = []
    for line in trec.split("\n"):
        if line == "":
            continue
        if not line[0].isdigit():
            print "Fail to parse line: %s" % line
            continue

        tokens = line.split(" ")
        qid = int(tokens[0])
        external = tokens[2]
        internal = dumpindex_get_internal_id(external)
        documents.append((qid, internal))
    return documents

def fetch_query_bow(query_file, queries):
    print "Fetching BOW for query " + query_file

    documents = fetch_documents(query_file)
    bow_long = Counter()
    bow_short = Counter()
    for qid, internal in documents:
        pair = queries[qid-1]
        result = fetch_document_bow(internal, pair[0], pair[1])
        bow_long += result[0]
        bow_short += result[1]
    return (bow_long, bow_short)


def output_bow(bow, path):
    print "Writing BOW result to " + path

    writeFile(path, "", "w")
    result = sorted(bow.items(), key=operator.itemgetter(1))
    result.reverse()
    for (term, tf) in result:
        content = term + " " + str(tf) + "\n"
        writeFile(path, content, "a")


import re

def process_query(query):
    p = r'#uw20\(#1\((.*)\) #1\((.*)\)\)'
    match = re.match(p, query)
    return (match.group(1).strip(), match.group(2).strip())

def fetch_relation_bow(relation_name):
    print "Fetching BOW for relation: " + relation_name

    query_file_path = pair_dir + relation_name + ".log"
    query_content = readFile(query_file_path)
    count = 1
    query = ""

    lines = query_content.split("\n")
    queries = []
    if (len(lines) > 100):
        lines = random.sample(lines, 100)

    for line in lines:
        if (line == ""):
            continue
        #for ch in fail_chars:
        #    line = line.replace(ch, "")
        #query += QUERY_FORMAT % (count, line)

        pair = process_query(line)
        queries.append(pair)
        e1, e2 = pair

        for ch in fail_chars:
            e1 = e1.replace(ch, "")
            e2 = e2.replace(ch, "")

        dump_query = DUMP_QUERY_FORMAT % (e1, e2)
        query += QUERY_FORMAT % (count, dump_query)


        count += 1
        if (count > 100):
            break


    parameter = PARAM_FORMAT % query
    parameter_path = query_dir + relation_name + ".log"
    writeFile(parameter_path, parameter, "w")

    bow_long, bow_short = fetch_query_bow(parameter_path, queries)

    long_filename = long_bow_dir + relation_name + ".log"
    short_filename = short_bow_dir + relation_name + ".log"
    output_bow(bow_long, long_filename)
    output_bow(bow_short, short_filename)


import os

def main(argv):
    index = int(argv[0])
    files = os.listdir("/home/hongyul/aqqu/testresult/dumpaqqu")
    size = len(files) / 16

    if (size == 0):
        size = 1

    if (index == 15):
        files = files[index*size:]
    else:
        files = files[index*size:(index+1)*size]

    for filename in files:
        if (not filename.endswith(".log")):
            continue
        relation_name = filename[:-4]
        fetch_relation_bow(relation_name)

if __name__ == "__main__":
    #print output_bow(fetch_query_bow("../query/query_parameter.txt"), "dummy")
    #print indri_run_query("../query/query_parameter.txt")
    #print fetch_bow("../query/query_parameter.txt")
    #fetch_relation_bow("discovery_technique")
    #print fetch_documents("testresult/query/discovery_technique.log")
    main(sys.argv[1:])
    #fetch_relation_bow("base_barbie_barbie_theme_dolls_with_this_theme")
    #print kstem("imaging")
    #fetch_document_bow("51953232", "HD 209458 b", "Transit")
