import math
from sqlalchemy import Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime, desc
import pathlib
import os
import datetime, time
from .InitializeDB import Price
import sched
import random
import matplotlib

eth = "0x0000000000000000000000000000000000000000"
dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F"

directory_for_db = pathlib.Path(__file__).parent.resolve()
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(directory_for_db, 'PriceData_generated.db')}"
base_price = 2000


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



def main(amount):
    now = datetime.datetime.now()
    current_price = base_price
    for i in range(amount):
        timestamp = now + datetime.timedelta(minutes=1)
        now = timestamp
        #print(current_price)
        price = get_next_price(current_price, i)
        current_price = price
        #print(price)
        add_to_db(price, timestamp)
        """if i % 100 == 0:
            print(price, timestamp)"""

    
    
def get_next_price(current, i):
    
    random_ = math.sin((i/100))
    print(current, random_-0.5)
    current = current + random_
    return current

def add_to_db(price, timestamp, test=False):
    engine=None
    if test:
        engine = create_engine(SQLALCHEMY_DATABASE_URI+"_test", echo=True)

    else:
        engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    exchange_rate = Price(price=price, time=timestamp, id=None)
    session.add(exchange_rate)
    session.commit()
    session.close()

# should give you x last data points back (sorted by date and time)
def read_data_from_db(x, test=False):
    engine=None
    if test:
        engine = create_engine(SQLALCHEMY_DATABASE_URI+"_test", echo=True)

    else:
        engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    price_data = [(x.price, x.time) for x in Price.get_last_x_prices(session, x)]
    session.close()
    return price_data

if __name__ == "__main__":
    initialize_db()
    main(10000)
    #print(read_data_from_db(10))