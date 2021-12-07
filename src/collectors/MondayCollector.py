import os
from functools import cached_property
from logging import exception

import pandas as pd
from dotenv import load_dotenv
from typing import List
from src.util import *

import requests
from moncli import client as MondayClient

from .Collector import Collector

from icecream import ic

load_dotenv()

API_KEY = os.getenv('MONDAY_API_KEY')
API_URL = "https://api.monday.com/v2"
HEADERS = {"Authorization": API_KEY}

EXCLUDED_BOARD_IDS = [
    # '1922161518',  # HR_TMP Clients
    # '1922060379',  # HR_TMP Invoices Receivable
    # '1915224762',  # HR_TMP Invoices Payable
    # '1915136720',  # HR_TMP Booking
    # '1915132511',  # HR_TMP Enquiry
    # '1497624294',  # Booking Sales Pipeline 2020/21
    # '1858086349',  # Consent Form October 2021
    # '1821249404',  # Subitems of Signalise Roadmap
    # '1820193304',  # Signalise Roadmap
    # '1714710739',  # TEST invoice board
    # '1698629932',  # TEST of Booking Sales Pipeline 2020/21
    # '1684090137',  # CCG Framework Locations
    # '1671904866',  # Customer Feedback Survey
    '1649557653',  # Calls
    # '1639560580',  # Booking Form 2020/21
    # '1638387981',  # Deaf Users
    # '1627893820',  # CCG Service Levels
    # '1527500053',  # DOC Legal Interpreting
    # '1509911608',  # DOC STTR Guidance
    # '1497319722',  # DOC Why 2 Interpreters are needed info
    # '1482864083',  # Subitems of Finance Requests
    # '1482864064',  # Finance Requests
    # '1482849221',  # Communication Professional Contacts
    # '1476461845',  # DOC Booking process v2 July 2021
    # '1462823210',  # Weekly Rota Schedule
]

BOARDS_TO_FETCH = [
    {'id': '1401246000', 'name': 'sales_contacts'},
    {'id': '1497624294', 'name': 'booking_sales_pipeline_2020_21'},
    {'id': '1684090137', 'name': 'ccg_framework_locations'},
    {'id': '1482849221', 'name': 'communication_professional_contacts'},
    {'id': '1915132511', 'name': 'hr_tmp_enquiry'},
    {'id': '1915136720', 'name': 'hr_tmp_booking'},
]

class MondayCollector(Collector):

    @cached_property
    def monday(self):
        MondayClient.api_key = os.getenv('MONDAY_API_KEY')
        return MondayClient

    @cached_property
    def boards(self):
        return BOARDS_TO_FETCH

    @cached_property
    def boards_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame([board for board in self.boards]).set_index('id')[['name']]
        df.index = df.index.astype(int)
        return df

    @cached_property
    def items_by_boards(self):
        boards = {}
        for board in self.boards:
            boards[board['id']] = self.get_items_from_board(board['id'])
        return boards

    @cached_property
    def boards_dataframes(self):
        all_boards = {}
        for board_id, items in self.items_by_boards.items():
            board_items = []
            for item in items:
                row = {}
                for column_value in item['column_values']:
                    # we need to restructure the data into something more tabular
                    row[f"{clean_column_name(column_value['title'])}__{column_value['id']}"] = column_value['text']
                    row['_board_id'] = board_id
                    row['_item_name'] = item['name']
                    row['_item_id'] = item['id']
                board_items.append(row)
            if not board_items:
                # ignore boards with no rows
                continue
            df = pd.DataFrame(board_items).set_index('_item_name')
            df = df.reindex(sorted(df.columns), axis=1)  # sort columns alphabetically for convenience
            all_boards[board_id] = df
        return all_boards

    @staticmethod
    def get_items_from_board(board_id: int) -> list:
        """ Fetch all the items (rows) from a board
        Ideally this would be done via the Moncli packages but it has some issues with casting values and API timeouts
        so for now we roll out own
        """
        all_items = []
        page = 1
        current_ids = True

        while current_ids:
            # get 25 most recent Ids
            items_per_page = 25
            board_query = f'{{boards(ids:{board_id}) {{ name id description items (limit: {items_per_page}, page: {page}, newest_first: true,) {{ id }} }} }}'
            data = {'query': board_query}

            r = requests.post(url=API_URL, json=data, headers=HEADERS)  # make request
            results = r.json()['data']['boards'][0]['items']
            print(f"Found {len(results)} IDs from page {page}")
            current_ids = [i['id'] for i in r.json()['data']['boards'][0]['items']]
            if len(current_ids) > 0:
                items_query = f"""
          {{
            items (ids: [{", ".join(current_ids)}] ) {{
                  id
                  name
                  column_values{{title id type text }}
              }}
          }}
          """
                data = {'query': items_query}
                r = requests.post(url=API_URL, json=data, headers=HEADERS)  # make request
                result = r.json()
                print(f"Found {len(result['data']['items'])} results in page {page}")
                all_items.extend(result['data']['items'])
                if len(result['data']['items']) < items_per_page:
                    # we fetched a partial page so there's not point fetching more
                    break
                page = page + 1

        return all_items

    @property
    def schema_name(self):
        return "monday"

    def collect(self):
        for board_id, board in self.boards_dataframes.items():
            board_name = clean_column_name(self.boards_dataframe.loc[int(board_id)]['name'])
            try:
                self.save_dataframe(board, board_name)
                print(f"Successfully saved {board_name}")
            except Exception as e:
                print(f"Could not save {board_name}", e)


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from os import getenv
    from dotenv import load_dotenv

    load_dotenv()

    db_engine = get_reporting_db_engine()
    prepare_db_for_collection(db_engine)
    collector = MondayCollector(db_engine)
    collector.collect()

    print(collector.boards_dataframes)
