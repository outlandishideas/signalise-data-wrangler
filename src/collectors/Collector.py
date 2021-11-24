import abc
import re
from abc import ABC

import pandas as pd
from pandas.core.dtypes.common import is_datetime64_any_dtype
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.engine.reflection import Inspector

from src.util import clean_column_name


class Collector(ABC):
    """A Base class for Collectors which fetch data from an API, external db, etc. and save it into a common reporting data warehouse"""
    _db_engine: Engine
    _db_inspector: Inspector
    db: Connection
    params = []

    def __init__(self, db: Engine, params: list = []) -> None:
        self._db_engine = db
        self.db = db.connect()
        self._db_inspector = inspect(db)
        self.params = params
        if type(db) is not Engine:
            raise TypeError("db must be Engine")

    @property
    @abc.abstractmethod
    def schema_name(self):
        pass

    @abc.abstractmethod
    def collect(self):
        """Do the fetching of data and saving it to the db"""
        pass

    def save_dataframe(self, dataframe: pd.DataFrame, table_name: str, dtypes: dict = {}) -> None:
        schema_name = None
        if self._db_engine.name == 'postgresql':
            """if it's sqlite for testing we don't want a schema, but otherwise we want each collector in a named 
            schema """
            self.db.execute(f"CREATE SCHEMA IF NOT EXISTS {self.schema_name}")
            schema_name = self.schema_name

        dataframe.columns = [clean_column_name(column_name) for column_name in dataframe.columns]

        type_convert = {}
        dataframe = dataframe.convert_dtypes()
        for column_name, column_type in dataframe.dtypes.items():
            if column_name in dtypes.keys():
                type_convert[column_name] = dtypes[column_name]
            elif column_type == 'object':
                type_convert[column_name] = JSONB
            elif column_type == 'string':
                try:
                    dataframe[column_name] = pd.to_datetime(dataframe[column_name])
                    type_convert[column_name] = TIMESTAMP
                except:
                    pass  # its not a datetime column

        dataframe.to_sql(name=table_name, con=self.db, if_exists='replace', dtype=type_convert, schema=schema_name)


if __name__ == "__main__":
    """ Some basic tests """
    from sqlalchemy import create_engine

    db = create_engine("sqlite:///")
    test_dataframe = pd.DataFrame.from_records([{'a.Fat': 1, 'b': 2}, {'a.Fat': 3, 'b': 42}], index='b')
    test_dataframe_name = 'test_dataframe'


    class TestCollector(Collector):
        def schema_name(self):
            return 'test_schema'

        def collect(self):
            df = test_dataframe
            return self.save_dataframe(df, test_dataframe_name)


    collector = TestCollector(db)
    assert (collector.schema_name() == 'test_schema')
    collector.collect()
    out = pd.read_sql(f"select * from {clean_column_name(test_dataframe_name)}", db, index_col='b')
    print(out)

    # the Collector normalises the column names to make them easier to query
    test_dataframe.columns = [clean_column_name(column) for column in test_dataframe.columns]
    pd.testing.assert_frame_equal(test_dataframe, out)
