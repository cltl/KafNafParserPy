"""
This module implements a parser for KAF or NAF files. It allows to parse an input KAF/NAF file and extract information from the
different layers as python objects. It also allows to create a new KAF/NAF file or add new information to an existing one

@author: U{Ruben Izquierdo Bevia<rubenizquierdobevia.com>}
@version: 1.3
@contact: U{ruben.izquierdobevia@vu.nl<mailto:ruben.izquierdobevia@vu.nl>} 
@contact: U{rubensanvi@gmail.com<mailto:rubensanvi@gmail.com>}
@contact: U{rubenizquierdobevia.com}
@since: 28-Jan-2015
"""
from KafNafParserPy.markable_data import Cmarkables
	
############### Changes   #####################
# v1.1 --> added functions to add external refs to entities and to read them
# v1.2 --> added functions to add new entities to the NAF/KAF file
# v1.3 --> added set_raw(text)
# v1.3.1 --> added functions to set and get fileDesc attributes
# v1.3.2 --> added markable layer and main accompanying functions
################################################


__last_modified__  = '2September2015'
__version__ = '1.3.1'
__author__ = 'Ruben Izquierdo Bevia'

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
from time_data import *
from causal_data import *
from temporal_data import *
from factuality_data import *
from markable_data import *


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
		self.raw = None
		self.timex_layer = None
		self.causalRelations_layer = None
		self.temporalRelations_layer = None
		self.factuality_layer = None
		self.markable_layer = None
	
		
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

		node_timex = self.root.find('timeExpressions')
		if node_timex is not None:
			self.timex_layer = CtimeExpressions(node_timex)

		node_temporalRelations = self.root.find('temporalRelations')
		if node_temporalRelations is not None:
			self.temporalRelations_layer = CtemporalRelations(node_temporalRelations)

		node_causalRelations = self.root.find('causalRelations')
		if node_causalRelations is not None:
			self.causalRelations_layer = CcausalRelations(node_causalRelations)

		node_factualitylayer = self.root.find('factualitylayer')
		if node_factualitylayer is not None:
			self.factuality_layer = Cfactualitylayer(node_factualitylayer)
			
		node_factualities = self.root.find('factualities')
		if node_factualities is not None:
			self.factuality_layer = Cfactualities(node_factualities)

		node_raw = self.root.find('raw')
		if node_raw is not None:
			self.raw = node_raw.text
			
		node_markables = self.root.find('markables')
		if node_markables is not None:
			self.markable_layer = Cmarkables(node_markables)
	
	def get_header(self):
		'''
		Returns the header object
		@return: the header object 
		@rtype: L{CHeader}
		'''
		return self.header
	
	def set_language(self,l):
		"""
		Sets the language to the KAF root element
		@param l: the language code
		@type l: string
		"""
		self.root.set('{http://www.w3.org/XML/1998/namespace}lang',l)
		                
	def set_version(self,v):
                """
                Sets the language to the KAF root element
		@param v: the language code
		@type v: string
		"""
		self.root.set('version',v) 
		
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
			
		
		## Convert the temporalRelations layer
		## It is not defined on KAF so we assme both will be similar
		if self.temporalRelations_layer is not None:
			self.temporalRelations_layer.to_kaf()

		## Convert the causalRelations layer
		## It is not defined on KAF so we assme both will be similar
		if self.causalRelations_layer is not None:
			self.causalRelations_layer.to_kaf()

		## Convert the factualitylayer
		## It is not defined on KAF so we assme both will be similar
		if self.factuality_layer is not None:
			self.factuality_layer.to_kaf()

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
		

			
		## Convert the temporalRelations layer
		## It is not defined on KAF so we assume both will be similar
		if self.temporalRelations_layer is not None:
			self.temporalRelations_layer.to_naf()	#Does nothing...

		## Convert the causalRelations layer
		## It is not defined on KAF so we assume both will be similar
		if self.causalRelations_layer is not None:
			self.causalRelations_layer.to_naf()	#Does nothing...

		## Convert the factuality layer
		## It is not defined on KAF so we assume both will be similar
		if self.factuality_layer is not None:
			self.factuality_layer.to_naf()		#Does nothing...
			
		
		## Convert the markable layer
		## It is not defined on KAF so we assume both will be similar
		if self.markable_layer is not None:
			self.markable_layer.to_naf()		#Changes identifier attribute nothing else...

				
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
	
	def get_trees_as_list(self):
		"""
		Iterator that returns the constituency trees
		@rtype: L{Ctree}
		@return: iterator to all the constituency trees
		"""
		mytrees = []
		if self.constituency_layer is not None:
			for tree in self.constituency_layer.get_trees():
				mytrees.append(tree)
				return mytrees

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
				
	def get_tlinks(self):
		"""
		Iterator that returns the tlinks from the temporalRelations layer. Use it as:
		for my_tlink in my_obj.get_tlinks():
		@rtype: L{Ctlink}
		@returns: iterator to get all the tlinks
		"""
		if self.temporalRelations_layer is not None:
			for tlink in self.temporalRelations_layer.get_tlinks():
				yield tlink

	def get_clinks(self):
		"""
		Iterator that returns the clinks from the causalRelations layer. Use it as:
		for my_clink in my_obj.get_clinks():
		@rtype: L{Cclink}
		@returns: iterator to get all the clinks
		"""
		if self.causalRelations_layer is not None:
			for clink in self.causalRelations_layer.get_clinks():
				yield clink

	def get_factvalues(self):
		"""
		Iterator that returns the factvalues from the factuality layer. Use it as:
		for my_fact in my_obj.get_factvalues():
		@rtype: L{Cfactvalue}
		@returns: iterator to get all the factvalues
		"""
		if self.factuality_layer is not None:
			for fact in self.factuality_layer.get_factvalues():
				yield fact 

	def get_corefs(self):
		"""
		Iterator that returns the corefs from the coreferences layer.
		@rtype: L{Ccoreference}
		@returns: iterator to get all the coreferences
		"""
		if self.coreference_layer is not None:
			for coref in self.coreference_layer.get_corefs():
				yield coref 

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
			
	def get_markables(self):
		"""Iterator that returns all the markables from the markable layer
		@rtype: L{Cmarkable}
		@return: list of markable objects
		"""
		if self.markable_layer is not None:
			for markable in self.markable_layer:
				yield markable
				
	def get_markable(self,markable_id):
		"""
		Returns a markable object for the specified markable_id
		@type markable_id:string
		@param markable_id: entity identifier
		@rtype: L{Cmarkable}
		@return: markable object
		"""
		if self.markable_layer is not None:
			return self.markable_layer.get_markable(markable_id)
		else:
			return None
			
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
	
	
	def get_entity(self,entity_id):
		"""
		Returns an entity object for the specified entity_id
		@type entity_id:string
		@param entity_id: entity identifier
		@rtype: L{Centity}
		@return: entity object
		"""
		if self.entity_layer is not None:
			return self.entity_layer.get_entity(entity_id)
		else:
			return None
	
				
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
		
	def get_raw(self):
		"""
		Returns the raw text as a string
		@rtype: string
		@return: the raw text
		"""
		if self.raw is not None:
			return self.raw
				
	def set_raw(self,text):
		"""
		Sets the text of the raw element (or creates the layer if does not exist)
		@param text: text of the raw layer
		@type text: string
		"""
		node_raw = self.root.find('raw')
		if node_raw is None:
			node_raw = etree.Element('raw')
			self.root.insert(0,node_raw)
		node_raw.text = etree.CDATA(text)
		
	def get_timeExpressions(self):
		"""
		Returns a list of all the timeexpressions in the text
		@rtype: L{Ctime}
		@return: list of time expressions (iterator)
		"""
		if self.timex_layer is not None:
			for time in self.timex_layer.get_timeExpressions():
				yield time

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
			self.entity_layer = None
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
			
			
	def remove_temporalRelations_layer(self):
		"""
		Removes the temporalRelations layer (if exists) of the object (in memory)
		"""
		if self.temporalRelations_layer is not None:
			this_node = self.temporalRelations_layer.get_node()
			self.root.remove(this_node)
			self.temporalRelations_layer = None

		if self.header is not None:
			self.header.remove_lp('temporalRelations')

	def remove_causalRelations_layer(self):
		"""
		Removes the causalRelations layer (if exists) of the object (in memory)
		"""
		if self.causalRelations_layer is not None:
			this_node = self.causalRelations_layer.get_node()
			self.root.remove(this_node)
			self.causalRelations_layer = None

		if self.header is not None:
			self.header.remove_lp('causalRelations')

	def remove_factualitylayer_layer(self):
		"""
		Removes the factualitylayer layer (the old version) (if exists) of the object (in memory)
		"""
		if self.factuality_layer is not None:
			this_node = self.factuality_layer.get_node()
			self.root.remove(this_node)
			self.factuality_layer = None

		if self.header is not None:
			self.header.remove_lp('factualitylayer')

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
			
	
	
	def remove_text_layer(self):
		"""
		Removes the text layer (if exists) of the object (in memory)
		"""
		if self.text_layer is not None:
			this_node = self.text_layer.get_node()
			self.root.remove(this_node)
			self.text_layer = None
			
		if self.header is not None:
			self.header.remove_lp('text')
	
	
	def remove_coreference_layer(self):
		"""
		Removes the constituency layer (if exists) of the object (in memory)
		"""
		if self.coreference_layer is not None:
			this_node = self.coreference_layer.get_node()
			self.root.remove(this_node)
		if self.header is not None:
			self.header.remove_lp('coreferences')
	
	
	def convert_factualitylayer_to_factualities(self):
		"""
		Takes information from factuality layer in old representation
		Creates new factuality representation and removes the old layer
		"""
		if self.factuality_layer is not None:
			this_node = self.factuality_layer.get_node()
			if this_node.tag == 'factualitylayer':
				new_node = Cfactualities()
				#create dictionary from token ids to the term ids 
				token2term = {}
				for t in self.get_terms():
					s = t.get_span()
					for w in s.get_span_ids():
						token2term[w] = t.get_id()
				fnr = 0
				for fv in self.get_factvalues():
					fnr += 1
					conf = fv.get_confidence()
					wid = fv.get_id()
					tid = token2term.get(wid)
					fnode = Cfactuality()
					#set span with tid as element
					fspan = Cspan()
					fspan.add_target_id(tid)
					fnode.set_span(fspan)
					#add factVal element with val, resource = factbank, + confidence if present
					fVal = Cfactval()
					fVal.set_resource('factbank')
					fVal.set_value(fv.get_prediction())
					if conf:
						fVal.set_confidence(conf)
					fnode.set_id('f' + str(fnr))
					fnode.add_factval(fVal)
					new_node.add_factuality(fnode)
				self.root.remove(this_node)
				self.root.append(new_node.get_node())
				self.factuality_layer = new_node
					
	
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
		
	def add_markable(self,markable_obj):
		"""
		Adds a markable to the markable layer
		@type markable_obj: L{Cmarkable}
		@param markable_obj: the markable object
		"""
		if self.markable_layer is None:
			self.markable_layer = Cmarkables(type=self.type)
			self.root.append(self.markable_layer.get_node())
		self.markable_layer.add_markable(markable_obj)
	
	
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


	def add_predicate(self, predicate_obj):
		"""
		Adds a predicate to the semantic layer
		@type predicate_obj: L{Cpredicate}
		@param predicate_obj: the predicate object
		"""
		if self.srl_layer is None:
			self.srl_layer = Csrl()
			self.root.append(self.srl_layer.get_node())
		self.srl_layer.add_predicate(predicate_obj)

	def add_timex(self, time_obj):
		"""
		Adds a timex entry to the time layer
		@type time_obj: L{Ctime}
		@param time_obj: time time object
		"""
		if self.timex_layer is None:
			self.timex_layer = CtimeExpressions()
			self.root.append(self.timex_layer.get_node())
		self.timex_layer.add_timex(time_obj)
	

	def set_header(self,header):
		"""
		Sets the header of the object
		@type header: L{CHeader}
		@param header: the header object
		"""	
		self.root.insert(0,header.get_node())
		
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

	def add_tlink(self,my_tlink):
		"""
		Adds a tlink to the temporalRelations layer
		@type my_tlink: L{Ctlink}
		@param my_tlink: tlink object
		"""
		if self.temporalRelations_layer is None:
			self.temporalRelations_layer = CtemporalRelations()
			self.root.append(self.temporalRelations_layer.get_node())
		self.temporalRelations_layer.add_tlink(my_tlink)

	def add_clink(self,my_clink):
		"""
		Adds a clink to the causalRelations layer
		@type my_clink: L{Cclink}
		@param my_clink: clink object
		"""
		if self.causalRelations_layer is None:
			self.causalRelations_layer = CcausalRelations()
			self.root.append(self.causalRelations_layer.get_node())
		self.causalRelations_layer.add_clink(my_clink)

	def add_factuality(self,my_fact):
		"""
		Adds a factvalue to the factuality layer
		@type my_fact: L{Cfactvalue}
		@param my_fact: factvalue object
		"""
		if self.factuality_layer is None:
			self.factuality_layer = Cfactualitylayer()
			self.root.append(self.factuality_layer.get_node())
		self.factuality_layer.add_factvalue(my_fact)

	def add_entity(self,entity):
		"""
		Adds an entity to the entity layer
		@type entity: L{Centity}
		@param entity: the entity object
		"""
		if self.entity_layer is None:
			self.entity_layer = Centities(type=self.type)
			self.root.append(self.entity_layer.get_node())
		self.entity_layer.add_entity(entity)
			
			
	def add_coreference(self, coreference):
		"""
		Adds an coreference to the coreference layer
		@type coreference: L{Ccoreference}
		@param coreference: the coreference object
		"""
		if self.coreference_layer is None:
			self.coreference_layer = Ccoreferences(type=self.type)
			self.root.append(self.coreference_layer.get_node())
		self.coreference_layer.add_coreference(coreference)
			
				
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
			
	
	def remove_external_references_from_terms(self):
		"""
		Removes all external references present in the term layer
		"""
		if self.term_layer is not None:
			for term in self.term_layer:
				term.remove_external_references()
			
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
			
			
	
	def remove_external_references_from_srl_layer(self):
		"""
		Removes all external references present in the term layer
		"""
		if self.srl_layer is not None:
			for pred in self.srl_layer.get_predicates():
				pred.remove_external_references()
				pred.remove_external_references_from_roles()
			
	def add_external_reference_to_entity(self,entity_id, external_ref):
		"""
		Adds an external reference to the given entity identifier in the entity layer
		@type entity_id: string
		@param entity_id: the entity identifier
		@param external_ref: an external reference object
		@type external_ref: L{CexternalReference}
		"""
		if self.entity_layer is not None:
			self.entity_layer.add_external_reference_to_entity(entity_id,external_ref)
			
		
