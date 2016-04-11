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
from util import writeFile


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
    #"http://rdf.freebase.com/ns/astronomy.astronomical_discovery.discovery_technique",
    "<http://rdf.freebase.com/key/wikipedia.en_id>"
]

result_file = "../testresult/dump/pairs"

def test():
    file = "/data/freebase-rdf-latest.gz"
    reader = FreebaseDumpReaderC()
    reader.open(file)
    Parser = FreebaseDumpParserC()


    d = {}
    for cnt,lvCol in enumerate(reader):

        if 0 == (cnt % 1000):
            print 'read [%d] obj' %(cnt)

        for vCol in lvCol:
            e1 = vCol[0]
            e1 = Parser.DiscardPrefix(e1).encode('utf-8')
            r = Parser.DiscardPrefix(vCol[1]).encode('utf-8')
            e2 = Parser.DiscardPrefix(vCol[2]).encode('utf-8')
            if e1.startswith("m."):
                print r, e2

    '''
        for edge in edges:
            edge_name = edge.split(".")[-1]
            target_file = result_file + "-" + edge_name + ".log"
            for (e1, e2) in Parser.FetchPairWithEdge(lvCol, edge):
                print e1
                e1 = Parser.DiscardPrefix(e1)
                e2 = Parser.DiscardPrefix(e2)
                content = e1 + "\t" + e2
                print edge_name, e1, e2
                writeFile(target_file, content, "a")
                '''

    return d


test()



