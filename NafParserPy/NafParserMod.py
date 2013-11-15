## LIST OF CHANGES
# Ruben 8-nov-2013 
#    + included layers for entities, properties, opinions
#    + renamed all classes to Cnameoftheclass
# Ruben 15-nov-2013
#	+ included constituency layer


__last_modified='15nov2013'

from lxml import etree
from nafHeader_data import *
from text_data import *
from term_data import *
from entity_data import *
from features_data import *
from opinion_data import *
from constituency_data import *

import sys



class NafParser:
	def __init__(self,filename):
		self.tree = None
		self.tree = etree.parse(filename,etree.XMLParser(remove_blank_text=True))
		self.root = self.tree.getroot()
		self.naf_header = None
		self.text_layer = None
		self.term_layer = None
		self.entity_layer = None
		self.features_layer = None
		self.opinion_layer = None
		self.constituency_layer = None
		
		self.lang = self.root.get('{http://www.w3.org/XML/1998/namespace}lang')
		self.version = self.root.get('version')
		
		node_header = self.root.find('nafHeader')
		if node_header is not None:
			self.naf_header = CnafHeader(node_header)
		
		node_text = self.root.find('text')
		if node_text is not None:
			self.text_layer = Ctext(node_text)
			
		node_term = self.root.find('terms')
		if node_term is not None:
			self.term_layer = Cterms(node_term)
			
		node_entity = self.root.find('entities')
		if node_entity is not None:
			self.entity_layer = Centities(node_entity)
			
		node_features = self.root.find('features')
		if node_features is not None:
			self.features_layer = Cfeatures(node_features)

		node_opinions = self.root.find('opinions')
		if node_opinions is not None:
			self.opinion_layer = Copinions(node_opinions)
			
		node_constituency = self.root.find('constituency')
		if node_constituency is not None:
			self.constituency_layer = Cconstituency(node_constituency)
			
	def print_constituency(self):
		print self.constituency_layer
		
	def get_trees(self):
		for tree in self.constituency_layer.get_trees():
			yield tree
		
	def get_language(self):
		return self.lang
		
	def get_tokens(self):
		for token in self.text_layer:
			yield token
			
	def get_terms(self):
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
		
	def add_external_reference(self,lemma_id, external_ref):
		self.term_layer.add_external_reference(lemma_id, external_ref)
		

	def add_linguistic_processor(self, layer ,my_lp):
		self.naf_header.add_linguistic_processor(layer,my_lp)

	
	def dump(self,filename=sys.stdout):
		self.tree.write(filename,encoding='UTF-8',pretty_print=True,xml_declaration=True)
		
	def add_opinion(self,opinion_obj):
		if self.opinion_layer is None:
			self.opinion_layer = Copinions()
			self.root.append(self.opinion_layer.get_node())
		self.opinion_layer.add_opinion(opinion_obj)
		
			
		