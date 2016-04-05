"""
Provides a console based translation interface.

Copyright 2015, University of Freiburg.

Elmar Haussmann <haussmann@cs.uni-freiburg.de>

"""

import collections
import logging
import globals
from query_translator.util import writeFile
from query_translator.FreebaseDumpParser import FreebaseDumpParserC
import requests
import subprocess


index = "/bos/tmp6/indexes/ClueWeb12_B13_index/"

def dumpindex(args):
    cmd = ['dumpindex', index]
    cmd.extend(args)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = p.communicate()
    return out


def dumpindex_get_internal_id(external):
    internal = dumpindex(['di', 'docno', external])
    print [internal]

def dumpindex_get_external_id(internal):
    external = dumpindex(['dn', internal])
    print [external]

def dumpindex_get_document_text(internal):
    pass

def fetch_documents(query):
    url = "http://boston.lti.cs.cmu.edu/Services/clueweb09_catb/lemur.cgi"
    headers = {
        'User-Agent' : "My User Agent 1.0",
        'From' : "hongyul@andrew.cmu.edu"
    }

    parameters = {
        "" : "4233518"
    }

    r = requests.get(url, params = parameters, headers = headers)
    print r.text

def clueweb_batch(query_file):
    url = "http://localhost:1111/lemur.cgi"

    parameters = {
        "query" : "harry potter"
    }

    r = requests.get(url, params = parameters)
    print r.text


if __name__ == "__main__":
    dumpindex_get_external_id("4233518")
