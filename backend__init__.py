# backend/__init__.py

# Initialize the backend package

# Import the modules for easy access
from .rdf_parser import RDFParser
from .mapper import RDFMapper
from .db_connector import DBConnector
from .query_interface import QueryInterface

__all__ = ['RDFParser', 'RDFMapper', 'DBConnector', 'QueryInterface']
