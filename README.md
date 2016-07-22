KafNafParserPy
=============

Description
----------
Parser for KAF or  NAF files in python. The documentation for all methods and API of this parser can be found at:

1. HTML API: [http://kyoto.let.vu.nl/~izquierdo/documentation/KafNafParserPy/api](http://kyoto.let.vu.nl/~izquierdo/documentation/KafNafParserPy/api)
2. PDF API: [http://kyoto.let.vu.nl/~izquierdo/documentation/KafNafParserPy/api.pdf](http://kyoto.let.vu.nl/~izquierdo/documentation/KafNafParserPy/api.pdf)
3. Maintainer guide: [http://kyoto.let.vu.nl/~izquierdo/documentation/KafNafParserPy/kafnafparserpy-maintaining.pdf](http://kyoto.let.vu.nl/~izquierdo/documentation/KafNafParserPy/kafnafparserpy-maintaining.pdf)

You can also take a look at this [presentation](http://www.slideshare.net/rubenizquierdobevia/kafnafparserpy-a-python-library-for-parsingcreating-kaf-and-naf-files) on slideshare
 about this library.

Quick Installation
-----------------

The KafNafParserPy is from Feb 10th available in the [Python Package Index](https://pypi.python.org/pypi/KafNafParserPy), so you can easily install it (and its dependencies), by running:
````shell
pip install KafNafParserPy
````


Installation
-----------
Clone the repository from github

````shell
git clone https://github.com/cltl/KafNafParserPy.git
````
You will need to have installed the lxml library for python (http://lxml.de/). Usually just by running`pip install --user lxml` should be enough for
getting lxml installed. In some cases there can be problems with the libraries libxml and libxslt. In this case (considering you have no root access
for the machine), you can try to do the following:
```shell
wget http://xmlsoft.org/sources/libxml2-sources-2.7.7.tar.gz
gzip -dc libxml2-sources-2.7.7.tar.gz | tar xvf -
cd libxml2-2.7.7
./configure --prefix=/home/ruben/lib
make
make install
wget http://xmlsoft.org/sources/libxslt-1.1.26.tar.gz
gzip -dc libxslt-1.1.26.tar.gz | tar xvf -
cd libxslt-1.1.26
./configure --prefix=/home/ruben/lib --with-libxml-prefix=/home/ruben/lib
make
make install
PATH=$PATH:/home/ruben/lib/bin/
pip install --user lxml
```

Of course replace `/home/ruben/lib` by the folder where you want to install the libraries, and check the corresponding websites for newer versions
of the libraries.

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
* rubenizquierdobevia@gmail.com
* http://rubenizquierdobevia.com/
* Vrije University of Amsterdam

License
------
Sofware distributed under GPL.v3, see LICENSE file for details.
