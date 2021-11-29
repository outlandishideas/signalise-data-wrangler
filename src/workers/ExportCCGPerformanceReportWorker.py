import pandas as pd

from src.util import get_reporting_db_engine
from src.workers.Worker import Worker


class ExportCCGPerformanceReportWorker(Worker):

    @property
    def name(self):
        return "ExportCCGPerformanceReportWorker"

    def find_candidates(self):
        q = "SELECT * from reporting.ccg_performance_reporting_booking_pipeline_2020_21"
        legacy = pd.read_sql(q, self.db)

        q = "SELECT * from reporting.ccg_performance_reporting_booking_pipeline_2020_21"
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
