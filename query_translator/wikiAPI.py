"""
Helper functions for communication with Wiki API
"""

import requests
import json
import nltk
import urllib2
from bs4 import BeautifulSoup
import string


class Wiki(object):
    def __init__(self):
        self.url = "https://en.wikipedia.org/w/api.php"
        self.mql = "https://www.googleapis.com/freebase/v1/mqlread"
        self.wiki = "https://en.wikipedia.org/wiki/index.html"

    def bag_of_words(self, entity):
        entity = entity.encode('utf-8')
        id = self.get_wiki_id(entity)

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
            if (punc):
                continue
            normal.append(stem)

        bow = {}
        total = len(normal)
        for stem in normal:
            if (stem in bow):
                bow[stem] += 1
            else:
                bow[stem] = 1
        return (bow, total)




    def mqlRead(self, entity):
        query = {
            "mid" : entity,
            "key" : {
                "namespace" : "/wikipedia/en_id",
                "value" : None
            }
        }

        dump = json.dumps(query)

        parameter = {
            'query' : dump
        }

        r = requests.get(self.mql, params = parameter)
        return r.json()


    def get_wiki_id(self, entity):
        bag = self.mqlRead(entity)
        return bag["result"]["key"]["value"]


    def get_wiki_page(self, entity):
        entity = entity.encode('utf-8')
        id = self.get_wiki_id(entity)

        parameter = {
            "action" : "query",
            "format" : "json",
            "pageids" : id,
            "prop" : "revisions",
            "rvprop" : "content"
        }
        r = requests.get(self.url, params = parameter)
        return r.json()["query"]["pages"][str(id)]["revisions"][0]["*"]



Wiki().bag_of_words("/m/011jq0qx")

