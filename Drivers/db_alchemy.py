# -- coding: utf-8 --
from __future__ import unicode_literals
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


# ******* POSTGRES ********
# db_url = {'drivername': 'postgres',
#           'database': 'data_db',
#           'username': 'postgres',
#           'password': 'superdyatel',
#           'host': 'localhost',
#           'port': 5432}
# engine = create_engine(URL(**db_url))

# ******* SQLite **********
# engine = create_engine("sqlite:///some.db")
engine = create_engine("sqlite:///d:\qua\Check_battery_software\Energizer CR2 1569313216.572497.db")

Base = declarative_base()


class TestTable(Base):
    __tablename__ = 'Test Table'
    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    val = Column(String)
    date = Column(DateTime, default=datetime.utcnow)


# class HeadData(Base):
#     __tablename__ = 'head_data'
#     battery_name = Column(String)
#     discharge_current = Column(Integer)
#     start_at_in_sec = Column(Integer)
#     start_at_in_date = Column(DateTime)


class BatteryData(Base):
    __tablename__ = 'battery_data'
    id = Column(Integer, primary_key=True)
    time_sec = Column(String)
    time_in_date = Column(String)
    volt = Column(Integer)


# create tables
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


data = {'a': 5566, 'b': 9527, 'c': 183}
try:
    for _key, _val in data.items():
        row = TestTable(key=_key, val=_val)
        session.add(row)
    session.commit()
except SQLAlchemyError as e:
    print(e)
# finally:
#     session.close()


try:
    # add row to database
    row = TestTable(key="hello", val="world")
    session.add(row)
    session.commit()

    # update row to database
    row = session.query(TestTable).filter(
          TestTable.key == 'hello').first()
    print('original:', row.key, row.val, row.id, row.date)
    row.key = "Hello"
    row.val = "World"
    session.commit()

    # check update correct
    row = session.query(TestTable).filter(
          TestTable.key == 'Hello').first()
    print('update:', row.key, row.val)

    row = session.query(TestTable).filter(
        TestTable.key == 'a').first()
    print('original:', row.key, row.val, row.id, row.date)

    # rows = session.query(TestTable).filter(
    #     TestTable.key == 'Hello').all()
    rows = session.query(TestTable).all()
    for row in rows:
        print('ALL:', row.key, row.val, row.id, row.date)

    rows = session.query(BatteryData).all()
    print(rows)
    for row in rows:
        print('ALL:', row.id, row.time_sec, row.time_in_date, row.volt)
except SQLAlchemyError as e:
    print(e)
finally:
    session.close()



