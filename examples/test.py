#!/usr/bin/env python
from __future__ import absolute_import, print_function

from KafNafParserPy.KafNafParserMod import *
import sys

obj = KafNafParser('kaf_example.xml')

print('I) The object type is: ',obj.get_type())
obj.to_naf()
print('II) The object type is: ',obj.get_type())
obj.to_kaf()
print('III) The object type is: ',obj.get_type())
obj.dump('my_file.kaf')
print('object saved in my_file.kaf as ',obj.get_type())

sys.exit(0)


print('ERA:',obj.type, file=sys.stderr)
obj.to_naf()
print('ahora es',obj.type, file=sys.stderr)
obj.to_kaf()
print('finalmente es',obj.type, file=sys.stderr)
obj.dump()
sys.exit(0)



#for token in naf_obj.get_tokens():
#    print token.get_id(), token.get_sent(), token.get_text()
    
 
   
for term in naf_obj.get_terms():
    print(term.get_id(),term.get_lemma())
    
#print naf_obj.get_token('w17').get_id()
#print naf_obj.get_term('t17').get_id()


'''
ext_ref = CexternalReference()
ext_ref.set_resource('my_res')
ext_ref.set_reference('my_ref')
ext_ref.set_confidence('my_conf')

naf_obj.add_external_reference('t17',ext_ref)

naf_obj.dump()
'''