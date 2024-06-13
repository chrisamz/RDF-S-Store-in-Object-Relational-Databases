# backend/mapper.py

import rdflib
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RDFMapper:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()

    def create_tables(self):
        class RDFSubject(Base):
            __tablename__ = 'rdf_subjects'
            id = Column(Integer, primary_key=True)
            uri = Column(String, unique=True)

        class RDFPredicate(Base):
            __tablename__ = 'rdf_predicates'
            id = Column(Integer, primary_key=True)
            uri = Column(String, unique=True)

        class RDFObject(Base):
            __tablename__ = 'rdf_objects'
            id = Column(Integer, primary_key=True)
            uri = Column(String, unique=True)

        class RDFTriple(Base):
            __tablename__ = 'rdf_triples'
            id = Column(Integer, primary_key=True)
            subject_id = Column(Integer, ForeignKey('rdf_subjects.id'))
            predicate_id = Column(Integer, ForeignKey('rdf_predicates.id'))
            object_id = Column(Integer, ForeignKey('rdf_objects.id'))

            subject = relationship("RDFSubject")
            predicate = relationship("RDFPredicate")
            object = relationship("RDFObject")

        Base.metadata.create_all(self.engine)

    def map_rdf_to_db(self, rdf_graph):
        session = self.Session()

        try:
            for subj, pred, obj in rdf_graph:
                subject = session.query(RDFSubject).filter_by(uri=str(subj)).first()
                if not subject:
                    subject = RDFSubject(uri=str(subj))
                    session.add(subject)
                    session.commit()

                predicate = session.query(RDFPredicate).filter_by(uri=str(pred)).first()
                if not predicate:
                    predicate = RDFPredicate(uri=str(pred))
                    session.add(predicate)
                    session.commit()

                object_ = session.query(RDFObject).filter_by(uri=str(obj)).first()
                if not object_:
                    object_ = RDFObject(uri=str(obj))
                    session.add(object_)
                    session.commit()

                triple = RDFTriple(subject_id=subject.id, predicate_id=predicate.id, object_id=object_.id)
                session.add(triple)

            session.commit()
            print("RDF data mapped to database successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error mapping RDF data to database: {e}")
        finally:
            session.close()

    def query_db(self, subject=None, predicate=None, object_=None):
        session = self.Session()
        query = session.query(RDFTriple)

        if subject:
            query = query.join(RDFSubject).filter(RDFSubject.uri == subject)
        if predicate:
            query = query.join(RDFPredicate).filter(RDFPredicate.uri == predicate)
        if object_:
            query = query.join(RDFObject).filter(RDFObject.uri == object_)

        results = query.all()
        session.close()
        return results

# Example usage
if __name__ == "__main__":
    db_url = 'sqlite:///rdf_store.db'
    mapper = RDFMapper(db_url)
    mapper.create_tables()

    # Assuming you have a parsed RDF graph from RDFParser
    rdf_parser = RDFParser()
    rdf_graph = rdf_parser.parse("""
    @prefix ex: <http://example.org/> .
    ex:subject ex:predicate ex:object .
    """, format='turtle')

    mapper.map_rdf_to_db(rdf_graph)

    results = mapper.query_db(subject="http://example.org/subject")
    for result in results:
        print(result)
