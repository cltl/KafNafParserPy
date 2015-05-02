"""
Parser for the factvalue layer in KAF/NAF
"""

from lxml import etree

class Cfactvalue:
	"""
	This class encapsulates a factvalue object in KAF/NAF
	"""
	def __init__(self,node=None):
		"""
		Constructor of the object
		@type node: xml Element or None (to create and empty one)
		@param node: this is the node of the element.
			If it is None it will create a new object
		"""
		if node is None:
			self.node = etree.Element('factvalue')
		else:
			self.node = node

	def get_node(self):
		"""
		Returns the node of the element
		@rtype: xml Element
		@return: the node of the element
		"""
		return self.node

	def get_id(self):
		"""
		Returns the fact identifier
		@rtype: string
		@return: the fact identifier
		"""
		return self.node.get('id')

	def get_prediction(self):
		"""
		Returns the prediction attribute of the factvalue
		@rtype: string
		@return: the prediction attribute
		"""
		return self.node.get('prediction')

	def get_confidence(self):
		"""
		Returns the confidence of the element
		@rtype: string
		@return: the confidence of the element
		"""
		return self.node.get('confidence')

	def set_id(self,this_id):
		"""
		Set the identifier for the fact
		@type this_id: string
		@param this_id: the identifier
		"""
		return self.node.set('id',this_id)

	def set_prediction(self,prediction):
		"""
		Sets the prediction attribute
		@type prediction: string
		@param prediction: the prediction attribute
		"""
		self.node.set('prediction',prediction)

	def set_confidence(self,confidence):
		"""
		Sets the confidence attribute
		@type confidence: string
		@param confidence: the confidence attribute
		"""
		self.node.set('confidence',confidence)

	def __str__(self):
		return dump(self.node)

class Cfactualitylayer:
	"""
	This class encapsulates the factvalue layer in KAF/NAF
	"""
	def __init__(self,node=None):
		"""
		Constructor of the object
		@type node: xml Element or None (to create and empty one)
		@param node: this is the node of the element.
			If it is None it will create a new object
		"""
		if node is None:
			self.node = etree.Element('factualitylayer')
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

	def __get_factvalue_nodes(self):
		for node_factvalue in self.node.findall('factvalue'):
			yield node_factvalue

	def get_factvalues(self):
		"""
		Iterator that returns all the factualitylayer in the layer
		@rtype: L{Cfactvalue}
		@return: list of factualitylayer (iterator)
		"""
		for node in self.__get_factvalue_nodes():
			yield Cfactvalue(node)

	def add_factvalue(self,my_factvalue):
		"""
		Adds a factvalue object to the layer
		@type my_factvalue: L{Cfactvalue}
		@param my_factvalue: the factvalue object to be added
		"""
		self.node.append(my_factvalue.get_node())

	def remove_this_factvalue(self,factvalue_id):
		"""
		Removes the factvalue for the given factvalue identifier
		@type factvalue_id: string
		@param factvalue_id: the factvalue identifier to be removed
		"""
		for fact in self.get_factvalues():
			if fact.get_id() == factvalue_id:
				self.node.remove(fact.get_node())
				break
