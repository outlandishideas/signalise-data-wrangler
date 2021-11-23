import os
from functools import cached_property

import dotenv

from .Collector import Collector
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd

from src.util import get_reporting_db_engine, prepare_db_for_collection

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/contacts.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/directory.readonly',
    'https://www.googleapis.com/auth/contacts.other.readonly',

]
dotenv.load_dotenv()
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # You should make it an environment variable
CREDENTIALS = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


class GsuiteCollector(Collector):
    _people_dataframe: pd.DataFrame
    _events_dataframe: pd.DataFrame

    @property
    def schema_name(self):
        return "gsuite"

    def collect(self):
        self.save_dataframe(self.people_dataframe, 'people')
        self.save_dataframe(self.events_dataframe, 'events')

    @property
    def default_subject_email(self):
        return os.getenv('GOOGLE_DEFAULT_SUBJECT_EMAIL')

    """
    PEOPLE collector
    Fetch people from the directory and people from the contacts
    """

    def get_people_service(self, subject_email=None):
        delegated_credentials = CREDENTIALS.with_subject(subject_email or self.default_subject_email)
        people_service = build('people', 'v1', credentials=delegated_credentials)
        return people_service

    def collect_people_directory(self, subject_email=None):
        print("Fetching people from directory")
        people = self.get_people_service(subject_email or self.default_subject_email).people()
        # https://googleapis.github.io/google-api-python-client/docs/dyn/people_v1.people.html
        all_people = []
        request = people.listDirectoryPeople(readMask='names,emailAddresses',
                                             sources=['DIRECTORY_SOURCE_TYPE_DOMAIN_CONTACT',
                                                      'DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE'])
        response = request.execute()
        while response is not None:
            all_people.extend(response['people'])
            request = people.listDirectoryPeople_next(request, response)
            if not request:
                break
            response = request.execute()

        return all_people

    def collect_people_contacts(self, subject_email=None):
        print("Fetching contacts")
        all_contacts = []
        # https://googleapis.github.io/google-api-python-client/docs/dyn/people_v1.otherContacts.html
        other_contacts = self.get_people_service(subject_email or self.default_subject_email).otherContacts()
        request = other_contacts.list(readMask='names,emailAddresses')
        response = request.execute()
        while response is not None:
            all_contacts.extend(response['otherContacts'])
            request = other_contacts.list_next(request, response)
            if not request:
                break
            response = request.execute()
        return all_contacts

    @cached_property
    def people_dataframe(self):
        all_people = self.collect_people_contacts() + self.collect_people_directory()
        return self.normalise_people_dataframe(all_people)

    @staticmethod
    def normalise_people_dataframe(people):
        return pd.json_normalize(people, record_path=['emailAddresses'], meta=['resourceName', 'etag'])

    """
    CALENDAR EVENTS collector
    """

    def get_calendar_service(self, subject):
        delegated_credentials = CREDENTIALS.with_subject(subject or self.default_subject_email)
        calendar_service = build('calendar', 'v3', credentials=delegated_credentials)
        return calendar_service

    # https://developers.google.com/calendar/api/v3/reference/events/list

    def get_events_for_subject(self, subject_email, days_past=0, days_ahead=90):
        start = (datetime.utcnow() - timedelta(days=days_past)).isoformat() + 'Z'  # 'Z' indicates UTC time
        end = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'

        all_events = []
        events = self.get_calendar_service(subject_email).events()
        request = events.list(calendarId=subject_email, timeMin=start, timeMax=end, orderBy='startTime',
                              singleEvents=True)
        response = request.execute()
        while response is not None:
            all_events.extend(response['items'])
            request = events.list_next(request, response)
            if not request:
                break
            response = request.execute()

        return all_events

    def get_events_for_all_people(self, days_past=0, days_ahead=90):
        everyones_events = []
        for address in self.people_dataframe.query('metadata_source_type == "DOMAIN_PROFILE"').value:
            if "outlandish.com" not in address:
                continue
            print(f"Fetching events for {address}")
            everyones_events.extend(self.get_events_for_subject(address, days_past=0, days_ahead=90))
        return everyones_events

    @cached_property
    def events_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame.from_records(pd.json_normalize(self.get_events_for_all_people()))


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from os import getenv
    from dotenv import load_dotenv

    load_dotenv()

    db_engine = get_reporting_db_engine()
    prepare_db_for_collection(db_engine)
    collector = GsuiteCollector(db_engine)
    collector.collect()
