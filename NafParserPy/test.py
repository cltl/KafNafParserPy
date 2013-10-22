#!/usr/bin/env python

from NafParserMod import NafParser
from text_data import wf
import sys

naf_obj = NafParser(sys.stdin)

for token in naf_obj.get_tokens():
    print token.id, token.sent, token.text
    
    
for term in naf_obj.get_terms():
    print term.id, term.lemma, term.span, term.pos
    
print naf_obj.get_token('w17')
print naf_obj.get_term('t17')