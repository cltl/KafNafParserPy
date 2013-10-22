from term_sentiment_data import term_sentiment

class externalReference:
    def __init__(self,node):
        self.resource = self.reference = self.refType = self.status = self.source = self.confidence = ''
        self.sentiment = None
        self.subreferences = []
        if node is not None:
            self.resource = node.get('resource','')
            self.reference = node.get('reference','')
            self.reftype = node.get('reftype','')
            self.status = node.get('status','')
            self.source = node.get('source','')
            self.confidence = node.get('confidence','')
            self.sentiment = term_sentiment(node.find('sentiment'))
            for subref_node in node.findall('externalRef'):
                self.subreferences.append(externalReference(subref_node))
            
    def __str__(self):
        s = 'externalReference\n'
        s += '  Res: '+self.resource+' Ref:'+self.reference+'  Type:'+self.reftype+' stat:'+self.status+' src:'+self.source+' Conf:'+self.confidence+'\n'
        s += '  Sentiment:'+str(self.sentiment)
        if len(self.subreferences) != 0:
            s += '\n    Subreferences:\n'
            for subref in self.subreferences:
                s+= '    '+str(subref)+'\n'                 
        return s
    

class externalReferences:
    def __init__(self,node):
        self.references = []
        if node is not None:
            for node_ref in node.findall('externalRef'):
                self.references.append(externalReference(node_ref))
                
    def __str__(self):
        s = 'externalReferences\n'
        for r in self.references:
            s += '\t\t\t'+str(r)+'\n'
        return s
    

if __name__=='__main__':
    from lxml import etree
    data2 = '''
    <externalReferences>
    <externalRef resource="WN-1.7" reference="eng-17-00861095-v" confidence="0.80">
        <externalRef resource="ontology" reference="Teach" reftype="SubClassOf">
             <externalRef resource="WN-1.7" reftype='sdsd' reference="eng-17-00859568-v" confidence="0.20">
                 <externalRef resource="WN-1.7" reftype='sdsd' reference="eng-17-00859568-v" confidence="0.69"/>
             </externalRef>
        </externalRef>
    </externalRef>
</externalReferences>
'''
    data='''
<externalReferences>
<externalRef resource="WN-ENG" reference="c_1009" conf="0.38">
<sentiment resource="VUA_polarityLexicon_synset" polarity="positive"
strength="average" subjectivity="subjective"
sentiment_semantic_type="behaviour/traitEvaluation"/>
</externalRef>
<externalRef resource="WN-ENG" reference="c_1008" conf="0.31">

</externalRef>
</externalReferences>
'''
    obj = etree.fromstring(data2, parser=None, base_url=None)
    node = externalReferences(obj)
    print node    
    