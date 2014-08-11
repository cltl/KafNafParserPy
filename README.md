KafNafParserPy
==========

Description
----------
Parser for KAF or  NAF files in python. The documentation for all methods and API of this parser can be found at http://kyoto.let.vu.nl/~izquierdo/api/KafNafParserPy

Installation
-----------
Clone the repository from github

````shell
git clone git@github.com:cltl/NafParserPy.git
````
You will need to have installed the lxml library for python (http://lxml.de/)


You can add the directory of the package KafNafParserMod in
sys.path. or you can install the package with the setup.py script:

```
cd KafNafParserPy
./setup.py install
```

Usage
-----

This library is a python module, that reads a KAF or NAF file and parses it. Basically:
```shell
python
>>> from KafNafParserMod import KafNafParser
>>> kaf_parser = KafNafParser('my_file.kaf')
```

The these are the main methods of that can be applied to a KafNafParser object:
* get_type() --> whether is a KAF or NAF file
* to_kaf() --> converts the NAF file to KAF
* to_naf() --> converts the KAF file to NAF
* get_language() --> returns the language code of the file
* get_tokens() --> iterator that returns the tokens (Cwf object) of the file. Cwf:
  * get_id() --> returns the identifier
  * get_text() --> the text of the token
  * get_sent() --> the sentence
  * get_offset() --> the offset
* get_token(token_id) --> return the Ctoken object with that identifier
* get_terms() --> iterator taht returns the terms (Cterm object) of the file
* get_term(term_id) --> return the Cterm object with that term identifier
  * get_id()
  * get_lemma()
  * get_pos()
  * get_morphofeat()
  * get_span() --> returns the span of the term (Cspan object)
    * get_span_ids() --> list of identifiers of the span
  * get_sentiment() --> return the Csentiment object
    * get_polarity()
    * get_modifier()
* get_properties() --> iterator that returns the properties (Cproperty objects)
  * get_id()
  * get_type()
  * get_references() --> iterator of references, Creference object:
    * iterator --> returns list of Cspan objects
* get_entities() --> iterator taht returns the entities (Centity objects)
  * get_id()
  * get_type()
  * get_references() --> iterator of references
* get_opinions() --> returns the opinions (Copinion object)
  * get_id()
  * get_holder() --> Cholder object
    * get_span() --> span object
  * get_target() --> Ctarget object
    * get_span()
  * get_expression()
    * get_polarity()
    * get_strength()
    * get_span()
* get_predicates() --> returns the predicates (Cpredicate object)
  * get_id()
  * get_uri()
  * get_confidence()
  * get_span()
  * get_external_references() --> list of external references CexternalReference object
    * get_resource()
    * get_confidence()
    * get_reference()
  * get_roles() --> list of roles. Crole object:
    * get_id()
    * get_node()
    * get_sem_role()
    * get_external_references()
    * get_span()
* get_trees() --> returns the constituency trees (Ctree object)
  * get_non_terminals() --> non terminal nodes, Cnonterminal object
    * get_id()
    * get_label()
  * get_terminals() --> list of terminals. Cterminal object:
    * get_id()
    * get_span()
  * get_edges()
    * get_from()
    * get_to()
* get_dependencies() --> returns the dependencies (Cdep object)
  * get_from()
  * get_to()
  * get_function()
  
This is one example of usage:
```shell
python
>>> from KafNafParserPy import KafNafParser
>>> my_parser = KafNafParser('myfile.kaf')
>>> for token_obj in my_parser.get_tokens():
>>>     print 'Token id',token.get_id()
>>>     print 'Token text',token.get_text()
>>>
>>> for term_obj in my_parser.get_terms():
>>>    print 'Lemma',term_obj.get_lemma()
>>>    print 'Ids:',term_obj.get_span().get_span_ids()
>>>
>>> for prop in my_paser.get_properties():
>>>    print 'Id',prop.get_id()
>>>    for reference in prop.get_references():
>>>        for span_obj in reference: ##Iterator over Creference object
>>>            print 'span ids',span_obj.get_span_ids()
```


Documentation
-------------
The documentation can be generated automatically by running:
```shell
epydoc --config documentation.cfg
```

This will call to the external program epydoc (http://epydoc.sourceforge.net/) with the provided configuration file, and will create the HTML documents
for the API in the folder `apidocs`. As said before the already generated documentation can be seen at http://kyoto.let.vu.nl/~izquierdo/api/KafNafParserPy

Contact
------

* Ruben Izquierdo Bevia
* ruben.izquierdobevia@vu.nl
* Vrije University of Amsterdam

License
------
Sofware distributed under GPL.v3, see LICENSE file for details.
