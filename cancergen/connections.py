#!/usr/bin/env python

from sqlalchemy import create_engine
from base import Base
from exceptions import NotConnectedToDatabase


class DatabaseConnection(object):
    """Base class for database connections"""

    def __init__(self, url):
        self.engine = create_engine(url)

    @property
    def session(self):
        try:
            self._session
        except AttributeError:
            raise NotConnectedToDatabase("Database connection needed. See cancergen.connect().")
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    def create_tables(self):
        """Creates all tables according to base"""
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        """Creates all tables according to base"""
        Base.metadata.drop_all(self.engine)


class MysqlConnection(DatabaseConnection):
    """Class for connecting to a MySQL database"""

    def __init__(self, host="localhost", user=None, password="",
                 database=None, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.url = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(
            **vars(self))
        super(MysqlConnection, self).__init__(self.url)


class SqliteConnection(DatabaseConnection):
    """Class for connecting to a SQLite database"""

    def __init__(self, filepath=""):
        self.filepath = filepath
        if self.filepath == "":
            self.url = "sqlite://"  # In-memory database
        else:
            self.url = "sqlite:///{filepath}".format(**vars(self))
        super(SqliteConnection, self).__init__(self.url)
