from operator import itemgetter
from VUA_pylib.common import get_max_distr_dict

class Cdependency_extractor:
    def __init__(self,knaf_obj):
        self.naf = knaf_obj
        self.relations_for_term = {}
        self.reverse_relations_for_term = {}
        self.prefix_for_reverse = ''
        
       
        for dep in knaf_obj.get_dependencies():
            term_from = dep.get_from()
            term_to = dep.get_to()
            rfunc = dep.get_function()
            

            
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
            sentence = token_obj.get_sent()
            
            self.sentence_for_termid[termid] = sentence
            ###########################################
            
            paths = self.__propagate_node(termid)
            inversed = self.__reverse_propagate_node(termid)
            
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

        
        
        
    def __propagate_node(self,node):
        paths = []
        relations = self.relations_for_term.get(node)
        if relations is None:   ##Case base
            paths = [[]] 

        else:    
            for func, target_node in relations:
                new_paths = self.__propagate_node(target_node)
                for new_path in new_paths:
                    new_path.insert(0,(func,target_node))
                    paths.append(new_path)
        return paths

    def __reverse_propagate_node(self,node):
        paths = []
        relations = self.reverse_relations_for_term.get(node)
        if relations is None:   ##Case base
            paths = [[]] 

        else:    
            for func, target_node in relations:
                new_paths = self.__reverse_propagate_node(target_node)
                for new_path in new_paths:
                    new_path.insert(0,(func,target_node))
                    paths.append(new_path)
        return paths        


    # Get the shortest path between 2 term ids
    def get_shortest_path(self,term1,term2):
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
                    idx1=ids1.index(term2)
                    hits.append((term2,idx1+0,idx1,0,num1,None))
                    #print 'Term2',term2,'found in one of the paths1'
                    
            for num2,p2 in enumerate(paths2):
                ids2 = [ my_id for my_func, my_id in p2]
                if term1 in p2:
                    idx2=ids2.index(term1)
                    hits.append((term1,0+idx2,0,idx2,None,num2))
                    #print 'Term1',term1,'found in one of the paths2'
            
            #Pair by pair
            for num1, p1 in enumerate(paths1):
                ids1 = [ my_id for my_func, my_id in p1]
                for num2, p2 in enumerate(paths2):
                    ids2 = [ my_id for my_func, my_id in p2]
                    common_ids = set(ids1) & set(ids2)
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
        shortest_path = None
        
        for term1 in span1:
            for term2 in span2:
                this_path = self.get_shortest_path(term1, term2)
                if shortest_path is None or (this_path is not None and len(this_path)<len(shortest_path)):
                    shortest_path = this_path
        return shortest_path
    
    # Get the dependency path to the sentence root for a term id
    def get_path_to_root(self,termid):
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
        shortest_path = None
        for termid in span:
            this_path = self.get_path_to_root(termid)
           
            ## In case of , or . or whatever, the path to the root usually is None, there are no dependencies...
            if shortest_path is None or (this_path is not None and len(this_path) < len(shortest_path)):
                shortest_path = this_path
        return shortest_path
        


                
                           
            
       