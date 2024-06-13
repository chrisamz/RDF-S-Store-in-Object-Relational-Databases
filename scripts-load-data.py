# scripts/load_data.py

import argparse
import os
from backend.rdf_parser import RDFParser
from backend.db_connector import DBConnector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def parse_arguments():
    parser = argparse.ArgumentParser(description="Load RDF data into the database.")
    parser.add_argument('--rdf-file', type=str, required=True, help='Path to the RDF file.')
    parser.add_argument('--db-url', type=str, required=True, help='Database connection URL.')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Check if RDF file exists
    if not os.path.exists(args.rdf_file):
        raise FileNotFoundError(f"RDF file not found: {args.rdf_file}")

    # Initialize RDF Parser
    rdf_parser = RDFParser(args.rdf_file)
    rdf_data = rdf_parser.parse()

    # Setup database connection
    engine = create_engine(args.db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Initialize DB Connector
    db_connector = DBConnector(engine)

    # Load RDF data into the database
    for table_name, table_data in rdf_data.items():
        schema = {
            "table_name": table_name,
            "columns": table_data['columns']
        }
        db_connector.create_table(schema)
        data = {
            "table_name": table_name,
            "rows": table_data['rows']
        }
        db_connector.insert_data(data)

    # Commit and close session
    session.commit()
    session.close()

    print("Data loaded successfully.")

if __name__ == "__main__":
    main()
