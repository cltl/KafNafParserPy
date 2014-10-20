""""
This is a parser for the header section of KAF/NAF
"""

from lxml import etree
import time
import platform 

class CfileDesc:
    """
    This class encapsulates the file description element in the header
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type = 'KAF/NAF'
        if node is None:
            self.node = etree.Element('fileDesc')
        else:
            self.node = node
    
    #self.title=''    #self.author=''    #self.creationtime=''    #self.filename=''    #self.filetype=''    #self.pages=''
    
 
class Cpublic:
    """
    This class encapsulates the public element in the header
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type = 'KAF/NAF'
        if node is None:
            self.node = etree.Element('public')
        else:
            self.node = node
            
        #self.publicId = ''
        #slf.uri = ''

   
class Clp:
    """
    This class encapsulates the linguistic processor element in the header
    """
    def __init__(self,node=None,name="",version="",timestamp=None,btimestamp=None,etimestamp=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create an empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type name: string
        @param name: the name of the linguistic processor
        @type version: string
        @param version: the version of the linguistic processor
        @type timestamp: string
        @param timestamp: the timestamp, or None to set it to the current time
        @param btimestamp: the begin timestamp, or None to set it to the current time (NOTE: only use None if header created at begining of process!)
        @param etimestamp: the end timestamp, or None to set it (NOTE: only use None if header created at the end of the process!)
        """
        self.type = 'KAF/NAF'
        if node is None:
            self.node = etree.Element('lp')
            self.set_name(name)
            self.set_version(version)
            self.set_timestamp(timestamp)
            self.set_beginTimestamp(btimestamp)
            self.set_endTimestamp(etimestamp)
            
            #For the hostnameimport platform
            self.node.set('hostname',platform.node())
            
        else:
            self.node = node
            
    def set_name(self,name):
        """
        Set the name of the linguistic processor
        @type name:string
        @param name: name of the linguistic processor
        """
        self.node.set('name',name)
        
    def set_version(self,version):
        """
        Set the version of the linguistic processor
        @type version:string
        @param version: version of the linguistic processor
        """
        self.node.set('version',version)
        
    def set_timestamp(self,timestamp=None):
        """
        Set the timestamp of the linguistic processor, set to None for the current time
        @type timestamp:string
        @param timestamp: version of the linguistic processor
        """
        if timestamp is None:
            import time
            timestamp = time.strftime('%Y-%m-%dT%H:%M:%S%Z')
        self.node.set('timestamp',timestamp)

    def set_beginTimestamp(self,btimestamp=None):
        """
        Set the begin timestamp of the linguistic processor, set to None for the current time
        @type btimestamp: string
        @param btimestamp: version of the linguistic processor
        """
        if btimestamp is None:
            import time
            btimestamp = time.strftime('%Y-%m-%dT%H:%M:%S%Z')
        self.node.set('beginTimestamp',btimestamp)

    def set_endTimestamp(self,etimestamp=None):
        """
        Set the end timestamp of the linguistic processor, set to None for the current time
        @type etimestamp: string
        @param etimestamp: version of the linguistic processor
        """
        if etimestamp is None:
            import time
            etimestamp = time.strftime('%Y-%m-%dT%H:%M:%S%Z')
        self.node.set('endTimestamp',etimestamp)





    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
        
    
class ClinguisticProcessors:
    """
    This class encapsulates the linguistic processors element in the header
    """
    def __init__(self,node=None):
        """
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        """
        self.type = 'KAF/NAF'
        if node is None:
            self.node = etree.Element('linguisticProcessors')
        else:
            self.node = node
            
    def get_layer(self):
        """
        Returns the layer of the element
        @rtype: string
        @return: the layer of the element
        """
        return self.node.get('layer')
    
    def set_layer(self,layer):
        """
        Set the layer of the element
        @type layer: string
        @param layer: layer
        """
        self.node.set('layer',layer)
    
    def add_linguistic_processor(self,my_lp):
        """
        Add a linguistic processor object to the layer
        @type my_lp: L{Clp}
        @param my_lp: linguistic processor object
        """
        self.node.append(my_lp.get_node())
        
    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node

    
class CHeader:
    """
    This class encapsulates the header
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
            if self.type == 'NAF':
                self.node = etree.Element('nafHeader')
            elif self.type == 'KAF':
                self.node = etree.Element('kafHeader')
        else:
            self.node = node

    def get_node(self):
        """
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        """
        return self.node
            
    def to_kaf(self):
        """
        Converts the header element to KAF
        """
        if self.type == 'NAF':
            self.node.tag = 'kafHeader'
            self.type = 'KAF'
        
    def to_naf(self):
        """
        Converts the header element to NAF
        """
        if self.type == 'KAF':
            self.node.tag = 'nafHeader'
            self.type = 'NAF'
      
    def add_linguistic_processors(self,linpro):
        """Adds a linguistic processors element
        @type linpro: ClinguisticProcessors
        @param linpro: linguistic processors element
        """
        self.node.append(linpro.get_node())
        
    def remove_lp(self,layer):
        """
        Removes the linguistic processors for a given layer
        @type layer: string
        @param layer: the name of the layer
        """
        for this_node in self.node.findall('linguisticProcessors'):
            if this_node.get('layer') == layer:
                self.node.remove(this_node)
                break
            
        
    def add_linguistic_processor(self, layer ,my_lp):
        """
        Adds a linguistic processor to a certain layer
        @type layer: string
        @param layer: the name of the layer
        @type my_lp: L{Clp}
        @param my_lp: the linguistic processor
        """
        ## Locate the linguisticProcessor element for taht layer
        found_lp_obj = None
        for this_lp in self.node.findall('linguisticProcessors'):
            lp_obj = ClinguisticProcessors(this_lp)
            if lp_obj.get_layer() == layer:
                found_lp_obj = lp_obj
                break
        
        if found_lp_obj is None:    #Not found
            found_lp_obj = ClinguisticProcessors()
            found_lp_obj.set_layer(layer)
            self.add_linguistic_processors(found_lp_obj)
            
        found_lp_obj.add_linguistic_processor(my_lp)
        
        
            
    