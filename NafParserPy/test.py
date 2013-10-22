#!/usr/bin/env python

from NafParserMod import *
import sys

naf_obj = NafParser(sys.stdin)

for token in naf_obj.get_tokens():
    print token.get_id(), token.get_sent(), token.get_text()
    
    
for term in naf_obj.get_terms():
    print term.get_id(),term.get_lemma()
    
print naf_obj.get_token('w17').get_id()
print naf_obj.get_term('t17').get_id()

ext_ref = externalReference()
ext_ref.set_resource('my_res')
ext_ref.set_reference('my_ref')
ext_ref.set_confidence('my_conf')

naf_obj.add_external_reference('t17',ext_ref)

#naf_obj.dump()