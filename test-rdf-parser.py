# tests/test_rdf_parser.py

import pytest
from backend.rdf_parser import RDFParser

@pytest.fixture
def sample_rdf_data():
    return """
    @prefix ex: <http://example.org/stuff/1.0/> .
    ex:thing1 a ex:Class1 ;
              ex:property1 "A property" ;
              ex:property2 "Another property" .
    """

def test_rdf_parser_initialization():
    parser = RDFParser()
    assert parser is not None, "RDFParser instance should be created"

def test_rdf_parser_parse(sample_rdf_data):
    parser = RDFParser()
    parsed_data = parser.parse(sample_rdf_data)
    assert parsed_data is not None, "Parsed data should not be None"
    assert isinstance(parsed_data, dict), "Parsed data should be a dictionary"
    assert 'ex:thing1' in parsed_data, "Parsed data should contain 'ex:thing1'"
    assert parsed_data['ex:thing1']['type'] == 'ex:Class1', "'ex:thing1' should be of type 'ex:Class1'"
    assert parsed_data['ex:thing1']['properties']['ex:property1'] == 'A property', "'ex:property1' should be 'A property'"
    assert parsed_data['ex:thing1']['properties']['ex:property2'] == 'Another property', "'ex:property2' should be 'Another property'"

def test_rdf_parser_invalid_data():
    parser = RDFParser()
    with pytest.raises(ValueError):
        parser.parse("Invalid RDF data")

