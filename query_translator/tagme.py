"""
Helper functions for communication with TagMe API
"""

import requests
from xml.etree import ElementTree

api_url = "http://tagme.di.unipi.it/api"
tag_url = "http://tagme.di.unipi.it/tag"
key = ""

def parse_xml_response(text):
    pass

def identify_entities_legacy(text, lang = "en"):
    text = text.encode('utf-8')
    parameter = {'text' : text, 'key' : key, 'lang' : lang}
    r = requests.get(api_url, params = parameter)
    tree = ElementTree.fromstring(r.content)

def identify_entities(text,
                      lang = "en",
                      tweet = "false",
                      include_abstract = "false",
                      include_categories = "false",
                      include_all_spots = "false",
                      long_text = 0,
                      epsilon = 0.3):
    text = text.encode('utf-8')
    parameter = {
        'text' : text,
        'lang' : lang,
        'tweet' : tweet,
        'include_abstract' : include_abstract,
        'include_categories' : include_categories,
        'long_text' : long_text,
        'epsilon' : epsilon
    }

    r = requests.get(tag_url, params = parameter)
    json = r.json()
    return [(e, )]


print identify_entities_legacy("what the fuck is this?")
print identify_entities("wo le ge qu")