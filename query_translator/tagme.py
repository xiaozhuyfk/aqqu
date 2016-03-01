"""
Helper functions for communication with TagMe API
"""

import requests
from xml.etree import ElementTree

api_url = "http://tagme.di.unipi.it/api"
tag_url = "http://tagme.di.unipi.it/tag"
spot_url = "http://tagme.di.unipi.it/spot"
key = "CMU2016abhwqlao"

def parse_xml_response(text):
    pass

def identify_entities_legacy(text, lang = "en"):
    text = text.encode('utf-8')
    parameter = {'text' : text, 'key' : key, 'lang' : lang}
    r = requests.get(api_url, params = parameter)
    tree = ElementTree.fromstring(r.content)

def tagme_tagging(text,
                  lang = "en",
                  tweet = "false",
                  include_abstract = "false",
                  include_categories = "false",
                  include_all_spots = "false",
                  long_text = 0,
                  epsilon = 0.3):
    text = text.encode('utf-8')
    parameter = {
        'key' : key,
        'text' : text,
        'lang' : lang,
        'tweet' : tweet,
        'include_abstract' : include_abstract,
        'include_categories' : include_categories,
        'long_text' : long_text,
        'epsilon' : epsilon
    }

    r = requests.get(tag_url, params = parameter)
    for i in  r.json()["annotations"]:
        print i
    return 0

def tagme_spotting(text,
                   lang = "en",
                   tweet = "false"):
    text = text.encode('utf-8')
    parameter = {
        'key' : key,
        'text' : text,
        'lang' : lang,
        'tweet' : tweet
    }

    r = requests.get(spot_url, params = parameter)
    spots = r.json()["spots"]
    return [spot["spot"] for spot in spots]


#tagme_tagging("when was 300 released")
#tagme_tagging("how many countries is spanish spoken in")
print tagme_spotting("when was 300 released")