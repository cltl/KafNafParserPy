"""
Parser for the tlink layer in KAF/NAF
"""
from lxml import etree

class Ctlink:
	"""
	This class encapsulates a tlink object in KAF/NAF
	"""
	def __init__(self,node=None):
		"""
		Constructor of the object
		@type node: xml Element or None (to create and empty one)
		@param node: this is the node of the element.
			If it is None it will create a new object
		"""
		if node is None:
			self.node = etree.Element('tlink')
		else:
			self.node = node
			
	def get_node_comment(self):
		"""
		Returns the lxml element for the comment
		@rtype: lxml Element
		@return: the lxml element for the comment
		"""
		return self.node_comment
	
	def get_node(self):
		"""
		Returns the node of the element
		@rtype: xml Element
		@return: the node of the element
		"""
		return self.node

	def get_id(self):
		"""
		Returns the token identifier
		@rtype: string
		@return: the token identifier
		"""
		return self.node.get('id')

	def get_from(self):
		"""
		Returns the from attribute of the tlink
		@rtype: string
		@return: the from attribute
		"""
		return self.node.get('from')
	
	def get_fromType(self):
		"""
		Returns the from attribute of the tlink
		@rtype: string
		@return: the from attribute
		"""
		return self.node.get('fromType')
	
	def get_to(self):
		"""
		Returns the to attribute of the tlink
		@rtype: string
		@return: the to attribute
		"""
		return self.node.get('to')
	
	def get_toType(self):
		"""
		Returns the to attribute of the tlink
		@rtype: string
		@return: the to attribute
		"""
		return self.node.get('toType')
	
	def get_relType(self):
		"""
		Returns the to attribute of the tlink
		@rtype: string
		@return: the to attribute
		"""
		return self.node.get('relType')
	
	def set_id(self,this_id):
		"""
		Set the identifier for the token
		@type this_id: string
		@param this_id: the identifier
		"""
		return self.node.set('id',this_id)

	def set_from(self, f):
		"""
		Sets the from attribute
		@type f: string
		@param f: the from attribute
		"""
		self.node.set('from',f)
	
	def set_fromType(self, f):
		"""
		Sets the from attribute
		@type f: string
		@param f: the from attribute
		"""
		self.node.set('fromType',f)
	
	def set_to(self,t):
		"""
		Sets the to attribute
		@type t: string
		@param t: the to attribute
		"""
		self.node.set('to',t)
	
	def set_toType(self,t):
		"""
		Sets the to attribute
		@type t: string
		@param t: the to attribute
		"""
		self.node.set('toType',t)
	
	def set_relType(self,t):
		"""
		Sets the to attribute
		@type t: string
		@param t: the to attribute
		"""
		self.node.set('relType',t)
	
	def set_comment(self,c):
		"""
		Sets the XML comment for the tlink
		@type c: string
		@param c: the string comment
		"""
		c = c.replace('--','- -')
		self.node.insert(0,etree.Comment(c))
	
	def __str__(self):
		return dump(self.node)

class CpredicateAnchor:
	"""
	This class encapsulates the predicateAnchor object in KAF/NAF
	"""
	
	def __init__(self,node=None):
		"""
		Constructor of the object
		@type node: xml Element or None (to create and empty one)
		@param node: this is the node of the element.
			If it is None it will create a new object
		"""
		if node is None:
			self.node = etree.Element('predicateAnchor')
		else:
			self.node = node


	def set_id(self,this_id):
		"""
		Set the identifier for the token
		@type this_id: string
		@param this_id: the identifier
		"""
		return self.node.set('id',this_id)


	def get_id(self):
		"""
		Returns the token identifier
		@rtype: string
		@return: the token identifier
		"""
		return self.node.get('id')
	
	
	def get_anchorTime(self):
		"""
		Returns the anchorTime
		@rtype: string
		@return: the anchorTime 
		"""
		return self.node.get('anchorTime')
	
	
	def set_anchorTime(self,anchorTime):
		"""
		Set the anchor time for the event
		@type anchorTime: string
		@param anchorTime: the anchorTime id
		"""
		return self.node.set('anchorTime',anchorTime)
	
	def get_endPoint(self):
		"""
		Returns the endPoint
		@rtype: string
		@return: the endPoint 
		"""
		return self.node.get('endPoint')
	
	
	def set_endPoint(self,endPoint):
		"""
		Set the endPoint for the event
		@type endPoint: string
		@param endPoint: the endPoint id
		"""
		return self.node.set('endPoint',endPoint)
	
	
	def get_beginPoint(self):
		"""
		Returns the beginPoint
		@rtype: string
		@return: the beginPoint 
		"""
		return self.node.get('beginPoint')
	
	
	def set_beginPoint(self,beginPoint):
		"""
		Set the beginPoint for the event
		@type beginPoint: string
		@param beginPoint: the beginPoint id
		"""
		return self.node.set('beginPoint',beginPoint)


	def get_span(self):
        """
        Returns the span object of the element
        @rtype: L{Cspan}
        @return: the span object of the element
        """
        
        node = self.node.find('span')
        if node is not None:
           	return Cspan(node)
       	else:
           	return None



    def set_span(self, this_span):
        """
        Sets the span for the predicate
        @type this_span: L{Cspan}
        @param this_span: the span object
        """
        self.node.append(this_span.get_node())



class CtemporalRelations:
	"""
	This class encapsulates the tlink layer in KAF/NAF
	"""
	def __init__(self,node=None):
		"""
		Constructor of the object
		@type node: xml Element or None (to create and empty one)
		@param node: this is the node of the element.
			If it is None it will create a new object
		"""
		if node is None:
			self.node = etree.Element('temporalRelations')
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
		pass
	
	def to_naf(self):
		pass
			
	def __str__(self):
		return dump(self.node)


	def __get_node_temporalRelations(self):
		for node_tlink in self.node.findall('tlink'):
			yield node_tlink
			
			
	def __get_node_predicateAnchors(self):
		for node_predAnch in self.node.findall('predicateAnchor'):
			yield node_predAnch
		
	def get_tlinks(self):
		"""
		Iterator that returns all the temporalRelations in the layer
		@rtype: L{Ctlink}
		@return: list of temporalRelations (iterator)
		"""
		for node in self.__get_node_temporalRelations():
			yield Ctlink(node)
			
	
	def get_predicateAnchors(self):
		"""
		Iterator that returns all the temporalRelation anchors in the layer
		@rtype: L{CpredicateAnchor}
		@return: list of temporalRelations (iterator)
		"""
		for node in self.__get_node_predicateAnchors():
			yield CpredicateAnchor(node)
			
	def add_tlink(self,my_tlink):
		"""
		Adds a tlink object to the layer
		@type my_tlink: L{Ctlink}
		@param my_tlink: the tlink object to be added
		"""
		self.node.append(my_tlink.get_node())
			
	def remove_this_tlink(self,tlink_id):
		"""
		Removes the tlink for the given tlink identifier
		@type tlink_id: string
		@param tlink_id: the tlink identifier to be removed
		"""
		for tlink in self.get_tlinks():
			if tlink.get_id() == tlink_id:
				self.node.remove(tlink.get_node())
				break
			
	def add_predicatAnchor(self,my_predAnch):
		"""
		Adds a predAnch object to the layer
		@type my_predAnch: L{CpredAnch}
		@param my_predAnch: the predAnc object to be added
		"""
		self.node.append(my_predAnch.get_node())
			
	def remove_this_predicateAnchor(self,predAnch_id):
		"""
		Removes the predicate anchor for the given predicate anchor identifier
		@type predAnch_id: string
		@param predAnch_id: the predicate anchor identifier to be removed
		"""
		for predAnch in self.get_predicateAnchors():
			if predAnch.get_id() == predAnch_id:
				self.node.remove(predAnch.get_node())
				break
