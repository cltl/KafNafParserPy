
"""
This module implements a parser for KAF or NAF files. It allows to parse an input KAF/NAF file and extract information from the
different layers as python objects. It also allows to create a new KAF/NAF file or add new information to an existing one
"""
	

__last_modified  = '17dec2013'

from lxml import etree
from header_data import *
from text_data import *
from term_data import *
from entity_data import *
from features_data import *
from opinion_data import *
from constituency_data import *
from dependency_data import *
from feature_extractor import Cdependency_extractor, Cconstituency_extractor
from coreference_data import *
from srl_data import *
from external_references_data import *

import sys



class KafNafParser:
	def __init__(self,filename=None,type=None):
		"""
		The constructor for the parser
		@type filename: string
		@param filename: KAF/NAF filename. Set it to None to create an empty file
		@type type: string
		@param type: to indicate if the file will be a NAF or a KAF file, in case of new files.
		"""
		
		self.tree = None
		if filename is not None:
			self.filename = filename
			self.tree = etree.parse(filename,etree.XMLParser(remove_blank_text=True))
		else:
			self.tree = etree.ElementTree(etree.Element(type))
		self.root = self.tree.getroot()
		self.type = self.root.tag # KAF NAF
		
		self.header = None
		self.text_layer = None
		self.term_layer = None
		self.entity_layer = None
		self.features_layer = None
		self.opinion_layer = None
		self.constituency_layer = None
		self.dependency_layer = None
		self.coreference_layer = None
		self.srl_layer = None
		
		## Specific feature extractor for complicated layers
		self.my_dependency_extractor = None
		self.my_constituency_extractor = None
		##################################################
		
		#######
		self.dict_tokens_for_tid = None
		self.terms_for_token = None
		##
		
		self.lang = self.root.get('{http://www.w3.org/XML/1998/namespace}lang')
		self.version = self.root.get('version')
		
		if self.type == 'NAF':
			node_header = self.root.find('nafHeader')
		elif self.type == 'KAF':
			node_header = self.root.find('kafHeader')
			
		if node_header is not None:
			self.header = CHeader(node_header,self.type)
		
		# Text layer adapted to naf/kaf
		node_text = self.root.find('text')
		if node_text is not None:
			self.text_layer = Ctext(node=node_text,type=self.type)
			
		node_term = self.root.find('terms')
		if node_term is not None:
			self.term_layer = Cterms(node=node_term,type=self.type)
			
		node_entity = self.root.find('entities')
		if node_entity is not None:
			self.entity_layer = Centities(node_entity,type=self.type)
			
		node_features = self.root.find('features')
		if node_features is not None:
			self.features_layer = Cfeatures(node_features,type=self.type)

		node_opinions = self.root.find('opinions')
		if node_opinions is not None:
			self.opinion_layer = Copinions(node_opinions,type=self.type)
			
		# Definition KAF/NAF is the same
		node_constituency = self.root.find('constituency')
		if node_constituency is not None:
			self.constituency_layer = Cconstituency(node_constituency)

		# Definition KAF/NAF is the same
		node_dependency = self.root.find('deps')
		if node_dependency is not None:
			self.dependency_layer = Cdependencies(node_dependency)
			
		node_coreferences = self.root.find('coreferences')
		if node_coreferences is not None:
			self.coreference_layer = Ccoreferences(node_coreferences,type=self.type)
			
		node_srl = self.root.find('srl')
		if node_srl is not None:
			self.srl_layer = Csrl(node_srl)
	
	def get_type(self):
		"""
		Returns the type (NAF/KAF) of the object
		@rtype: string
		@return: the type of the file
		"""
		
		return self.type
	
	def get_filename(self):
		"""
		Returns the name of the filename
		@rtype: string
		@return: the filename of the KAF/NAF object
		"""
		return self.filename
		
	def to_kaf(self):
		"""
		Converts a NAF object to KAF (in memory). You will have to use the method dump later to save it as a new KAF file
		"""
		
		if self.type == 'NAF':
			self.root.tag = 'KAF'
			self.type = 'KAF'
		
		## Convert the header	
		if self.header is not None:
			self.header.to_kaf()
		
		## Convert the token layer
		if self.text_layer is not None:
			self.text_layer.to_kaf()
			
		## Convert the term layer
		if self.term_layer is not None:
			self.term_layer.to_kaf()
			
		## Convert the entity layer
		if self.entity_layer is not None:
			self.entity_layer.to_kaf()
			
		## Convert the features layer
		## There is no feature layer defined in NAF, but we assumed
		## that is defined will be followin the same rules
		if self.features_layer is not None:
			self.features_layer.to_kaf()
			
		
		##Convert the opinion layer
		if self.opinion_layer is not None:
			self.opinion_layer.to_kaf()
			
		## Convert the constituency layer
		## This layer is exactly the same in KAF/NAF
		if self.constituency_layer is not None:
			self.constituency_layer.to_kaf()	#Does nothing...
			
			
		## Convert the dedepency layer
		## It is not defined on KAF so we assme both will be similar
		if self.dependency_layer is not None:
			self.dependency_layer.to_kaf()
			
		if self.coreference_layer is not None:
			self.coreference_layer.to_kaf()
			
		
	def to_naf(self):
		"""
		Converts a KAF object to NAF (in memory). You will have to use the method dump later to save it as a new NAF file
		"""
		if self.type == 'KAF':
			self.root.tag = self.type = 'NAF'
		
		## Convert the header	
		if self.header is not None:
			self.header.to_naf()
		
		## Convert the token layer
		if self.text_layer is not None:
			self.text_layer.to_naf()
		
			
		## Convert the term layer
		if self.term_layer is not None:
			self.term_layer.to_naf()
			
		
		## Convert the entity layer
		if self.entity_layer is not None:
			self.entity_layer.to_naf()
		
		## Convert the features layer
		## There is no feature layer defined in NAF, but we assumed
		## that is defined will be followin the same rules
		if self.features_layer is not None:
			self.features_layer.to_naf()
			
		
		##Convert the opinion layer
		if self.opinion_layer is not None:
			self.opinion_layer.to_naf()
		
			
		## Convert the constituency layer
		## This layer is exactly the same in KAF/NAF
		if self.constituency_layer is not None:
			self.constituency_layer.to_naf()	#Does nothing...
			
			
		## Convert the dedepency layer
		## It is not defined on KAF so we assume both will be similar
		if self.dependency_layer is not None:
			self.dependency_layer.to_naf()	  #Does nothing...
			
		if self.coreference_layer is not None:
			self.coreference_layer.to_naf()
		

			
	def print_constituency(self):
		"""
		Prints the constituency layer
		"""
		print self.constituency_layer
		
	def get_trees(self):
		"""
		Iterator that returns the constituency trees
		@rtype: L{Ctree}
		@return: iterator to all the constituency trees
		"""
		
		if self.constituency_layer is not None:
			for tree in self.constituency_layer.get_trees():
				yield tree
		

	def get_dependencies(self):
		"""
		Iterator that returns the dependencies from the dependency layer. Use it as:
		for my_dep in my_obj.get_dependencies():
		@rtype: L{Cdependency}
		@returns: iterator to get all the dependencies
		"""
		if self.dependency_layer is not None:
			for dep in self.dependency_layer.get_dependencies():
				yield dep
				
	def get_language(self):
		"""
		Returns the code language of the file
		@rtype: string
		@returns: language code of the file
		"""
		return self.lang
		
	
	def get_tokens(self):
		"""Iterator that returns all the tokens from the text layer
		@rtype: L{Cwf}
		@return: list of token objects
		"""
		for token in self.text_layer:
			yield token
			
	def get_terms(self):
		"""Iterator that returns all the terms from the term layer
		@rtype: L{Cterm}
		@return: list of term objects
		"""
		if self.term_layer is not None:
			for term in self.term_layer:
				yield term
			
	def get_token(self,token_id):
		"""
		Returns a token object for the specified token_id
		@type token_id:string
		@param token_id: token identifier
		@rtype: L{Cwf}
		@return: token object
		"""
		if self.text_layer is not None:
			return self.text_layer.get_wf(token_id)
		else:
			return None
	

	def get_term(self,term_id):
		"""
		Returns a term object for the specified term_id
		@type term_id:string
		@param term_id: token identifier
		@rtype: L{Cterm}
		@return: term object
		"""
		if self.term_layer is not None:
			return self.term_layer.get_term(term_id)
		else:
			return None
		
	def get_properties(self):
		"""
		Returns all the properties of the features layer (iterator)
		@rtype: L{Cproperty}
		@return: list of properties
		"""
		if self.features_layer is not None:
			for property in self.features_layer.get_properties():
				yield property
		
	def get_entities(self):
		"""
		Returns a list of all the entities in the object
		@rtype: L{Centity}
		@return: list of entities (iterator)
		"""
		if self.entity_layer is not None:
			for entity in self.entity_layer:
				yield entity
				
	def get_opinions(self):
		"""
		Returns a list of all the opinions in the object
		@rtype: L{Copinion}
		@return: list of opinions (iterator)
		"""
		if self.opinion_layer is not None:
			for opinion in self.opinion_layer.get_opinions():
				yield opinion
		
	def get_predicates(self):
		"""
		Returns a list of all the predicates in the object
		@rtype: L{Cpredicate}
		@return: list of predicates (iterator)
		"""
		if self.srl_layer is not None:
			for pred in self.srl_layer.get_predicates():
				yield pred
	
	def dump(self,filename=sys.stdout):
		"""
		Dumps the object to an output filename (or open file descriptor). The filename
		parameter is optional, and if it is not provided, the standard output will be used
		@type filename: string or file descriptor
		@param filename: file where to dump the object (default standard output)
		"""
		
		self.tree.write(filename,encoding='UTF-8',pretty_print=True,xml_declaration=True)
		
		
	def remove_entity_layer(self):
		"""
		Removes the entity layer (if exists) of the object (in memory)
		"""
		if self.entity_layer is not None:
			this_node = self.entity_layer.get_node()
			self.root.remove(this_node)
		if self.header is not None:
			self.header.remove_lp('entities')
			
	def remove_dependency_layer(self):
		"""
		Removes the dependency layer (if exists) of the object (in memory)
		"""
		if self.dependency_layer is not None:
			this_node = self.dependency_layer.get_node()
			self.root.remove(this_node)
			self.dependency_layer = self.my_dependency_extractor = None
			
		if self.header is not None:
			self.header.remove_lp('deps')
			
			
	def remove_constituency_layer(self):
		"""
		Removes the constituency layer (if exists) of the object (in memory)
		"""
		if self.constituency_layer is not None:
			this_node = self.constituency_layer.get_node()
			self.root.remove(this_node)
		if self.header is not None:
			self.header.remove_lp('constituents')
			
			
	def remove_this_opinion(self,opinion_id):
		"""
		Removes the opinion with the provided opinion identifier
		@type opinion_id: string
		@param opinion_id: the opinion identifier of the opinion to remove
		"""
		if self.opinion_layer is not None:
			self.opinion_layer.remove_this_opinion(opinion_id)
			
	def remove_opinion_layer(self):
		"""
		Removes the opinion layer (if exists) of the object (in memory)
		"""
		if self.opinion_layer is not None:
			this_node = self.opinion_layer.get_node()
			self.root.remove(this_node)
			self.opinion_layer = None
			
		if self.header is not None:
			self.header.remove_lp('opinions')
			
	def remove_properties(self):
		"""
		Removes the property layer (if exists) of the object (in memory)
		"""
		if self.features_layer is not None:
			self.features_layer.remove_properties()
			
		if self.header is not None:
			self.header.remove_lp('features')
			
			
	def remove_term_layer(self):
		"""
		Removes the term layer (if exists) of the object (in memory)
		"""
		if self.term_layer is not None:
			this_node = self.term_layer.get_node()
			self.root.remove(this_node)
			self.term_layer = None
			
		if self.header is not None:
			self.header.remove_lp('terms')
			
	
	def get_constituency_extractor(self):
		"""
		Returns a constituency extractor object
		@rtype: L{Cconstituency_extractor}
		@return: a constituency extractor object
		"""
		
		if self.constituency_layer is not None:	##Otherwise there are no constituens
			if self.my_constituency_extractor is None:
				self.my_constituency_extractor = Cconstituency_extractor(self)
			return self.my_constituency_extractor
		else:
			return None
	
	def get_dependency_extractor(self):
		"""
		Returns a dependency extractor object
		@rtype: L{Cdependency_extractor}
		@return: a dependency extractor object
		"""
		if self.dependency_layer is not None:	#otherwise there are no dependencies
			if self.my_dependency_extractor is None:
				self.my_dependency_extractor = Cdependency_extractor(self)
			return self.my_dependency_extractor
		else:
			return None
		
	## ADDING METHODS
	def add_wf(self,wf_obj):
		"""
		Adds a token to the text layer
		@type wf_obj: L{Cwf}
		@param wf_obj: the token object
		"""
		if self.text_layer is None:
			self.text_layer = Ctext(type=self.type)
			self.root.append(self.text_layer.get_node())
		self.text_layer.add_wf(wf_obj)	
		
	def add_term(self,term_obj):
		"""
		Adds a term to the term layer
		@type term_obj: L{Cterm}
		@param term_obj: the term object
		"""
		if self.term_layer is None:
			self.term_layer = Cterms(type=self.type)
			self.root.append(self.term_layer.get_node())
		self.term_layer.add_term(term_obj)
	
	
	def add_opinion(self,opinion_obj):
		"""
		Adds an opinion to the opinion layer
		@type opinion_obj: L{Copinion}
		@param opinion_obj: the opinion object
		"""
		if self.opinion_layer is None:
			self.opinion_layer = Copinions()
			self.root.append(self.opinion_layer.get_node())
		self.opinion_layer.add_opinion(opinion_obj)
		
	
	def add_linguistic_processor(self, layer ,my_lp):
		"""
		Adds a linguistic processor to the header
		@type my_lp: L{Clp}
		@param my_lp: linguistic processor object
		@type layer: string
		@param layer: the layer to which the processor is related to
		"""
		if self.header is None:
			self.header = CHeader(type=self.type)		
			self.root.insert(0,self.header.get_node())
		self.header.add_linguistic_processor(layer,my_lp)
		
	
	def add_dependency(self,my_dep):
		"""
		Adds a dependency to the dependency layer
		@type my_dep: L{Cdependency}
		@param my_dep: dependency object
		"""
		if self.dependency_layer is None:
			self.dependency_layer = Cdependencies()
			self.root.append(self.dependency_layer.get_node())
		self.dependency_layer.add_dependency(my_dep)
		
		
	def add_constituency_tree(self,my_tree):
		"""
		Adds a constituency tree to the constituency layer
		@type my_tree: L{Ctree}
		@param my_tree: the constituency tree object
		"""
		if self.constituency_layer is None:
			self.constituency_layer = Cconstituency()
			self.root.append(self.constituency_layer.get_node())
		self.constituency_layer.add_tree(my_tree)
		
	## Adds a property to the feature layer
	def add_property(self,label,term_span,pid=None):
		"""
		Adds a property to the property layer
		@type label: string
		@param label: the type of property
		@type term_span: list
		@param term_span: list of term ids
		@type pid: string
		@param pid: the identifier for the property (use None to automatically generate one)
		"""
		if self.features_layer is None:
			self.features_layer = Cfeatures(type=self.type)
			self.root.append(self.features_layer.get_node())
		self.features_layer.add_property(pid, label,term_span)
	
	## EXTRA FUNCTIONS
	## Gets the token identifiers in the span of a term id
	def get_dict_tokens_for_termid(self, term_id):
		"""
		Returns the tokens ids that are the span of the term specified
		@type term_id: string
		@param term_id: the term idenfier
		@rtype: list
		@return: list of token ids that are the span of the term
		"""
		if self.dict_tokens_for_tid is None:
			self.dict_tokens_for_tid = {}
			for term in self.get_terms():
				self.dict_tokens_for_tid[term.get_id()] = term.get_span().get_span_ids()
		
		return self.dict_tokens_for_tid.get(term_id,[])
	
	## Maps a list of token ids to term ids
	def map_tokens_to_terms(self,list_tokens):
		"""
		Maps a list of token ids to the corresponding term ids
		@type list_tokens: list
		@param list_tokens: list of token identifiers
		@rtype: list
		@return: list of term idenfitiers
		"""
		if self.terms_for_token is None:
			self.terms_for_token = {}
			for term in self.get_terms():
				termid = term.get_id()
				token_ids = term.get_span().get_span_ids()
				for tokid in token_ids:
					if tokid not in self.terms_for_token:
						self.terms_for_token[tokid] = [termid]
					else:
						self.terms_for_token[tokid].append(termid)
					
		ret = set()
		for my_id in list_tokens:
			term_ids = self.terms_for_token.get(my_id,[])
			ret |= set(term_ids)
		return sorted(list(ret))
	
	def remove_tokens_of_sentence(self,sentence_id):
		"""
		Removes the tokens belonging to the supplied sentence
		@type sentence_id: string
		@param sentence_id: a sentence identifier
		"""
		self.text_layer.remove_tokens_of_sentence(sentence_id)
		
	def remove_terms(self,list_term_ids):
		"""
		Removes the list of terms specified
		@type list_term_ids: list
		@param list_term_ids: list of term identifiers
		"""
		self.term_layer.remove_terms(list_term_ids)
		
		
	def add_external_reference(self,term_id, external_ref):
		self.add_external_reference_to_term(term_id, external_ref)

	def add_external_reference_to_term(self,term_id, external_ref):
		"""
		Adds an external reference to the given term identifier
		@type term_id: string
		@param term_id: the term identifier
		@param external_ref: an external reference object
		@type external_ref: L{CexternalReference}
		"""
		if self.term_layer is not None:
			self.term_layer.add_external_reference(term_id, external_ref)	
			
	def add_external_reference_to_role(self,role_id,external_ref):
		"""
		Adds an external reference to the given role identifier in the SRL layer
		@type role_id: string
		@param role_id: the role identifier
		@param external_ref: an external reference object
		@type external_ref: L{CexternalReference}
		"""
		if self.srl_layer is not None:
			self.srl_layer.add_external_reference_to_role(role_id,external_ref)
			
		