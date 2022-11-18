from sqlalchemy import Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime, desc
import pathlib
import os
import datetime, time
from InitializeDB import Price, SQLALCHEMY_DATABASE_URI, initialize_db
from main import add_to_db, read_data_from_db, delete_old, get_total_price_count



def test_add_to_db():
    initialize_db(test=True)
    add_to_db(10.0, datetime.datetime.now(), test=True)
    
    engine = create_engine(SQLALCHEMY_DATABASE_URI+"_test", echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    #Base.metadata.create_all(engine)

    price = session.get(Price, 1)
    #session.expunge_all()
    #session.commit()
    assert price.price == 10

    session.close()
    #time.sleep(1)
    os.remove(SQLALCHEMY_DATABASE_URI[10:]+"_test")


def test_read_data_from_db():
    initialize_db(test=True)
    for i in range(10):
        add_to_db(10.0, datetime.datetime.now(), test=True)
    
    data = read_data_from_db(6, test=True)

    assert len(data) == 6 and data[0] != None


    #time.sleep(1)
    os.remove(SQLALCHEMY_DATABASE_URI[10:]+"_test")

