"""
Helper functions for communication with Wiki API
"""

import requests
from xml.etree import ElementTree



class Wiki(object):
    def __init__(self):
        self.url = "https://en.wikipedia.org/w/api.php"

    def bag_of_words(self, entity):
        entity = entity.encode('utf-8')
        parameter = {
            'action' : "query",
            'titles' : entity,
            "format" : "json"
        }

        r = requests.get(self.url, params = parameter)
        print r.json()


Wiki().bag_of_words("obama")

