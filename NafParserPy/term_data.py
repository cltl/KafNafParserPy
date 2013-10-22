from span_data import span
from external_references_data import *
from term_sentiment_data import term_sentiment
from lxml import etree


class term:
    def __init__(self,node=None):
        if node is None:
            self.node = etree.Element('term')
        else:
            self.node = node
            
        #self.id = self.type = self.lemma = self.pos = self.morphofeat = self.head = self.case = ''
        #self.span = None
        #self.term_sentiment = None
        #self.externalReferences = None
        #self.node = node
            
    def get_id(self):
        return self.node.get('id')
    
    def get_lemma(self):
        return self.node.get('lemma')
    
    def get_pos(self):
        return self.node.get('pos')
    
    def get_span(self):
        node_span = self.node.find('span')
        if node_span is not None:
            return span(node_span)
        else:
            return None
        
        
    def add_external_reference(self,ext_ref):
        ext_refs_node = self.node.find('externalReferences')
        if ext_refs_node is None:
            ext_refs_obj = externalReferences()
            self.node.append(ext_refs_obj.get_node())
        else:
            ext_refs_obj = externalReferences(ext_refs_node)
            
        ext_refs_obj.add_external_reference(ext_ref)
            
           
        
    
class terms:
    def __init__(self,node=None):
        self.idx = {}
        if node is None:
            self.node = etree.Element('terms')
        else:
            self.node = node
            for node_term in self.__get_node_terms():
                self.idx[node_term.get('id')] = node_term    
    
    def __get_node_terms(self):
        for node_term in self.node.findall('term'):
            yield node_term
            
    def __iter__(self):
        for node_term in self.__get_node_terms():
            yield term(node_term)
            
    def get_term(self,term_id):
        if term_id in self.idx:
            return term(self.idx[term_id])
        else:
            return None
           
    def add_external_reference(self,term_id, external_ref):
        if term_id in self.idx:
            term_obj = term(self.idx[term_id])
            term_obj.add_external_reference(external_ref)


if __name__ == '__main__':
    from lxml import etree
    data = '''
        <terms>
<term id="t1" lemma="John" pos="R">
<span>
<target id="w1"/>
</span>
</term>
<term id="t2" type="open" lemma="teach" pos="V">
<span>
<target id="w2"/>
</span>
</term>
<term id="t3" lemma="mathematics" pos="N">
<span>
<target id="w3"/>
</span>
</term>
<term id="t4" lemma="20" pos="N">
<span>
<target id="w4"/>
</span>
</term>
<term id="t5" lemma="minute" pos="N">
<span>
<target id="w5"/>
</span>
</term>
<term id="t5" lemma="every" pos="D">
<span>
<target id="w6"/>
</span>
</term>
<term id="t6" lemma="Monday" pos="N">
<span>
<target id="w7"/>
</span>
</term>
<term id="t7" lemma="in" pos="P">
<span>
<target id="w8"/>
</span>
</term>
<term id="t8" lemma="New_York" pos="R">
<span>
<target id="w9"/>
<target id="w10"/>
NewsReader: ICT-316404 October 9, 2013
NAF 20/43
</span>
</term>
<term id="t2" lemma="nice" pos="G">
<sentiment resource="VUA_polarityLexicon_word" polarity="positive"
strength="average" subjectivity="subjective"
sentiment_semantic_type="behaviour/trait" />
<span><target id="w2"/></span>
<!-- sense level sentiment annotation -->
</term>
</terms>'''
    
    node = etree.fromstring(data, parser=None, base_url=None)
    obj = terms(node)
    print obj