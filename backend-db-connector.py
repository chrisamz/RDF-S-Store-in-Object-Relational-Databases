# backend/db_connector.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

class DBConnector:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def test_connection(self):
        try:
            connection = self.engine.connect()
            connection.close()
            print("Database connection successful.")
        except SQLAlchemyError as e:
            print(f"Database connection failed: {e}")

    def get_session(self):
        return self.Session()

# Example usage
if __name__ == "__main__":
    db_url = 'sqlite:///rdf_store.db'
    db_connector = DBConnector(db_url)
    db_connector.test_connection()

    # Get a session and perform a simple query to test
    session = db_connector.get_session()
    result = session.execute("SELECT 1")
    for row in result:
        print(row)
    session.close()
