"""
This module allows to extract elaborated information from the dependency layer of a KAF/NAF object
"""

from operator import itemgetter
import sys

def get_max_distr_dict(my_dict):
    vect = my_dict.items()
    if len(vect) !=0:
        vect.sort(key=itemgetter(1),reverse=True)
        return vect[0]
    return None
    
class Cdependency_extractor:
    """
    This is the main class for the information extraction
    """
    def __init__(self,knaf_obj):
        """
        The constructor of this class take one kaf/naf object
        @type knaf_obj: kaf/naf object
        @param knaf_obj: the kaf/naf object
        """
        self.naf = knaf_obj
        self.relations_for_term = {}
        self.reverse_relations_for_term = {}
        self.prefix_for_reverse = ''
        
       
        already_linked = {}
        for dep in knaf_obj.get_dependencies():
            term_from = dep.get_from()
            term_to = dep.get_to()
            rfunc = dep.get_function()
            
            # Dependencies reversed are skipped...
            #if rfunc.startswith('rhd/') or rfunc.startswith('whd/'):
            #    continue
            
            #  For detecting cycles like:
            #       <!-- rhd/body(geef,wat) -->  
            #       <dep from="t19" to="t15" rfunc="rhd/body"/>
            #       <!-- hd/su(wat,geef) -->
            #      <dep from="t15" to="t19" rfunc="hd/su"/>
            
            '''
            if term_from in already_linked and term_to in already_linked[term_from]:
                #There could be a cycle, skip this 
                print>>sys.stderr,'Skipped from',term_from,'to',term_to,'func',rfunc,' cycle detected'
                continue
            else:
                #Include term_from as linked with term_to for future...
                if term_to not in already_linked:
                    already_linked[term_to] = set()
                already_linked[term_to].add(term_from)
            ''' 
                
                        

            
            if term_from in self.relations_for_term:
                self.relations_for_term[term_from].append((rfunc,term_to))
            else:
                self.relations_for_term[term_from] = [(rfunc,term_to)]
        
            if term_to in self.reverse_relations_for_term:                
                self.reverse_relations_for_term[term_to].append((self.prefix_for_reverse+rfunc,term_from))
            else:
                self.reverse_relations_for_term[term_to] = [(self.prefix_for_reverse+rfunc,term_from)]
        
        
        self.paths_for_termid={}      
        self.sentence_for_termid={}  
        self.top_relation_for_term = {}     ## termid --> (relation,topnode)
        self.root_for_sentence = {}         ## sentenceid --> termid
        
        for term_obj in knaf_obj.get_terms():
            termid = term_obj.get_id()
            
            #Calculating the sentence id for the term id
            span_ids = term_obj.get_span().get_span_ids()
            token_obj = knaf_obj.get_token(span_ids[0])
            if token_obj is None:
                continue
                
            sentence = token_obj.get_sent()
            
            self.sentence_for_termid[termid] = sentence
            ###########################################
            
            #paths = self.__propagate_node(termid,[])
            #inversed = self.__reverse_propagate_node(termid)
            
            ## Due to the change on direction of dependencies...
            inversed = self.__propagate_node(termid,already_propagated=[])
            paths = self.__reverse_propagate_node(termid,already_propagated=[])

            ##Calculate the top relation for the node, the relation with the main root of the tree
            if len(inversed) != 0:
                for ip in inversed:
                    if len(ip)!=0:
                        self.top_relation_for_term[termid] = ip[-1] ## ex. ('NMOD', 't2')
                        root = ip[-1][1]
                        if sentence not in self.root_for_sentence:
                            self.root_for_sentence[sentence] = {}
                        
                        if root not in self.root_for_sentence[sentence]:
                            self.root_for_sentence[sentence][root]=0
                        else:
                            self.root_for_sentence[sentence][root]+=1
                        break
                    
            self.paths_for_termid[termid] = paths + inversed
            
            '''
            print termid
            print 'DIRECT RELS'
            for p in paths:
                print ' ',p 
                
            print 'INDIRECT RELS'
            for p in inversed:
                print ' ',p 
            '''
        ####

        for sent_id, distr in self.root_for_sentence.items():
            ## get_max_distr_dict imported from VUA_pylib.common
            most_freq,c = get_max_distr_dict(distr)
            self.root_for_sentence[sent_id] = most_freq

        
        
        
    def __propagate_node(self,node,already_propagated=[]):
        paths = []
        
        relations = self.relations_for_term.get(node)
        #print 'Propagate ',node,relations
        if relations is None:   ##Case base
            paths = [[]] 
        elif node in already_propagated:
            paths = [[]]

        else:    
            already_propagated.append(node)
            for func, target_node in relations:
                new_paths = self.__propagate_node(target_node, already_propagated)
                for new_path in new_paths:
                    new_path.insert(0,(func,target_node))
                    paths.append(new_path)
        return paths

    def __reverse_propagate_node(self,node,already_propagated=[]):
        paths = []
        relations = self.reverse_relations_for_term.get(node)
        #print 'Propagate reverse',node,relations,already_propagated
        if relations is None:   ##Case base
            paths = [[]] 
        elif node in already_propagated:
            paths = [[]]
        else:    
            already_propagated.append(node)
            for func, target_node in relations:
                new_paths = self.__reverse_propagate_node(target_node,already_propagated)
                for new_path in new_paths:
                    new_path.insert(0,(func,target_node))
                    paths.append(new_path)
        return paths        


    # Get the shortest path between 2 term ids
    def get_shortest_path(self,term1,term2):
        """
        Returns the list of dependency labels of the shortest path between two terms
        @type term1: string
        @param term1: the term identifier for one term  
        @type term2: string
        @param term2: the term identifier for the other term  
        @rtype: list
        @return: list of dependency relations
        """
        dep_path = None
        if term1 == term2: dep_path = []
        else:
            paths1 = self.paths_for_termid[term1]
            paths2 = self.paths_for_termid[term2]

            ##Check if term2 is on paths1 
            hits = [] ## list of (common_id,idx1,idx2,numpath1,numpath2)
            for num1, p1 in enumerate(paths1):
                ids1 = [ my_id for my_func, my_id in p1]
                if term2 in ids1:
                    idx1 = ids1.index(term2)
                    hits.append((term2,idx1+0,idx1,0,num1,None))
                    
            for num2,p2 in enumerate(paths2):
                ids2 = [ my_id for my_func, my_id in p2]
                if term1 in ids2:
                    idx2=ids2.index(term1)
                    hits.append((term1,0+idx2,0,idx2,None,num2))
                    
            #Pair by pair
            for num1, p1 in enumerate(paths1):
                #print 'Path1',term1, p1
                ids1 = [ my_id for my_func, my_id in p1]
                #print 'IDS1',ids1
                for num2, p2 in enumerate(paths2):
                    #print '\t',term2,p2
                    ids2 = [ my_id for my_func, my_id in p2]
                    #print '  IDS2',ids2
                    common_ids = set(ids1) & set(ids2)
                    #print '  cmmon',common_ids
                    for common_id in common_ids:
                        idx1 = ids1.index(common_id)
                        idx2 = ids2.index(common_id)
                        hits.append((common_id,idx1+idx2,idx1,idx2,num1,num2))

                        
            if len(hits) != 0:
                dep_path = []
                hits.sort(key=itemgetter(1))
                best_hit = hits[0]
                common_id, _, idx1, idx2, numpath1, numpath2 = best_hit
                
                if numpath2 is None:  #term2 is in one of the paths of t1
                    path1 = paths1[numpath1]
                    my_rels1 = path1[:idx1+1]
                    ##complete_path = ''
                    ##complete_path_ids = ''
                    for func,node in my_rels1:
                        dep_path.append(func)
                        ##complete_path+=func+'#'
                        ##complete_path_ids+=node+'#'
                        
                    #===========================================================
                    # print 'CASE1',best_hit
                    # print complete_path
                    # print complete_path_ids
                    #===========================================================
                elif numpath1 is None: #term1 is in one of the paths of t2
                    path2 = paths2[numpath2]
                    my_rels2 = path2[:idx2+1]
                    ##complete_path = ''
                    ##complete_path_ids = ''
                    for func,node in my_rels2:
                        dep_path.append(func)
                        #complete_path+=func+'#'
                        #complete_path_ids+=node+'#'
                        
                    #===========================================================
                    # print 'CASE2',best_hit
                    # print complete_path
                    # print complete_path_ids
                    #===========================================================
                else:   #There is a common node linking both
                    path1 = paths1[numpath1]
                    my_rels1 = path1[:idx1+1]
                    
                    path2 = paths2[numpath2]
                    my_rels2 = path2[:idx2+1]
                    
                    ##complete_path = ''
                    #complete_path_ids = ''
                    for func,node in my_rels1:
                        dep_path.append(func)
                        ##complete_path+=func+'#'
                        #complete_path_ids+=func+'->'+self.naf.get_term(node).get_lemma()+'->'
                        
                    for func,node in my_rels2[-1::-1]:
                        dep_path.append(func)
                        ##complete_path+=func+'#'
                        #complete_path_ids+=func+'->'+self.naf.get_term(node).get_lemma()+'->'
                    #===========================================================
                    #    
                    # print complete_path
                    # print complete_path_ids
                    # print path2
                    # print my_rels1
                    # print my_rels2
                    # print 'CASE3',best_hit
                    #===========================================================
        return dep_path
    
    ## Get the shortest dependency path between 2 sets of spans
    def get_shortest_path_spans(self,span1,span2):
        """
        Returns the list of dependency labels of the shortest path between two span of terms
        @type span1: list
        @param span1: list of term identifiers
        @type span2: list
        @param span2: list of term identifiers 
        @rtype: list
        @return: list of dependency relations
        """
        shortest_path = None
        
        for term1 in span1:
            for term2 in span2:
                this_path = self.get_shortest_path(term1, term2)
                #print term1,term2, this_path
                if shortest_path is None or (this_path is not None and len(this_path)<len(shortest_path)):
                    shortest_path = this_path
        return shortest_path
    
    # Get the dependency path to the sentence root for a term id
    def get_path_to_root(self,termid):
        """
        Returns the dependency path from the term to the root
        @type termid: string
        @param termid: the term identifier
        @rtype: list
        @return: list of dependency relations
        """        
        # Get the sentence for the term
        root = None
        sentence = self.sentence_for_termid.get(termid)
        
        if sentence is None:    #try with the top node
            top_node = self.top_relation_for_term.get(termid)
            if top_node is not None:
                root = top_node[1]
            else:
                return None
        else:
            if sentence in self.root_for_sentence:
                root = self.root_for_sentence[sentence]
            else:
                ##There is no root for this sentence
                return None
        # In this point top_node should be properly set
        path = self.get_shortest_path(termid, root)
        return path
    
    # Get the shortest dependency path to the sentence root for a span of ids
    # extractor.get_shortest_path_to_root_span(['t444','t445','t446'])
    def get_shortest_path_to_root_span(self,span):
        """
        Returns the dependency path from a span of terms to the root
        @type span: list
        @param span: list of term identifiers
        @rtype: list
        @return: list of dependency relations
        """  
        shortest_path = None
        for termid in span:
            this_path = self.get_path_to_root(termid)
            ## In case of , or . or whatever, the path to the root usually is None, there are no dependencies...
            if shortest_path is None or (this_path is not None and len(this_path) < len(shortest_path)):
                shortest_path = this_path
        return shortest_path
        
    # Get all terms that are embedded under a given head (its dependents and dependents of its dependents
    def get_full_dependents(self, term_id, relations):
        """
        Returns the complete list of dependents and embedded dependents of a certain term.
        """
        relations = []
        deps = self.relations_for_term
        if term_id in deps and len(deps.get(term_id)) > 0:
            for dep in deps.get(term_id):
                if not dep[1] in relations:
                    relations.append(dep[1])
                    if dep[1] in deps:
                        dep_relations = self.get_full_dependents(dep[1], relations)
                        relations += dep_relations
        return relations



                
                           
            
       