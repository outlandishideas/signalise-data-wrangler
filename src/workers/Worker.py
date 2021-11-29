import abc
from abc import ABC

from sqlalchemy import inspect
from sqlalchemy.engine import Engine


class Worker(ABC):

    def __init__(self, db: Engine = None):
        self.db = db.connect()
        self._db_engine = db
        self._db_inspector = inspect(db)

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def work(self, candidate):
        """Do whatever the work is for one candidate"""

    @abc.abstractmethod
    def find_candidates(self) -> list:
        """Find the candidates that need the work applying to them"""
        pass

    def do_all_work(self):
        """Find all the candidates and do the work to each of them"""
        candidates = self.find_candidates()
        for candidate in candidates:
            self.work(candidate)

if __name__ == "__main__":
    from sqlalchemy import  create_engine
    worker = Worker()
    worker.do_all_work()