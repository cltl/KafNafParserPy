from __future__ import unicode_literals, print_function

import sys
import os
import tempfile
from io import BytesIO
from contextlib import contextmanager

from nose.tools import assert_in

from KafNafParserPy import KafNafParser

@contextmanager
def capture_stdout(dest=None):
    """Capture stdout into dest"""
    if dest is None: dest = BytesIO()
    saved_stdout = sys.stdout
    sys.stdout = dest
    try:
        yield dest
    finally:
        sys.stdout = saved_stdout
        
def test_dump():
    """
    Can we use naf.dump() to stdout and file?

    Make sure the run with nosetests -s, otherwise python3 will err
    """

    naf = KafNafParser(type="NAF")
    token = naf.create_wf("\xd8lleg\xe5rd", 1, 1)
    expected = '<![CDATA[\xd8lleg\xe5rd]]></wf>'

    # do we get an error on dumping to stdout without redirect?
    naf.dump()
    
    # Can we dump to stdout?
    with capture_stdout() as s:
        naf.dump()
    output = s.getvalue().decode("utf-8")
    assert_in(expected, output)
    
    # Can we dump to a named file?
    f = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
    try:
        naf.dump(f.name)
        f.close()
        output = open(f.name, mode='rb').read().decode('utf-8')
    finally:
        os.remove(f.name)
    assert_in(expected, output)
        
if __name__=='__main__':
    test_dump()
