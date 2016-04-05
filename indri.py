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


def fetch_documents(query):
    url = "http://boston.lti.cs.cmu.edu/Services/clueweb09_catb/lemur.cgi"
    headers = {
        'User-Agent' : "My User Agent 1.0",
        'From' : "hongyul@andrew.cmu.edu"
    }

    parameters = {
        "getdocext" : "clueweb12-1313wb-10-13464"
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
    fetch_documents("query.txt")
