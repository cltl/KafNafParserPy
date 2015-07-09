"""
Parser for the entity layer in KAF/NAF
"""

## Modified for KAF NAF adaptation
from lxml import etree
from lxml.objectify import dump
from references_data import *
from external_references_data import *
    
    
class Centity:
    """
    This class encapsulates the entity element in KAF/NAF
    """
    def __init__(self,node=None,type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.type = type
        if node is None:
            self.node = etree.Element('entity')
        else:
            self.node = node

    def set_comment(self,c):
        """
        Sets the comment for the element
        @type c: string
        @param c: comment for the element
        """
        c = c.replace('--','- -')
        self.node.insert(0,etree.Comment(c))
        
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
                    
    def get_id(self):
        """
        Returns the identifier of the element
        @rtype: string
        @return: the identifier of the entity
        """
        if self.type == 'NAF':
            return self.node.get('id')
        elif self.type == 'KAF':
            return self.node.get('eid')

    def set_id(self,i):
        """
        Sets the identifier for the entity
        @type i: string
        @param i: entity identifier
        """
        if self.type == 'NAF':
            self.node.set('id',i)
        elif self.type == 'KAF':
            self.node.set('eid',i)
                
    def get_type(self):
        """
        Returns the type of the entity
        @rtype: string
        @return: the type of the entity
        """
        return self.node.get('type')
    
    def set_type(self,t):
        self.node.set('type',t)
        
    def get_references(self):
        """
        Returns the references of the entity
        @rtype: L{Creferences}
        @return: list of references (iterator)
        """
        for ref_node in self.node.findall('references'):
            yield Creferences(ref_node)

    def add_reference(self,ref):
        """
        Adds a reference to the layer
        @type ref: L{Creferences}
        @param ref: a reference object  
        """
        self.node.append(ref.get_node())
                    
    def add_external_reference(self,ext_ref):
        """
        Adds an external reference to the entity
        @param ext_ref: the external reference object
        @type ext_ref: L{CexternalReference}
        """
        #check if the externalreferences sublayer exist for the role, and create it in case
        node_ext_refs = self.node.find('externalReferences')
        ext_refs = None
        if node_ext_refs == None:
            ext_refs = CexternalReferences()
            self.node.append(ext_refs.get_node())
        else:
            ext_refs = CexternalReferences(node_ext_refs)
        
        ext_refs.add_external_reference(ext_ref)  
        
        
    def get_external_references(self):
        """
        Returns the external references of the element
        @rtype: L{CexternalReference}
        @return: the external references (iterator)
        """
        node = self.node.find('externalReferences')
        if node is not None:
            ext_refs = CexternalReferences(node)
            for ext_ref in ext_refs:
                yield ext_ref    
    
        def get_source(self):
        """
        Returns the source of the entity
        @rtype: string
        @return: the source of the entity
        """
        return self.node.get('source')
    
    def set_source(self,t):
        self.node.set('source',t)
    
class Centities:
    """
    This class encapsulates the entity layer in KAF/NAF
    """
    def __init__(self,node=None,type='NAF'):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        """
        self.type = type
        self.map_entity_id_to_node = {}
        if node is None:
            self.node = etree.Element('entities')
        else:
            self.node = node
            for entity_obj in self:
                self.map_entity_id_to_node[entity_obj.get_id()] = entity_obj.get_node()
    
    def add_entity(self,ent):
        self.node.append(ent.get_node())
                                        
            
        
    def add_external_reference_to_entity(self,entity_id,ext_ref):
        """
        Adds an external reference to a entity specified by the entity identifier
        @param entity_id: the entity identifier
        @type entity_id: string
        @param ext_ref: the external reference
        @type ext_ref: L{CexternalReference}
        """
        node_entity = self.map_entity_id_to_node.get(entity_id)
        if node_entity is not None:
            entity = Centity(node_entity,self.type)
            entity.add_external_reference(ext_ref)
        else:
            print>>sys.stderr,'Trying to add a reference to the entity',entity_id,'but can not be found in this file'
        

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
                
    def to_kaf(self):
        """
        Converts the layer from KAF to NAF
        """
        if self.type == 'NAF':
            for node in self.__get_entity_nodes():
                node.set('eid',node.get('id'))
                del node.attrib['id']

    def to_naf(self):
        """
        Converts the layer from NAF to KAF
        """
        if self.type == 'KAF':
            for node in self.__get_entity_nodes():
                node.set('id',node.get('eid'))
                del node.attrib['eid']
                
    def __get_entity_nodes(self):
        for ent_node in self.node.findall('entity'):
            yield ent_node
                
    def __iter__(self):
        """
        Iterator that returns the entities of the layer
        @rtype: L{Centity}
        @return: list of entities (iterator)
        """
        for ent_node in self.__get_entity_nodes():
            yield Centity(ent_node,self.type)
        
        
    def __str__(self):
        return dump(self.node)
