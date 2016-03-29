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

from EseUtils.FreebaseDumpParser import FreebaseDumpParserC
from EseUtils.FreebaseDumpReader import FreebaseDumpReaderC
from EseUtils.EseTextBase import EseLmC
import ConfigParser
import json


lTargetField = ['Name','Desp','Alias']


        

def Process(DumpInName,TargetIdIn,OutPre):
    
    reader = FreebaseDumpReaderC()
    reader.open(DumpInName)
    Parser = FreebaseDumpParserC()
    global lTargetField
    
    sTargetId = set([item.split('\t')[0] for item in open(TargetIdIn).read().splitlines()])
    
    lOut = [open(OutPre + '_' + field, 'w') for field in lTargetField]
    
    for cnt,lvCol in enumerate(reader):
        
        if 0 == (cnt % 1000):
            print 'read [%d] obj' %(cnt)
        
        ObjId = Parser.GetObjId(lvCol)
        if not ObjId in sTargetId:
            continue
        
        lText = [Parser.GetField(lvCol, field) for field in lTargetField]
        lLm = [EseLmC(text) for text in lText]
        
        for out, lm in zip(lOut,lLm):
            print >>out, ObjId + '\t' + json.dumps(lm.hTerm)
            
    
    for out in lOut:
        out.close()
        
    print 'finished'
    return


import sys

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
            
        
        
        
        