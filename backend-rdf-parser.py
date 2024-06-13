# backend/rdf_parser.py

import rdflib

class RDFParser:
    def __init__(self):
        self.graph = rdflib.Graph()

    def parse(self, rdf_data, format='xml'):
        """
        Parses the given RDF data.

        Parameters:
        rdf_data (str): The RDF data to parse.
        format (str): The format of the RDF data (e.g., 'xml', 'turtle').

        Returns:
        rdflib.Graph: The parsed RDF graph.
        """
        try:
            self.graph.parse(data=rdf_data, format=format)
            print("RDF data parsed successfully.")
        except Exception as e:
            print(f"Error parsing RDF data: {e}")
        
        return self.graph

    def load_from_file(self, file_path, format='xml'):
        """
        Loads RDF data from a file and parses it.

        Parameters:
        file_path (str): The path to the RDF file.
        format (str): The format of the RDF data in the file (e.g., 'xml', 'turtle').

        Returns:
        rdflib.Graph: The parsed RDF graph.
        """
        try:
            self.graph.parse(file_path, format=format)
            print(f"RDF data loaded and parsed from file {file_path} successfully.")
        except Exception as e:
            print(f"Error loading RDF data from file {file_path}: {e}")
        
        return self.graph

    def serialize(self, format='xml'):
        """
        Serializes the RDF graph to a string.

        Parameters:
        format (str): The format to serialize the RDF graph (e.g., 'xml', 'turtle').

        Returns:
        str: The serialized RDF graph.
        """
        try:
            rdf_serialized = self.graph.serialize(format=format)
            return rdf_serialized
        except Exception as e:
            print(f"Error serializing RDF graph: {e}")
            return None

    def get_graph(self):
        """
        Returns the current RDF graph.

        Returns:
        rdflib.Graph: The current RDF graph.
        """
        return self.graph
