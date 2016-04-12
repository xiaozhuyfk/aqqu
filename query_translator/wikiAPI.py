"""
Helper functions for communication with Wiki API
"""

import json
import string
import urllib2

import nltk
import requests
from bs4 import BeautifulSoup
from collections import Counter


class Wiki(object):
    def __init__(self):
        self.url = "https://en.wikipedia.org/w/api.php"
        self.mql = "https://www.googleapis.com/freebase/v1/mqlread"
        self.wiki = "https://en.wikipedia.org/wiki/index.html"
        self.stopwords = [
            "a",
            "about",
            "above",
            "after",
            "again",
            "against",
            "all",
            "am",
            "an",
            "and",
            "any",
            "are",
            "aren't",
            "as",
            "at",
            "be",
            "because",
            "been",
            "before",
            "being",
            "below",
            "between",
            "both",
            "but",
            "by",
            "can't",
            "cannot",
            "could",
            "couldn't",
            "did",
            "didn't",
            "do",
            "does",
            "doesn't",
            "doing",
            "don't",
            "down",
            "during",
            "each",
            "few",
            "for",
            "from",
            "further",
            "had",
            "hadn't",
            "has",
            "hasn't",
            "have",
            "haven't",
            "having",
            "he",
            "he'd",
            "he'll",
            "he's",
            "her",
            "here",
            "here's",
            "hers",
            "herself",
            "him",
            "himself",
            "his",
            "how",
            "how's",
            "i",
            "i'd",
            "i'll",
            "i'm",
            "i've",
            "if",
            "in",
            "into",
            "is",
            "isn't",
            "it",
            "it's",
            "its",
            "itself",
            "let's",
            "me",
            "more",
            "most",
            "mustn't",
            "my",
            "myself",
            "no",
            "nor",
            "not",
            "of",
            "off",
            "on",
            "once",
            "only",
            "or",
            "other",
            "ought",
            "our",
            "ours",
            "the",
            "to",
            "s",
            "that",
            "this"
        ]

    def bag_of_words(self, entity):
        entity = entity.encode('utf-8')
        id = self.get_wiki_id(entity)
        if (id == None):
            return (None, None)

        url = self.wiki + "?" + "curid=" + id
        html = urllib2.urlopen(url).read().decode('utf8')
        raw = BeautifulSoup(html, "html.parser").get_text()
        tokens = nltk.word_tokenize(raw)
        text = nltk.Text(tokens)
        words = [w.lower() for w in text]
        lancaster = nltk.LancasterStemmer()
        stems = [lancaster.stem(t) for t in words]

        normal = []
        for stem in stems:
            stem = stem.encode('utf-8')
            punc = True
            for s in stem:
                if (s not in string.punctuation and s not in string.whitespace):
                    punc = False
                    break
            if (punc or stem in self.stopwords):
                continue
            normal.append(stem)

        bow = Counter()
        total = len(normal)
        for stem in normal:
            if (stem in bow):
                bow[stem] += 1
            else:
                bow[stem] = 1
        return (bow, total)

    def mqlRead(self, entity):
        query = {
            "mid": entity,
            "key": {
                "namespace": "/wikipedia/en_id",
                "value": None
            }
        }

        dump = json.dumps(query)

        parameter = {
            'query': dump
        }

        r = requests.get(self.mql, params = parameter)
        return r.json()

    def get_wiki_id(self, entity):
        bag = self.mqlRead(entity)
        try:
            id = bag["result"]["key"]["value"]
        except:
            return None

        return id


    def get_wiki_page(self, entity):
        entity = entity.encode('utf-8')
        id = self.get_wiki_id(entity)

        parameter = {
            "action": "query",
            "format": "json",
            "pageids": id,
            "prop": "revisions",
            "rvprop": "content"
        }
        r = requests.get(self.url, params = parameter)
        return r.json()["query"]["pages"][str(id)]["revisions"][0]["*"]


print Wiki().bag_of_words("/m/0c3qy")
