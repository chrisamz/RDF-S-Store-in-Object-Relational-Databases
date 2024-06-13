# tests/test_db_connector.py

import pytest
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

def test_db_connector_initialization(db_connector):
    assert db_connector is not None, "DBConnector instance should be created"
    assert db_connector.engine is not None, "DBConnector should have an engine"

def test_db_connector_create_table(db_connector):
    schema = {
        "table_name": "test_table",
        "columns": {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "value": "REAL"
        }
    }
    db_connector.create_table(schema)
    tables = db_connector.engine.table_names()
    assert "test_table" in tables, "test_table should be created in the database"

def test_db_connector_insert_data(db_connector):
    schema = {
        "table_name": "test_table",
        "columns": {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "value": "REAL"
        }
    }
    db_connector.create_table(schema)

    data = {
        "table_name": "test_table",
        "rows": [
            {"id": 1, "name": "Sample", "value": 123.45}
        ]
    }
    db_connector.insert_data(data)

    result = db_connector.engine.execute("SELECT * FROM test_table").fetchall()
    assert len(result) == 1, "There should be one row in test_table"
    assert result[0]["id"] == 1, "The id of the row should be 1"
    assert result[0]["name"] == "Sample", "The name of the row should be 'Sample'"
    assert result[0]["value"] == 123.45, "The value of the row should be 123.45"

def test_db_connector_query_data(db_connector):
    schema = {
        "table_name": "test_table",
        "columns": {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "value": "REAL"
        }
    }
    db_connector.create_table(schema)

    data = {
        "table_name": "test_table",
        "rows": [
            {"id": 1, "name": "Sample", "value": 123.45}
        ]
    }
    db_connector.insert_data(data)

    query = "SELECT * FROM test_table WHERE name = 'Sample'"
    result = db_connector.query_data(query)

    assert len(result) == 1, "Query should return one row"
    assert result[0]["id"] == 1, "The id of the row should be 1"
    assert result[0]["name"] == "Sample", "The name of the row should be 'Sample'"
    assert result[0]["value"] == 123.45, "The value of the row should be 123.45"
