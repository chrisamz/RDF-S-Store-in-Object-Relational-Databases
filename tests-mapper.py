# tests/test_mapper.py

import pytest
from backend.mapper import RDFMapper

@pytest.fixture
def sample_parsed_data():
    return {
        "ex:thing1": {
            "type": "ex:Class1",
            "properties": {
                "ex:property1": "A property",
                "ex:property2": "Another property"
            }
        }
    }

@pytest.fixture
def sample_mapping_rules():
    return {
        "ex:Class1": {
            "table": "class1_table",
            "properties": {
                "ex:property1": "property1_column",
                "ex:property2": "property2_column"
            }
        }
    }

def test_mapper_initialization():
    mapper = RDFMapper()
    assert mapper is not None, "RDFMapper instance should be created"

def test_mapper_map(sample_parsed_data, sample_mapping_rules):
    mapper = RDFMapper(sample_mapping_rules)
    mapped_data = mapper.map(sample_parsed_data)
    assert mapped_data is not None, "Mapped data should not be None"
    assert isinstance(mapped_data, dict), "Mapped data should be a dictionary"
    assert 'class1_table' in mapped_data, "Mapped data should contain 'class1_table'"
    assert mapped_data['class1_table']['property1_column'] == 'A property', "'property1_column' should be 'A property'"
    assert mapped_data['class1_table']['property2_column'] == 'Another property', "'property2_column' should be 'Another property'"

def test_mapper_invalid_data():
    mapper = RDFMapper()
    with pytest.raises(ValueError):
        mapper.map(None)

def test_mapper_missing_rules(sample_parsed_data):
    mapper = RDFMapper()
    with pytest.raises(KeyError):
        mapper.map(sample_parsed_data)
