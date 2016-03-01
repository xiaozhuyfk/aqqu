"""
Helper functions for communication with TagMe API
"""

import requests
from xml.etree import ElementTree


class TagMe(object):
    def __init__(self):
        self.api_url = "http://tagme.di.unipi.it/api"
        self.tag_url = "http://tagme.di.unipi.it/tag"
        self.spot_url = "http://tagme.di.unipi.it/spot"
        self.key = "CMU2016abhwqlao"

    def identify_entities_legacy(self, text, lang = "en"):
        text = text.encode('utf-8')
        parameter = {'text' : text, 'key' : self.key, 'lang' : lang}
        r = requests.get(api_url, params = parameter)
        tree = ElementTree.fromstring(r.content)

    def tagme_tagging(self,
                      text,
                      lang = "en",
                      tweet = "false",
                      include_abstract = "false",
                      include_categories = "false",
                      include_all_spots = "false",
                      long_text = 0,
                      epsilon = 0.3):
        text = text.encode('utf-8')
        parameter = {
            'key' : self.key,
            'text' : text,
            'lang' : lang,
            'tweet' : tweet,
            'include_abstract' : include_abstract,
            'include_categories' : include_categories,
            'long_text' : long_text,
            'epsilon' : epsilon
        }

        r = requests.get(self.tag_url, params = parameter)
        for i in  r.json()["annotations"]:
            print i
        return 0

    def tagme_spotting(self,
                       text,
                       lang = "en",
                       tweet = "false"):
        text = text.encode('utf-8')
        head = [0]
        tail = []
        for token in text.split(" "):
            tail.append(head[-1] + len(token))
            head.append(head[-1] + len(token) + 1)

        parameter = {
            'key' : self.key,
            'text' : text,
            'lang' : lang,
            'tweet' : tweet
        }

        r = requests.get(self.spot_url, params = parameter)
        spots = r.json()["spots"]
        return [(spot["spot"], head.index(spot["start"], tail.index(spot["end"]))) for spot in spots]


#tagme_tagging("when was 300 released")
#tagme_tagging("how many countries is spanish spoken in")
#print TagMe().tagme_spotting("when was 300 released")