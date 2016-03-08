#!/usr/bin/env python


from KafNafParserPy import *

if __name__ == '__main__':
    filename = 'entity_example.naf'
    # We create the parser object
    my_parser = KafNafParser(filename)    
    
    # Iterate over the entities and print some information
    for entity_obj in my_parser.get_entities():
        print((entity_obj.get_id(), entity_obj.get_type()))
        for ext_ref in entity_obj.get_external_references():
            print(('\t',ext_ref.get_reference(), ext_ref.get_resource(), ext_ref.get_confidence()))
            
            
        
    # Add an external reference to the entity to the last entity (id e23)
    # First we create the external reference
    my_ext_ref = CexternalReference()
    my_ext_ref.set_reference('my_reference')
    my_ext_ref.set_resource('example')
    my_ext_ref.set_confidence('1.0')
    for entity_obj in my_parser.get_entities():
        if entity_obj.get_id() == 'e23':
            entity_obj.add_external_reference(my_ext_ref)
            
    # We print the entities again
    for entity_obj in my_parser.get_entities():
        print((entity_obj.get_id(), entity_obj.get_type()))
        for ext_ref in entity_obj.get_external_references():
            print(('\t',ext_ref.get_reference(), ext_ref.get_resource(), ext_ref.get_confidence()))
            
            
    #We can also add it directly to the parser object if we know the entity identifier
    my_ext_ref2 = CexternalReference()
    my_ext_ref2.set_reference('another_reference')
    my_ext_ref2.set_resource('example#2')
    my_ext_ref2.set_confidence('0.45')
    my_parser.add_external_reference_to_entity('e22', my_ext_ref2)
    
    # We dump the object to a file to store it with the new 2 entities
    my_parser.dump()  
    # This will dump in to the stdout you can also use my_parser.dump(fd) where fd is an open file
    # or my_parser.dump('my_name.naf') with a filename
                    
            
            
