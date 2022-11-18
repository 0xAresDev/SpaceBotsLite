from sqlalchemy import Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime, desc, asc
import pathlib
import os
import datetime


# Run this file to create the DB and the tables...

#SQLALCHEMY_DATABASE_URI = "sqlite:///PriceData.db"
directory_for_db = pathlib.Path(__file__).parent.resolve()
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(directory_for_db, 'PriceData.db')}"

Base = declarative_base()

class Price(Base):
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    price = Column(Float)
    time = Column(DateTime)

    def __repr__(self):
        return f'Time: {self.time} Price: {self.price}'
    

    @classmethod
    def get_last_x_prices(cls, session, x):
        return session.query(cls).order_by(desc(cls.time)).limit(x).all()
    


def initialize_db(test=False):
    engine = None
    if test:
            engine = create_engine(SQLALCHEMY_DATABASE_URI+"_test", echo=True)
    else:
        engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    session.commit()
    session.close()

if __name__ == "__main__":
    initialize_db()