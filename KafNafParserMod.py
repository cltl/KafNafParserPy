## LIST OF CHANGES
# Ruben 8-nov-2013 
#    + included layers for entities, properties, opinions
#    + renamed all classes to Cnameoftheclass
# Ruben 15-nov-2013
#	+ included constituency layer
#
# Ruben 19-nov-2013
#	+ included dependency layer
# Ruben 17-dec-2013
#	+ modified all to red/write NAF and KAF
#
# Ruben 21-Feb-2014
#	+ Included coreference layer
from KafNafParserPy.features_data import Cfeatures
	

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

import sys



class KafNafParser:
	def __init__(self,filename):
		self.tree = None
		self.filename = filename
		self.tree = etree.parse(filename,etree.XMLParser(remove_blank_text=True))
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
	
	def get_type(self):
		return self.type
	
	def get_filename(self):
		return self.filename
		
	def to_kaf(self):
		#Convert the root
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
		#Convert the root
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
		print self.constituency_layer
		
	def get_trees(self):
		if self.constituency_layer is not None:
			for tree in self.constituency_layer.get_trees():
				yield tree
		
		
	def get_dependencies(self):
		if self.dependency_layer is not None:
			for dep in self.dependency_layer.get_dependencies():
				yield dep
				
	def get_language(self):
		return self.lang
		
	def get_tokens(self):
		for token in self.text_layer:
			yield token
			
	def get_terms(self):
		if self.term_layer is not None:
			for term in self.term_layer:
				yield term
			
	def get_token(self,token_id):
		if self.text_layer is not None:
			return self.text_layer.get_wf(token_id)
		else:
			return None
	
	def get_term(self,term_id):
		if self.term_layer is not None:
			return self.term_layer.get_term(term_id)
		else:
			return None
		
	def get_properties(self):
		if self.features_layer is not None:
			for property in self.features_layer.get_properties():
				yield property
		
	def get_entities(self):
		if self.entity_layer is not None:
			for entity in self.entity_layer:
				yield entity
				
	def get_opinions(self):
		if self.opinion_layer is not None:
			for opinion in self.opinion_layer.get_opinions():
				yield opinion
		
	
	def dump(self,filename=sys.stdout):
		self.tree.write(filename,encoding='UTF-8',pretty_print=True,xml_declaration=True)
		
		
	def remove_entity_layer(self):
		if self.entity_layer is not None:
			this_node = self.entity_layer.get_node()
			self.root.remove(this_node)
		if self.header is not None:
			self.header.remove_lp('entities')
			
	def remove_dependency_layer(self):
		if self.dependency_layer is not None:
			this_node = self.dependency_layer.get_node()
			self.root.remove(this_node)
			self.dependency_layer = self.my_dependency_extractor = None
			
		if self.header is not None:
			self.header.remove_lp('deps')
			
			
	def remove_constituency_layer(self):
		if self.constituency_layer is not None:
			this_node = self.constituency_layer.get_node()
			self.root.remove(this_node)
		if self.header is not None:
			self.header.remove_lp('constituents')
	def remove_this_opinion(self,opinion_id):
		if self.opinion_layer is not None:
			self.opinion_layer.remove_this_opinion(opinion_id)
			
	def remove_opinion_layer(self):
		if self.opinion_layer is not None:
			this_node = self.opinion_layer.get_node()
			self.root.remove(this_node)
			self.opinion_layer = None
			
		if self.header is not None:
			self.header.remove_lp('opinions')
			
	def remove_properties(self):
		if self.features_layer is not None:
			self.features_layer.remove_properties()
			
		if self.header is not None:
			self.header.remove_lp('features')
			
			
	def remove_term_layer(self):
		if self.term_layer is not None:
			this_node = self.term_layer.get_node()
			self.root.remove(this_node)
			self.term_layer = None
			
		if self.header is not None:
			self.header.remove_lp('terms')
			
	def get_constituency_extractor(self):
		if self.constituency_layer is not None:	##Otherwise there are no constituens
			if self.my_constituency_extractor is None:
				self.my_constituency_extractor = Cconstituency_extractor(self)
			return self.my_constituency_extractor
		else:
			return None
	
	def get_dependency_extractor(self):
		if self.dependency_layer is not None:	#otherwise there are no dependencies
			if self.my_dependency_extractor is None:
				print>>sys.stderr,'Created dependencies'
				self.my_dependency_extractor = Cdependency_extractor(self)
			return self.my_dependency_extractor
		else:
			return None
		
	## ADDING METHODS
	def add_wf(self,wf_obj):
		if self.text_layer is None:
			self.text_layer = Ctext(type=self.type)
			self.root.append(self.text_layer.get_node())
		self.text_layer.add_wf(wf_obj)	
	
	def add_opinion(self,opinion_obj):
		if self.opinion_layer is None:
			self.opinion_layer = Copinions()
			self.root.append(self.opinion_layer.get_node())
		self.opinion_layer.add_opinion(opinion_obj)
		
	def add_linguistic_processor(self, layer ,my_lp):
		self.header.add_linguistic_processor(layer,my_lp)
		
	
	def add_dependency(self,my_dep):
		if self.dependency_layer is None:
			self.dependency_layer = Cdependencies()
			self.root.append(self.dependency_layer.get_node())
		self.dependency_layer.add_dependency(my_dep)
		
	## Adds a property to the feature layer
	def add_property(self,label,term_span,pid=None):
		if self.features_layer is None:
			self.features_layer = Cfeatures(type=self.type)
			self.root.append(self.features_layer.get_node())
		self.features_layer.add_property(pid, label,term_span)
	
	## EXTRA FUNCTIONS
	## Gets the token identifiers in the span of a term id
	def get_dict_tokens_for_termid(self, term_id):
		if self.dict_tokens_for_tid is None:
			self.dict_tokens_for_tid = {}
			for term in self.get_terms():
				self.dict_tokens_for_tid[term.get_id()] = term.get_span().get_span_ids()
		
		return self.dict_tokens_for_tid.get(term_id,[])
	
	## Maps a list of token ids to term ids
	def map_tokens_to_terms(self,list_tokens):
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
		self.text_layer.remove_tokens_of_sentence(sentence_id)
		
	def remove_terms(self,list_term_ids):
			self.term_layer.remove_terms(list_term_ids)
		
		
			
		