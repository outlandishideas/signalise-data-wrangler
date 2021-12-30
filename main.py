from dotenv import load_dotenv
from datetime import datetime

from src.collectors.GsuiteCollector import GsuiteCollector
from src.collectors.MondayCollector import MondayCollector
from src.util import create_reporting_views, get_reporting_db_engine, prepare_db_for_collection
from src.workers.ExportCCGPerformanceReportWorker import ExportCCGPerformanceReportWorker


if __name__ == '__main__':
    print("Starting")
    load_dotenv()
    db = get_reporting_db_engine()
    prepare_db_for_collection(db)
    # gsuite = GsuiteCollector(db)
    # gsuite.collect()
    monday = MondayCollector(db)
    monday.collect()
    create_reporting_views(db)

    worker = ExportCCGPerformanceReportWorker(db)
    worker.this_month()

    # if its the first day of the month get the last day.
    if datetime.now().day == 1:
        worker.last_month()

    # worker.start = datetime(2021,10,1)
    # worker.end = datetime(2021,10,31)

    worker.do_all_work()

    # print(db.execute("SELECT * from reporting.events_by_attendee limit 10").fetchall())