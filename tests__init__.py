# tests/__init__.py

"""
This module contains unit tests for the RDF(S) Store in Object-Relational Databases project.

The tests ensure that each component of the system functions as expected:
- RDF Parser: Parsing RDF(S) data and converting it into a suitable format for storage.
- Mapper: Mapping RDF(S) data to the object-relational database schema.
- DB Connector: Connecting to the database and providing session management.
- Query Interface: Executing queries, inserting, updating, and deleting data.

To run the tests, use a test runner such as pytest:
    $ pytest tests/

"""

import os
import sys
import pytest

# Add the backend module to the sys.path to allow importing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

@pytest.fixture(scope='module')
def db_connector():
    from backend.db_connector import DBConnector
    db_url = 'sqlite:///test_rdf_store.db'
    connector = DBConnector(db_url)
    yield connector
    # Teardown: clean up the database after tests
    connector.engine.dispose()

@pytest.fixture(scope='module')
def query_interface(db_connector):
    from backend.query_interface import QueryInterface
    return QueryInterface(db_connector)
