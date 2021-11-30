import pandas as pd

from src.util import get_reporting_db_engine
from src.workers.Worker import Worker
from datetime import timedelta


def get_sla_level(request_time, start_time):
    diff = start_time - request_time
    if diff < timedelta(minutes=5):
        return 1
    elif diff < timedelta(minutes=30):
        return 2
    elif diff < timedelta(minutes=60):
        return 3
    elif diff < timedelta(hours=24):
        return 4
    else:
        return 5


class ExportCCGPerformanceReportWorker(Worker):

    @property
    def name(self):
        return "ExportCCGPerformanceReportWorker"

    def find_candidates(self):
        q = "SELECT * FROM reporting.ccg_performance_reporting_booking_pipeline_2020_21_simple"

        legacy = pd.read_sql(q, self.db)
        legacy['sla_level'] = legacy.apply(lambda x: get_sla_level(x.request_datetime, x.booking_start_datetime), axis=1)

        q = "SELECT * FROM reporting.ccg_performance_reporting_booking_pipeline_2020_21"
        new_boards = pd.read_sql(q, self.db)

        all_bookings = pd.concat([legacy, new_boards])
        return [all_bookings]

    def work(self, candidate: pd.DataFrame):
        # this particular worker just has one candidate which takes the form of a dataframe
        # in future it might be one dataframe per customer or similar

        candidate.to_excel('performance.xlsx')


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    db_engine = get_reporting_db_engine()
    worker = ExportCCGPerformanceReportWorker(db_engine)
    worker.do_all_work()
