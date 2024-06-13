# backend/query_interface.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

class QueryInterface:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        self.session = self.db_connector.get_session()

    def execute_query(self, query):
        try:
            result = self.session.execute(query)
            return result.fetchall()
        except SQLAlchemyError as e:
            print(f"Query execution failed: {e}")
            return None

    def insert_data(self, table, data):
        try:
            self.session.execute(table.insert(), data)
            self.session.commit()
            print("Data insertion successful.")
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Data insertion failed: {e}")

    def fetch_data(self, table, conditions=None):
        try:
            if conditions:
                result = self.session.query(table).filter_by(**conditions).all()
            else:
                result = self.session.query(table).all()
            return result
        except SQLAlchemyError as e:
            print(f"Data fetch failed: {e}")
            return None

    def update_data(self, table, conditions, new_data):
        try:
            self.session.query(table).filter_by(**conditions).update(new_data)
            self.session.commit()
            print("Data update successful.")
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Data update failed: {e}")

    def delete_data(self, table, conditions):
        try:
            self.session.query(table).filter_by(**conditions).delete()
            self.session.commit()
            print("Data deletion successful.")
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Data deletion failed: {e}")

# Example usage
if __name__ == "__main__":
    from db_connector import DBConnector
    from sqlalchemy import Table, MetaData

    db_url = 'sqlite:///rdf_store.db'
    db_connector = DBConnector(db_url)
    query_interface = QueryInterface(db_connector)

    # Example table definition (assuming table already exists in database)
    metadata = MetaData()
    example_table = Table('example_table', metadata, autoload_with=db_connector.engine)

    # Example data insertion
    data = [{'column1': 'value1', 'column2': 'value2'}, {'column1': 'value3', 'column2': 'value4'}]
    query_interface.insert_data(example_table, data)

    # Example data fetch
    fetched_data = query_interface.fetch_data(example_table)
    print(fetched_data)

    # Example data update
    conditions = {'column1': 'value1'}
    new_data = {'column2': 'new_value'}
    query_interface.update_data(example_table, conditions, new_data)

    # Example data deletion
    delete_conditions = {'column1': 'value3'}
    query_interface.delete_data(example_table, delete_conditions)
