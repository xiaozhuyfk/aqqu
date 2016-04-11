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

pair_dir = "testresult/dump/"
query_dir = "testresult/query/"
bow_dir = "testresult/bow/"

internals = {}
vectors = {}

relations = [
    "discovery_technique",
    "languages",
    "name_of_collection_activity",
    "works_in_this_series"
]

def dumpindex(args):
    cmd = ['dumpindex', index]
    cmd.extend(args)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
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
    cmd = ["IndriRunQuery", query_file]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = p.communicate()
    return out[:-1]

def fetch_document_bow(internal):
    print "Fetching BOW for document %s" % internal
    bow = Counter()
    vector = dumpindex_get_document_vector(internal)
    lines = vector.split("\n")
    for line in lines[5:]:
        if (not line[0].isdigit()):
            continue
        tokens = line.split(" ")
        tf = int(tokens[1])
        term = tokens[2]
        if (term != "[OOV]" or tf != 0):
            bow[term] = tf
    return bow

def fetch_documents(query_file):
    trec = indri_run_query(query_file)
    if (trec == ""):
        return []

    documents = []
    for line in trec.split("\n"):
        tokens = line.split(" ")
        external = tokens[2]
        internal = dumpindex_get_internal_id(external)
        documents.append(internal)
    return documents

def fetch_query_bow(query_file):
    print "Fetching BOW for query " + query_file

    documents = fetch_documents(query_file)
    bow = Counter()
    for internal in documents:
        bow += fetch_document_bow(internal)
    return bow


def output_bow(bow, filename):
    path = bow_dir + filename + ".log"
    print "Writing BOW result to " + path

    writeFile(path, "", "w")
    result = sorted(bow.items(), key=operator.itemgetter(1))
    result.reverse()
    for (term, tf) in result:
        content = term + " " + str(tf) + "\n"
        writeFile(path, content, "a")


def fetch_relation_bow(relation_name):
    print "Fetching BOW for relation: " + relation_name

    query_file_path = pair_dir + relation_name + ".log"
    query_content = readFile(query_file_path)
    count = 1
    query = ""

    lines = query_content.split("\n")

    if (len(lines) > 150):
        lines = random.sample(lines, 150)

    for line in lines:
        if (line == ""):
            continue
        query += QUERY_FORMAT % (count, line)
        count += 1
        if (count > 150):
            break


    parameter = PARAM_FORMAT % query
    parameter_path = query_dir + relation_name + ".log"
    writeFile(parameter_path, parameter, "w")

    bow = fetch_query_bow(parameter_path)
    output_bow(bow, relation_name)

    return bow


def main(argv):
    #fetch_relation_bow(argv[0])
    writeFile(argv[0], argv[0], "w")

if __name__ == "__main__":
    #print output_bow(fetch_query_bow("../query/query_parameter.txt"), "dummy")
    #print indri_run_query("../query/query_parameter.txt")
    #print fetch_bow("../query/query_parameter.txt")
    #fetch_relation_bow("discovery_technique")
    #print fetch_documents("testresult/query/discovery_technique.log")
    main(sys.argv[1:])
