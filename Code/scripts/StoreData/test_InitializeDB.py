import pytest
from InitializeDB import *
from os.path import exists

from sqlalchemy import Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime, desc
import pathlib
import os
import datetime



def test_initialize_db():
    initialize_db()
    assert exists(os.path.join(directory_for_db, 'PriceData.db')) == True
