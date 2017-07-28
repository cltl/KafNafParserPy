from KafNafParserPy import KafNafParser

from nose.tools import assert_equal
from io import BytesIO


from KafNafParserPy.header_data import CHeader


def test_header():
    """
    Do the functions to set header attributes work correctly?

    Make sure the run with nosetests -s, otherwise python3 will err
    """

    naf = KafNafParser(type="NAF")
    naf.header = CHeader(type=naf.type)
    naf.root.insert(0, naf.header.get_node())

    naf.header.set_uri("http://example.com")
    assert_equal("http://example.com", naf.header.get_uri())
    naf.header.set_publicId("123")
    assert_equal("123", naf.header.get_publicId())

    # test if properties are serialized/deserialized correctly
    b = BytesIO()
    naf.dump(b)
    b.seek(0)
    naf2 = KafNafParser(b, type="NAF")
    assert_equal("http://example.com", naf2.header.get_uri())
    assert_equal("123", naf2.header.get_publicId())

