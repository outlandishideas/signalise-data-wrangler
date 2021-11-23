import os
from functools import cached_property
import pandas as pd
from dotenv import load_dotenv
from typing import List
from src.util import *

import requests
from moncli import client as MondayClient

from Collector import Collector

from icecream import ic

load_dotenv()

API_KEY = os.getenv('MONDAY_API_KEY')
API_URL = "https://api.monday.com/v2"
HEADERS = {"Authorization": API_KEY}

EXCLUDED_BOARD_IDS = [
    # '1922161518', #                          HR_TMP Clients
    # '1922060379', #              HR_TMP Invoices Receivable
    # '1915224762', #                 HR_TMP Invoices Payable
    # '1915136720', #                          HR_TMP Booking
    # '1915132511', #                          HR_TMP Enquiry
    '1858086349',  # Consent Form October 2021
    '1821249404',  # Subitems of Signalise Roadmap
    '1820193304',  # Signalise Roadmap
    '1714710739',  # TEST invoice board
    '1698629932',  # TEST of Booking Sales Pipeline 2020/21
    '1684090137',  # CCG Framework Locations
    '1671904866',  # Customer Feedback Survey
    '1649557653',  # Calls
    '1639560580',  # Booking Form 2020/21
    '1638387981',  # Deaf Users
    '1627893820',  # CCG Service Levels
    '1527500053',  # DOC Legal Interpreting
    '1509911608',  # DOC STTR Guidance
    # '1497624294', #          Booking Sales Pipeline 2020/21
    '1497319722',  # DOC Why 2 Interpreters are needed info
    '1482864083',  # Subitems of Finance Requests
    '1482864064',  # Finance Requests
    '1482849221',  # Communication Professional Contacts
    '1476461845',  # DOC Booking process v2 July 2021
    '1462823210',  # Weekly Rota Schedule
]


class MondayCollector(Collector):

    @cached_property
    def monday(self):
        MondayClient.api_key = os.getenv('MONDAY_API_KEY')
        return MondayClient

    @cached_property
    def boards(self):
        return self.monday.get_boards('id', 'name')

    def boards_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([dict(board) for board in self.boards]).set_index('id')[['name']]

    @cached_property
    def items_by_boards(self):
        boards = {}
        for board in self.boards:
            if board.id in EXCLUDED_BOARD_IDS:
                continue
            print(board.name)
            board_items = []
            board_items = []
            page = 1
            chunk_size = 15

            items = board.get_items(get_column_values=True, limit=chunk_size, page=page)
            while items:
                print("+", end='')
                board_items.append(items)
                page = page + 1
                items = board.get_items(get_column_values=True, limit=chunk_size, page=page)
            boards[board.id] = board_items
        return boards

    @property
    def schema_name(self):
        return "gsuite"

    def collect(self):
        boards = self.boards


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from os import getenv
    from dotenv import load_dotenv

    load_dotenv()

    db_engine = get_reporting_db_engine()
    prepare_db_for_collection(db_engine)
    collector = MondayCollector(db_engine)
    collector.collect()

    print(collector.items_by_boards)
