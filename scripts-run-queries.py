# scripts/run_queries.py

import argparse
from backend.db_connector import DBConnector
from backend.query_interface import QueryInterface
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run queries on the RDF data stored in the database.")
    parser.add_argument('--db-url', type=str, required=True, help='Database connection URL.')
    parser.add_argument('--query', type=str, required=True, help='SQL query to execute.')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Setup database connection
    engine = create_engine(args.db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Initialize DB Connector and Query Interface
    db_connector = DBConnector(engine)
    query_interface = QueryInterface(session)

    # Execute query
    results = query_interface.execute_query(args.query)

    # Print results
    for row in results:
        print(row)

    # Close session
    session.close()

if __name__ == "__main__":
    main()
