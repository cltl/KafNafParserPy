from span_data import span
from external_references_data import *
from term_sentiment_data import term_sentiment


class term:
    def __init__(self,node):
        self.id = self.type = self.lemma = self.pos = self.morphofeat = self.head = self.case = ''
        self.span = None
        self.term_sentiment = None
        self.externalReferences = None
        
        if node is not None:
            self.id = node.get('id','')
            self.type = node.get('type','')
            self.lemma = node.get('lemma','')
            self.pos = node.get('pos','')
            self.morphofeat = node.get('morphofeat','')
            self.head = node.get('head','')
            self.case = node.get('case','')
            
            node_span = node.find('span')
            if node_span is not None: self.span = span(node_span)
            
            node_sentiment = node.find('sentiment')
            if node_sentiment is not None: self.term_sentiment = term_sentiment(node_sentiment)
            
            node_extref = node.find('externalReferences')
            if node_extref is not None: self.externalReferences = externalReferences(node_extref)
            
    def get_id(self):
        return self.id
    
    def get_lemma(self):
        return self.lemma
    
    def get_pos(self):
        return self.pos
    
    def get_span(self):
        return self.span
        
            
    def __str__(self):
        #s='Term: '+self.id+'  lemma:'+self.lemma+'.'+self.pos+' '+self.morphofeat+' '+self.head+' '+self.case+'\n'
        s='Term: '+self.id+'  lemma:'+self.lemma+'.'+self.pos+' '+self.morphofeat+'\n'
        s += str(self.span)+'\n'
        if self.term_sentiment is not None:
            s += 'Sentiment:'+str(self.term_sentiment)+'\n'
        if self.externalReferences is not None:
            s += 'ExternalRefs:'+str(self.externalReferences) +'\n'
        return s
            
        
    
class terms:
    def __init__(self,node):
        self.terms = []
        self.idx = {}
        if node is not None:
            for term_node in node.findall('term'):
                self.terms.append(term(term_node))
                this_id = self.terms[-1].get_id()
                this_pos = len(self.terms)-1
                self.idx[this_id] = this_pos
                
    
    def __iter__(self):
        for term in self.terms:
            yield term
            
    def get_term(self,term_id):
        this_position = self.idx.get(term_id,None)
        if this_position is not None:
            return self.terms[this_position]
        else:
            return None
    
    def __str__(self):
        s = 'Terms\n'
        for t in self.terms:
            s+=str(t)+'\n'
        return s
    

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