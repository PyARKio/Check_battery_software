# -- coding: utf-8 --
from __future__ import unicode_literals
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


engine = create_engine("sqlite:///some.db")

Base = declarative_base()
session = scoped_session(sessionmaker(class_=, autocommit=False))
Base.query = session.query_property()


# # Session = sessionmaker(bind=engine)
#
# engine.execute("""
#     create table employee (
#         emp_id integer primary key,
#         emp_name varchar
#     )
# """)
#
# engine.execute("""
#     create table employee_of_month (
#         emp_id integer primary key,
#         emp_name varchar
#     )
# """)
#
# engine.execute("""insert into employee(emp_name) values ('ed')""")
# engine.execute("""insert into employee(emp_name) values ('jack')""")
# engine.execute("""insert into employee(emp_name) values ('fred')""")


# from sqlalchemy import create_engine
# from sqlalchemy import MetaData
# from sqlalchemy import Table
# from sqlalchemy import Column
# from sqlalchemy import Integer, String
#
# db_uri = 'sqlite:///db.sqlite'
# engine = create_engine(db_uri)
#
# # Create a metadata instance
# metadata = MetaData(engine)
# # Declare a table
# table = Table('Example', metadata,
#               Column('id', Integer, primary_key=True),
#               Column('name', String))
# # Create all tables
# metadata.create_all()
# for _t in metadata.tables:
#     print("Table: ", _t)



