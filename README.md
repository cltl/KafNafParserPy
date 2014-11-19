KafNafParserPy
=============

Description
----------
Parser for KAF or  NAF files in python. The documentation for all methods and API of this parser can be found at:

1. HTML: [http://kyoto.let.vu.nl/~izquierdo/api/KafNafParserPy](http://kyoto.let.vu.nl/~izquierdo/api/KafNafParserPy)
2. PDF: [http://kyoto.let.vu.nl/~izquierdo/api/KafNafParserPy/api.pdf](http://kyoto.let.vu.nl/~izquierdo/api/KafNafParserPy/api.pdf)

You can also take a look at this [presentation](http://www.slideshare.net/rubenizquierdobevia/kafnafparserpy-a-python-library-for-parsingcreating-kaf-and-naf-files) on slideshare
 about this library.

Installation
-----------
Clone the repository from github

````shell
git clone https://github.com/cltl/KafNafParserPy.git
````
You will need to have installed the lxml library for python (http://lxml.de/)

Usage
-----

This library is a python module, that reads a KAF or NAF file and parses it. It basically parses one KAF/NAF file
and allows to access to all the layers through different methods and functions. This is one example of usage:
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

You can find some examples of usage of this parser in the subfolder `examples`.

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
* http://rubenizquierdobevia.com/
* Vrije University of Amsterdam

License
------
Sofware distributed under GPL.v3, see LICENSE file for details.
