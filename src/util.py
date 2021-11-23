from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from re import sub


def get_reporting_db_engine():
    engine = create_engine(
        f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASS')}@{getenv('DB_HOST')}/{getenv('DB_NAME')}")
    return engine


def clean_column_name(column_name: str) -> str:
    return sub('[^a-zA-Z0-9]', '_', column_name).lower()


def prepare_db_for_collection(db: Engine):
    db.execute("DROP SCHEMA IF EXISTS reporting CASCADE")
    db.execute("CREATE SCHEMA reporting")


def create_reporting_views(db: Engine):
    sql_files = (Path(__file__).parent / 'reporting_views').glob('*.sql')
    for path in sql_files:
        db.execute(path.read_text())


if __name__ == '__main__':
    load_dotenv()
    create_reporting_views(get_reporting_db_engine())
