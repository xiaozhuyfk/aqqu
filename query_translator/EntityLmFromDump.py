'''
Created on Dec 3, 2015 2:19:48 PM
@author: cx

what I do:
    i fetch the text and made lm from freebase for target ids
what's my input:

what's my output:


'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/ExplicitSemanticEncoder')

from FreebaseDumpParser import FreebaseDumpParserC
from FreebaseDumpReader import FreebaseDumpReaderC
#from EseTextBase import EseLmC
import ConfigParser
#import json


lTargetField = ['Name','Desp','Alias']




def Process(DumpInName,TargetIdIn,OutPre):

    reader = FreebaseDumpReaderC()
    reader.open(DumpInName)
    Parser = FreebaseDumpParserC()
    global lTargetField

    sTargetId = set([item.split('\t')[0] for item in open(TargetIdIn).read().splitlines()])

    #lOut = [open(OutPre + '_' + field, 'w') for field in lTargetField]

    for cnt,lvCol in enumerate(reader):

        if 0 == (cnt % 1000):
            print 'read [%d] obj' %(cnt)

        ObjId = Parser.GetObjId(lvCol)
        if not ObjId in sTargetId:
            continue

        #lText = [Parser.GetField(lvCol, field) for field in lTargetField]
        #lLm = [EseLmC(text) for text in lText]

        #for out, lm in zip(lOut,lLm):
        #   print >>out, ObjId + '\t' + json.dumps(lm.hTerm)


    #for out in lOut:
    #    out.close()

    print 'finished'
    return


import sys

"""
ConfSec = 'EntityLmFromDump'
if 2 != len(sys.argv):
    print 'I simply fetch field texts for entity in Freebase'
    print '1 para, conf'
    print '[%s]' %(ConfSec)
    print 'DumpIn=\nTargetId=\nOut=\n'
    sys.exit()

conf = ConfigParser.SafeConfigParser()
conf.read(sys.argv[1])

DumpIn = conf.get(ConfSec,'DumpIn')
TargetId = conf.get(ConfSec,'TargetId')
OutPre = conf.get(ConfSec,'Out')

Process(DumpIn, TargetId, OutPre)
"""

edges = [
    "http://rdf.freebase.com/ns/astronomy.astronomical_discovery.discovery_technique"
]

def test():
    file = "/data/freebase-rdf-latest.gz"
    reader = FreebaseDumpReaderC()
    reader.open(file)
    Parser = FreebaseDumpParserC()


    d = {}
    for cnt,lvCol in enumerate(reader):

        if 0 == (cnt % 1000):
            print 'read [%d] obj' %(cnt)

        for (mid, wiki) in Parser.FetchPairWithEdge(lvCol, edges[0]):
            mid = Parser.DiscardPrefix(mid)
            if (mid[0] != "m"):
                continue
            d[mid] = wiki

    return d


test()



