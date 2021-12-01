from dotenv import load_dotenv

from src.collectors.GsuiteCollector import GsuiteCollector
from src.collectors.MondayCollector import MondayCollector
from src.util import create_reporting_views, get_reporting_db_engine, prepare_db_for_collection

if __name__ == '__main__':
    load_dotenv()
    db = get_reporting_db_engine()
    prepare_db_for_collection(db)
    # gsuite = GsuiteCollector(db)
    # gsuite.collect()
    # monday = MondayCollector(db)
    # monday.collect()
    create_reporting_views(db)

    # print(db.execute("SELECT * from reporting.events_by_attendee limit 10").fetchall())