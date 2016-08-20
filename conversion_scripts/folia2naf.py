#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function, unicode_literals, division, absolute_import

from KafNafParserPy import *
from pynlpl.formats import folia

import sys


#global dictionary that maps folia token ids to NAF term ids
fid2tid = {}


def header_to_header_layer(foliaObj, nafObj):
    '''
    :param foliaobj:
    :param nafobj:
    :return:
    '''
    myPublic = Cpublic()
    myPublic.set_publicid(foliaObj.id)

    if 'http' in foliaObj.id:
        myPublic.set_uri(foliaObj.id)

    myHeader = CHeader()
    myHeader.set_publicId(myPublic)
    nafObj.set_header(myHeader)

    # TODO: add annotation information (as linguistic processes)


def set_word_info(nafWord, word, offset):
    '''
    Adds all information that is deducted from the word form to the new token
    :param nafWord: Cwf() object for new NAF token
    :param word: FoLiA token
    :param offset: offset of word
    :return: offset updated with word length and space if applicable
    '''

    nafWord.set_offset(str(offset))
    text = word.text()
    wLength = len(text)
    nafWord.set_length(str(wLength))
    nafWord.set_text(text)
    offset += wLength
    if word.space:
        offset += 1

    return offset


def create_span(idList):
    '''
    Creates NAF span object pointing to ids in list
    :param idList: list of ids
    :return: span object
    '''
    my_span = Cspan()
    my_span.create_from_ids(idList)

    return my_span


def set_folia_info(folia_word, term):
    '''
    Retrieves information from folia_word and adds this to term
    :param folia_word: folia word object
    :param term: naf term object
    :return: None
    '''
    #FoLiA pos class is NAF morphofeat
    term.set_morphofeat(folia_word.pos())
    term.set_lemma(folia_word.lemma())
    #NAF pos tag corresponds to head (attribute's value) of pos element in FoLiA
    naf_pos = folia_word.xml().find('{http://ilk.uvt.nl/folia}pos').get('head')
    term.set_pos(naf_pos)


def get_and_add_term_information(folia_word, word_count):
    '''
    Retrieves term related information from folia word and adds a term
    :param foliaWord: FoLiA word obj
    :param nafObj: naf object to be updated
    :param word_count: count for term id/span
    :return: None
    '''
    global fid2tid
    naf_term = Cterm()
    # adding obligatory elements
    term_id = 't' + str(word_count)
    naf_term.set_id(term_id)
    fid2tid[folia_word.id] = term_id
    naf_span = create_span(['w' + str(word_count)])
    naf_term.set_span(naf_span)
    # add information from foliaWord
    set_folia_info(folia_word, naf_term)
    return naf_term

def text_to_text_layer(folia_obj, naf_obj):
    '''
    Goes through folia's text and adds all tokens to NAF token layer
    :param folia_obj: folia input object
    :param naf_obj: naf output object
    :return: None
    '''
    # FoLiA does not provide offset, length; setting it ourselves
    # More complex word ids, for now not taken over in NAF; flipping back and forth,
    # i.e. conversion to NAF will generate NAF ids, conversion to FoLiA will generate FoLiA ids
    offset = 0
    naf_sent = 0
    naf_para = 0
    word_count = 0
    for para in folia_obj.paragraphs():
        naf_para += 1
        for sent in para.sentences():
            sent_nr = str(naf_sent)
            for word in sent.words():
                naf_word = Cwf()
                offset = set_word_info(naf_word, word, offset)
                word_count += 1
                naf_word.set_id('w' + str(word_count))
                naf_word.set_sent(sent_nr)
                naf_word.set_para(str(naf_para))
                naf_obj.add_wf(naf_word)
                naf_term = get_and_add_term_information(word, word_count)
                naf_obj.add_term(naf_term)
            naf_sent += 1


def add_raw_from_text_layer(naf_obj):
    '''
    Goes through NAF's token layer and adds a raw layer based on its data.
    :param naf_obj: nafobject containing text layer
    :return: None
    '''
    raw = ''
    offset = 0
    paragraph = '1'
    for tok in naf_obj.get_tokens():
        # add space and update offset if there was a space
        if tok.get_offset() != str(offset):
            raw += ' '
            offset += 1
        # add double new line for now paragraph
        if tok.get_para() != paragraph:
            raw += '\n\n'
            paragraph = tok.get_para()
        token = tok.get_text()
        raw += token
        offset += len(token)
    naf_obj.set_raw(raw)


def create_span_from_folia_words(folia_word_list):
    '''
    Goes through list of folia words and identifies corresponding term id for each
    :param folia_word_list: list of FoLiA word objects
    :return: list of term ids
    '''

    global fid2tid
    naf_span = []
    for word in folia_word_list:
        naf_term_id = fid2tid.get(word.id)
        naf_span.append(naf_term_id)
    return naf_span


def add_span_to_elem(naf_elem, span_ids):
    '''
    Creates a NAF span object from a list of ids and adds this to the naf element
    :param naf_elem: a naf element
    :param span_ids: a list of ids that composes the span
    :return: None
    '''

    span = Cspan()
    span.create_from_ids(span_ids)
    naf_elem.set_span(span)

def chunking_to_chunks_layer(folia_obj, naf_obj):
    '''
    Extract chunks from FoLiA object and add to NAF's chunk layer
    :param folia_obj: folia object
    :param naf_obj: naf object
    :return: None
    '''
    chunk_id = 1
    for chunk in folia_obj.select(folia.Chunk):
        naf_chunk = Cchunk()
        naf_chunk.set_id('c' + str(chunk_id))
        chunk_id += 1
        naf_span = create_span_from_folia_words(chunk.wrefs())
        add_span_to_elem(naf_chunk, naf_span)
        naf_chunk.set_phrase(chunk.cls)
        #add phrase, head (when possible)
        if len(naf_span) == 1:
            naf_chunk.set_head(naf_span[0])
        naf_obj.add_chunk(naf_chunk)


def entities_to_entity_layer(folia_obj, naf_obj):
    '''
    Retrieves all entities from folia obj and adds them to naf entity layer
    :param folia_obj: folia object
    :param naf_obj: naf object
    :return: None
    '''
    entity_id = 1
    for entity in folia_obj.select(folia.Entity):
        naf_entity = Centity()
        naf_entity.set_id('e' + str(entity_id))
        entity_id += 1
        naf_span = create_span_from_folia_words(entity.wrefs())
        entity_references = Creferences()
        add_span_to_elem(entity_references, naf_span)
        naf_entity.add_reference(entity_references)
        naf_entity.set_type(entity.cls)
        naf_obj.add_entity(naf_entity)

def check_overall_info(folia_obj):
    '''
    :param folia_obj:
    :return:
    '''
    if folia_obj.version is None:
        print('[WARNING] FoLiA input did not have a version indicated.', file=sys.stderr)

        # print('Problems')


def convert_file_to_naf(inputfolia, outputnaf=None):
    '''
    :param inputfolia: file
    :return: None
    '''

    # if no output name provided, output name is original filename with .naf extension
    if outputnaf == None:
        outputnaf = "".join([inputfolia, '.naf'])

    folia_obj = folia.Document(file=inputfolia)
    check_overall_info(folia_obj)
    # check what information is present and print warnings if not all can be handled (yet)


    naf_obj = KafNafParser(type='NAF')
    text_to_text_layer(folia_obj, naf_obj)
    add_raw_from_text_layer(naf_obj)
    chunking_to_chunks_layer(folia_obj, naf_obj)
    entities_to_entity_layer(folia_obj, naf_obj)
    naf_obj.dump(outputnaf)

    header_to_header_layer(folia_obj, naf_obj)

def main(argv=None):
    # option to add: keep original identifiers...
    # option to add: language

    if argv == None:
        argv = sys.argv

    if len(argv) < 2:
        print('python folia2naf.py folia_input.xml (naf_output.xml)')
    elif len(argv) < 3:
        convert_file_to_naf(argv[1])
    else:
        convert_file_to_naf(argv[1], argv[2])


if __name__ == "__main__":
    main()
