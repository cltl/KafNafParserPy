from lxml import etree

from nafHeader_data import *
from text_data import *
from term_data import *


class NafParser:
	def __init__(self,filename):
		self.tree = None
		self.tree = etree.parse(filename,etree.XMLParser(remove_blank_text=True))
		self.root = self.tree.getroot()
		self.naf_header = None
		self.text_layer = None
		self.term_layer = None
		
		self.lang = self.root.get('{http://www.w3.org/XML/1998/namespace}lang')
		self.version = self.root.get('version')
		
		node_header = self.root.find('nafHeader')
		if node_header is not None:
			self.naf_header = nafHeader(node_header)
		
		node_text = self.root.find('text')
		if node_text is not None:
			self.text_layer = text(node_text)
			
		node_term = self.root.find('terms')
		if node_term is not None:
			self.term_layer = terms(node_term)
			
		
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
			
		