# tests/test_query_interface.py

import pytest
from backend.query_interface import QueryInterface
from backend.db_connector import DBConnector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="module")
def test_engine():
    engine = create_engine('sqlite:///:memory:')  # In-memory SQLite database for testing
    yield engine
    engine.dispose()

@pytest.fixture(scope="module")
def test_session(test_engine):
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def db_connector(test_engine):
    return DBConnector(test_engine)

@pytest.fixture
def query_interface(db_connector):
    return QueryInterface(db_connector)

def test_query_interface_initialization(query_interface):
    assert query_interface is not None, "QueryInterface instance should be created"
    assert query_interface.db_connector is not None, "QueryInterface should have a DBConnector instance"

def test_query_interface_create_and_query_table(query_interface):
    schema = {
        "table_name": "test_table",
        "columns": {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "value": "REAL"
        }
    }
    query_interface.db_connector.create_table(schema)

    data = {
        "table_name": "test_table",
        "rows": [
            {"id": 1, "name": "Sample", "value": 123.45}
        ]
    }
    query_interface.db_connector.insert_data(data)

    query = "SELECT * FROM test_table WHERE name = 'Sample'"
    result = query_interface.execute_query(query)

    assert len(result) == 1, "Query should return one row"
    assert result[0]["id"] == 1, "The id of the row should be 1"
    assert result[0]["name"] == "Sample", "The name of the row should be 'Sample'"
    assert result[0]["value"] == 123.45, "The value of the row should be 123.45"

def test_query_interface_insert_and_query_data(query_interface):
    schema = {
        "table_name": "test_table",
        "columns": {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "value": "REAL"
        }
    }
    query_interface.db_connector.create_table(schema)

    data = {
        "table_name": "test_table",
        "rows": [
            {"id": 2, "name": "Example", "value": 678.90}
        ]
    }
    query_interface.db_connector.insert_data(data)

    query = "SELECT * FROM test_table WHERE name = 'Example'"
    result = query_interface.execute_query(query)

    assert len(result) == 1, "Query should return one row"
    assert result[0]["id"] == 2, "The id of the row should be 2"
    assert result[0]["name"] == "Example", "The name of the row should be 'Example'"
    assert result[0]["value"] == 678.90, "The value of the row should be 678.90"
