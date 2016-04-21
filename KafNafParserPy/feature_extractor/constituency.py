#!/usr/bin/env python

"""
This module provides methods for extracting elaborated information from the constituency layer in a KAF/NAF file
"""
from __future__ import print_function

from operator import itemgetter
from collections import defaultdict

import copy

class Cconstituency_extractor:
    """
    This is the main class that allows the extraction of information
    """
    def __init__(self,knaf_obj):
        """
        Constructor from a KAfPArser object
        @type knaf_obj: KAfParser
        @param knaf_obj: the KAF/NAF object
        """
        self.naf = knaf_obj
        #Extract terminals, non terminals and edges
        ## Extracted directly from 
        self.terminals = {}          #terminal id --> list term ids
        self.terminal_for_term = {}  #term id --> terminal id
        self.label_for_nonter = {}   # nonter --> label
        self.reachable_from = {}     # node_from --> [nodeto1, nodeto2...]
        
        self.extract_info_from_naf(knaf_obj)
        
        #Extracting all posible paths from leave to root for each terminal id
        self.paths_for_terminal= {}
        for terminal_id in self.terminals.keys():
            paths = self.__expand_node(terminal_id,False)
            self.paths_for_terminal[terminal_id] = paths
        #######################################
        
        ## Create, for each non terminal, which are the terminals subsumed
        self.terms_subsumed_by_nonter = {}  ## ['nonter12'] = set('t1,'t2','t3','t4')
        for terminal_id, span_terms in self.terminals.items():
            for path in self.paths_for_terminal[terminal_id]:
                for nonter in path:
                    if nonter not in self.terms_subsumed_by_nonter:
                        self.terms_subsumed_by_nonter[nonter] = set()
                    for termid in span_terms:
                        self.terms_subsumed_by_nonter[nonter].add(termid)
        
        ## To print the paths calculated
#        for terminal in self.terminals.keys():
#            print terminal
#            for path in self.paths_for_terminal[terminal]:
#                sep=' '
#                for node in path:
#                    print sep,node,self.label_for_nonter.get(node,'?')
#                    sep+=' '
#            print '#'*20

               
    def get_deepest_phrases(self):
        all_nonter = set()
        for terminal in self.terminals.keys():
            for path in self.paths_for_terminal[terminal]:
                first_non_ter_phrase = path[1]
                subsumed = self.terms_subsumed_by_nonter[first_non_ter_phrase]
                this_type = self.label_for_nonter[first_non_ter_phrase]
                print(terminal, this_type, subsumed)
        return None
        
        ter_for_nonter = {}
        for nonter in all_nonter:
            for terminal in self.terminals.keys():
                for path in self.paths_for_terminal[terminal]:
                    if nonter in path:
                        if nonter in ter_for_nonter:
                            ter_for_nonter[nonter].append(terminal)
                        else:
                            ter_for_nonter[nonter] = [terminal]
        
        visited = set()
        for nonter, list_term in ter_for_nonter.items():
            for ter in list_term:
                print(ter)
                visited.add(ter)
    
    
    ### Returns the label of the deepest phrase for the term id (termid as in the term layer)
    def get_deepest_phrase_for_termid(self,termid):
        """
        Returns the deepest phrase type for the term identifier and the list of subsumed by the same element
        @type termid: string
        @param termid: term identifier
        @rtype: (string,list)
        @return: the label and list of terms subsumed
        """
        terminal_id = self.terminal_for_term.get(termid)
        label = None
        subsumed = []
        if terminal_id is not None:
            first_path = self.paths_for_terminal[terminal_id][0]
            first_phrase_id = first_path[1]
            label = self.label_for_nonter.get(first_phrase_id)
            subsumed = self.terms_subsumed_by_nonter.get(first_phrase_id,[])
        return label,sorted(list(subsumed))
    
    
    def get_least_common_subsumer(self,from_tid,to_tid):
        """
        Returns the deepest common subsumer among two terms
        @type from_tid: string
        @param from_tid: one term id
        @type to_tid: string
        @param to_tid: another term id
        @rtype: string
        @return: the term identifier of the common subsumer
        """
        termid_from = self.terminal_for_term.get(from_tid)
        termid_to = self.terminal_for_term.get(to_tid)
        
        path_from = self.paths_for_terminal[termid_from][0]
        path_to = self.paths_for_terminal[termid_to][0]
        common_nodes = set(path_from) & set(path_to)
        if len(common_nodes) == 0:
            return None
        else:
            indexes = []
            for common_node in common_nodes:
                index1 = path_from.index(common_node)
                index2 = path_to.index(common_node)
                indexes.append((common_node,index1+index2))
            indexes.sort(key=itemgetter(1))
            shortest_common = indexes[0][0]
            return shortest_common
        
    
    def get_path_from_to(self,from_tid, to_tid):
        """
        This function returns the path (in terms of phrase types) from one term to another
        @type from_tid: string
        @param from_tid: one term id
        @type to_tid: string
        @param to_tid: another term id
        @rtype: list
        @return: the path, list of phrase types     
        """
        shortest_subsumer = self.get_least_common_subsumer(from_tid, to_tid)
        
        #print 'From:',self.naf.get_term(from_tid).get_lemma()
        #print 'To:',self.naf.get_term(to_tid).get_lemma()
        termid_from = self.terminal_for_term.get(from_tid)
        termid_to = self.terminal_for_term.get(to_tid)
        
        path_from = self.paths_for_terminal[termid_from][0]
        path_to = self.paths_for_terminal[termid_to][0]
        
        if shortest_subsumer is None:
            return None
        
        complete_path = []
        for node in path_from:
            complete_path.append(node)
            if node == shortest_subsumer: break
        
        begin=False
        for node in path_to[-1::-1]:
            if begin:
                complete_path.append(node)
             
            if node==shortest_subsumer:
                begin=True
        labels = [self.label_for_nonter[nonter] for nonter in complete_path]
        return labels
                
            
    def get_path_for_termid(self,termid):
        """
        This function returns the path (in terms of phrase types) from one term the root
        @type termid: string
        @param termid: one term id
        @rtype: list
        @return: the path, list of phrase types     
        """
        terminal_id = self.terminal_for_term.get(termid)
        paths = self.paths_for_terminal[terminal_id]
        labels = [self.label_for_nonter[nonter] for nonter in paths[0]]
        return labels
        
    def extract_info_from_naf(self,knaf_obj):
        ## Generated internally
        # For each terminal node, a list of paths through all the edges
        self.paths_for_terminal = {} 
        for tree in knaf_obj.get_trees():
            for terminal in tree.get_terminals():
                ter_id = terminal.get_id()
                span_ids = terminal.get_span().get_span_ids()
                self.terminals[ter_id] = span_ids
                for this_id in span_ids:
                    self.terminal_for_term[this_id] = ter_id
            
            
            for non_terminal in tree.get_non_terminals():
                nonter_id = non_terminal.get_id()
                label = non_terminal.get_label()
                self.label_for_nonter[nonter_id] = label
                
                
            for edge in tree.get_edges():
                node_from = edge.get_from()
                node_to = edge.get_to()
                if node_from not in self.reachable_from:
                    self.reachable_from[node_from] = [node_to]
                else:
                    self.reachable_from[node_from].append(node_to)
        
     
        
    def get_deepest_subsumer(self,list_terms):
        '''
        Returns the labels of the deepest node that subsumes all the terms in the list of terms id's provided
        '''
        
        #To store with how many terms every nonterminal appears
        count_per_no_terminal = defaultdict(int)
        
        #To store the total deep of each noter for all the term ides (as we want the deepest)
        total_deep_per_no_terminal = defaultdict(int)
        for term_id in list_terms:
            terminal_id = self.terminal_for_term.get(term_id)
            path = self.paths_for_terminal[terminal_id][0]
            print(term_id, path)
            for c,noter in enumerate(path):
                count_per_no_terminal[noter] += 1
                total_deep_per_no_terminal[noter] += c
                
                
        deepest_and_common = None
        deepest = 10000
        for noterid, this_total in total_deep_per_no_terminal.items():
            if count_per_no_terminal.get(noterid,-1) == len(list_terms):    ##Only the nontarms that ocurr with all the term ids in the input
                if this_total < deepest:
                    deepest = this_total
                    deepest_and_common = noterid
                    
        label = None
        if deepest_and_common is not None:
            label = self.label_for_nonter[deepest_and_common]
        return deepest_and_common, label 
        #return label 
    
    
    ##Recursive function
    ## Propagates the node through all the relations extracte from the edges information
    ## It returns a list of lists, one for each path
    ## Include_this_node is used for avoiding the first node 
    def __expand_node(self,node,include_this_node=True):
        paths = []
        possible_nodes = self.reachable_from.get(node,[])
        if len(possible_nodes) == 0:
            return [[node]]
        else:
            for possible_node in possible_nodes:
                new_paths = self.__expand_node(possible_node)
                for path in new_paths:
                    if include_this_node: 
                        path.insert(0,node)
                    paths.append(path)
            return paths
       
    def get_chunks(self,chunk_type):
        """
        Returns the chunks for a certain type
        @type chunk_type: string
        @param chunk_type: type of the chunk
        @rtype: list
        @return: the chunks for that type
        """
        for nonter,this_type in self.label_for_nonter.items():
            if this_type == chunk_type:
                subsumed = self.terms_subsumed_by_nonter.get(nonter)
                if subsumed is not None:
                    yield sorted(list(subsumed))
    
          
    
    
    def get_all_deepest_chunks(self):
        all_chunks = []
        n=0
        for nonter,this_type in self.label_for_nonter.items():
            subsumed = self.terms_subsumed_by_nonter.get(nonter)
            print(nonter, this_type, subsumed)
            continue
            if subsumed is not None:
                if len(subsumed) > 1:
                    all_chunks.append(('chunk_%d' % n, this_type,subsumed))
                else:
                    tid = self.terminal_for_term.get(list(subsumed)[0])
                    reachable = self.reachable_from[tid]
                    if reachable[0] != nonter:
                        all_chunks.append(('chunk_%d' % n, this_type,subsumed))
 
 
 
        while True:
            ids_to_be_removed = set()
            for id1, type1, span1 in all_chunks:
                #We fixed id1
                for id2, type2, span2 in all_chunks:
                    if id1 != id2:
                        #If id2 subsumes id1 is a candidate to be removed
                        if len(span2) > len(span1):
                            common = span1 & span2
                            if len(common) == len(span1):
                                ids_to_be_removed.add(id2)
            
            filtered_chunks = []
            for this_id, this_type, this_span in all_chunks:
                if this_id not in ids_to_be_removed:
                    filtered_chunks.append((this_id, this_type, this_span))
        
            del all_chunks
            all_chunks = copy.copy(filtered_chunks)
            if len(ids_to_be_removed) == 0:
                break
            
        for this_id, this_type, this_span in all_chunks:
            yield this_type, this_span
                            
                    
    def get_all_chunks_for_term(self,termid):
        """
        Returns all the chunks in which the term is contained
        @type termid: string
        @param termid: the term identifier
        @rtype: list
        @return: list of chunks
        """
        terminal_id = self.terminal_for_term.get(termid)
        paths = self.paths_for_terminal[terminal_id]
        for path in paths:
            for node in path:
                this_type = self.label_for_nonter[node]
                subsumed =  self.terms_subsumed_by_nonter.get(node)
                if subsumed is not None:
                    yield this_type,sorted(list(subsumed))
        
