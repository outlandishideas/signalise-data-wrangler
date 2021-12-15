import pandas as pd
from shutil import copyfile
from src.util import get_reporting_db_engine
from src.workers.Worker import Worker
from datetime import timedelta, datetime

SPREADSHEET_COLUMNS = {
    "booking_time": "Booking Time",
    "booking_date": "Booking Date",
    "level": "Level",
    "appt_confirmation_time": "Appt Confirmation Time",
    "appt_confirmation_date": "Appt Confirmation Date",
    "confirmed_within_level_timescale": "Confirmed within appropriate Level timescale",
    "booker_ref": "Booker ref",
    "practice_code": "Practice Code",
    "location": "Venue of appointment (inc. video)",
    "type_of_appointment_requested": "Type of appointment requested",
    "type_of_appointment_request_met": "Type of appointment request met?",
    "details_of_request": "Details of request",
    "language_professional": "Language/professional",
    "named_interpreter_requested": "Named interpreter requested?",
    "named_interpreter_request_met": "Named interpreter request met?",
    "preferred_sex_of_interpreter_requested": "Preferred sex of interpreter requested?",
    "sex_pref_met": "Preferred sex of interpreter request met?",
    "ooa_interpreter_requested": "OOA interpreter requested?",
    "ooa_request_met": "OOA interpreter request met?",
    "interpreter_ref": "Interpreter ref",
    "action_taken_to_investigate_summary": "Action taken to investigate summary",
    "level_of_interpreter_met": "Level of qualified interpreter met?",
    "booking_cancelled": "Booking cancelled?",
    "appt_fee": "Cost of app/translation",
    "length_of_appt_booked": "Length of appt booked (hours and minutes)",
    "start_of_appt_took_place_in_appropriate_timescale": "Did the start of the assignment take place within the appropriate Level timescale",
    "actual_start_time": "Actual appt start time",
    "actual_end_time": "Actual appt finish time",
    "actual_length_of_appt": "Actual length of appt",
    "appt_fulfilled_within_length_of_time_booked": "Appt fulfilled within length of time booked?",
    "interpreter_present_within_level_timescale": "Interpreter present on site within appropriate Level timescale?",
    "interpreter_connected_remotely_within_timescale": "Interpreter connected remotely within timescale?",
}

def get_sla_level(request_time, start_time):
    """
    Get the SLA level of the booking based on the request time and start time

    We take the difference between the two times, and determine the SLA level
    based on the difference in minutes or hours between the two values.

    todo: how to manage cases where the request time is after the start time.

    :param request_time:
    :param start_time:
    :return:
    """

    diff = start_time - request_time
    if diff < timedelta(minutes=30):
        return 1
    elif diff < timedelta(hours=24*1):
        return 2
    elif diff <= timedelta(hours=24*3):
        return 3
    elif diff < timedelta(hours=24*14):
        return 4
    else:
        return 5

def get_confirmation_sla_level(request_time, start_time, confirmed_time):
    """
    Get the output for whether the booking was confirmed in time.

    Currently this returns "Yes Level {SLA}", but we might need to
    expand this if it is reasonable for the value to be No.

    :param request_time:
    :param start_time:
    :return:
    """

    level = get_sla_level(request_time, start_time)

    diff = confirmed_time - request_time

    if level == 1 and diff < timedelta(minutes=5):
        success = "Yes"
    elif level == 2 and diff < timedelta(minutes=30):
        success = "Yes"
    elif level == 3 and diff <= timedelta(hours=2):
        success = "Yes"
    elif level == 4 and diff <= timedelta(hours=24*1):
        success = "Yes"
    elif level == 5 and diff <= timedelta(hours=24*3) :
        success = "Yes"
    else:
        success = "No"

    return "{success} Level {level}".format(success=success, level=level)

def get_present_within_timescale(request_time, start_time):
    """
    Get the output for whether the person was present within the timescale.

    This returns "Yes Level {SLA}" as this column is not relevant for
    this type of work but is expected to filled in.

    :param request_time: The time that the request was made
    :param start_time:   The time of the booking
    :return:
    """
    return "Yes Level {}".format(get_sla_level(request_time, start_time))

def get_start_within_timescale(request_time, start_time):
    """
    Get the output for whether the appointment was started within the timescale.

    This returns "Yes Level {SLA}" as this column is not relevant for
    this type of work but is expected to filled in.

    :param request_time: The time that the request was made
    :param start_time:   The time of the booking
    :return:
    """
    return "Yes Level {}".format(get_sla_level(request_time, start_time))

def get_level_of_interpreter_met(request_time, start_time):
    """
    Get the output for whether the person was of the correct level.

    This returns "Yes Level {SLA}" as this column is not relevant for
    this type of work but is expected to filled in.

    :param request_time: The time that the request was made
    :param start_time:   The time of the booking
    :return:
    """
    return "Yes Level {}".format(get_sla_level(request_time, start_time))

def get_cost_from_appt_fee(fee):
    """
    Output the the appointment cost correctly formatted for worksheet

    If the fee is 0 or null or empty then we return None, but if
    the fee has a value then append "£" and return the value.

    :param fee: textual value of the fee
    :return:
    """
    if fee == '' or fee is None or fee == '0':
        return None

    return "£{}".format(fee)

def get_cancellation_status(cancelled, fee):
    """
    Output the cancellation status, based on whether it was cancelled and the fee

    If cancelled is true and fee is 0 or None then result is
    'Yes & no charge', if fee is anything else then result is
    'Yes & charged'.

    If cancelled is false then result is 'Not cancelled'.

    :param cancelled: boolean whether appointment cancelled
    :param fee: textual value of the fee
    :return:
    """
    if cancelled:
        if fee == '' or fee is None or fee == '0':
            return 'Yes & no charge'
        else:
            return 'Yes & charged'
    else:
        return 'Not cancelled'

def get_appointment_type(location):
    """
    Output the appointment type based on location

    If there is a location and the location is not Remote,
    then the requested appointment type is "Face to Face",
    if there is no location, then it is "N/A"

    :param location: location of appointment
    :return:
    """
    if location and location != 'Remote':
        return "Face to face"
    else:
        return 'N/A'

def get_appointment_type_met(location):
    """
    Output if the appointment type was met

    If there is a location and the location is not Remote, then
    the requested appointment type was "Face to face" and we can
    say "Yes Face to face", if there is no location, then it is "N/A".

    :param location: location of appointment
    :return:
    """
    if location is None:
        return 'N/A'
    elif location is '':
        return 'N/A'
    elif location == 'Remote':
        return 'N/A'
    elif location == 'n/a':
        return 'N/A'
    elif location == 'N/A':
        return 'N/A'
    else:
        return "Yes Face to face"


def get_interpreter_type(interpreter):
    """
    Output the required output for interpreter

    The value for the interpreter field, is specific for CCGs
    and depends on what the value from monday.com is.

    :param location: location of appointment
    :return:
    """
    if interpreter == 'Interpreter':
        return 'BSL Interpreter – TSLI'
    elif interpreter == 'Trainee interpreter':
        return 'BSL Interpreter – TSLI'
    elif interpreter == 'Translator':
        return 'BSL Translator'
    elif interpreter == 'Deafblind interpreter':
        return 'Deafblind Interpreter”'
    elif interpreter == 'ENT':
        return 'Electronic Notetaker'
    else:
        return interpreter



class ExportCCGPerformanceReportWorker(Worker):


    def __init__(self, db):
        super().__init__(db)
        self._start = datetime.today() - timedelta(days=30)
        self._end = datetime.today()

    @property
    def name(self):
        return "ExportCCGPerformanceReportWorker"

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value

    def find_candidates(self):
        q = """
            SELECT
                to_char(booking_start_datetime, 'HH24:MI') AS booking_time,
                to_char(booking_start_datetime, 'FMDD/MM/YYYY') AS booking_date,
                NULL AS level,
                to_char(request_datetime, 'FMHH12:MI:00 am') AS appt_confirmation_time,
                to_char(request_datetime, 'FMDD/MM/YYYY') AS appt_confirmation_date,
                NULL AS confirmed_within_level_timescale,
                booker_ref,
                practice_code,
                location,
                NULL AS type_of_appointment_requested,
                NULL AS type_of_appointment_request_met,
                details_of_request,
                language_professional,
                CASE 
                    WHEN named_interpreter_requested THEN 
                        'Yes' 
                    ELSE 
                        'No' 
                END AS named_interpreter_requested,
                CASE 
                    WHEN named_interpreter_request_met THEN 
                        'Yes' 
                    ELSE 
                        'No' 
                END AS named_interpreter_request_met,
                CASE 
                    WHEN preferred_sex_of_interpreter_requested THEN 
                        'Yes' 
                    ELSE 
                        'No' 
                END AS preferred_sex_of_interpreter_requested,
                CASE 
                    WHEN preferred_sex_of_interpreter_requested IS FALSE THEN 
                        'N/A' 
                    WHEN sex_pref_met THEN
                        'Yes'
                    ELSE
                        'No'
                END AS sex_pref_met,
                'No' AS ooa_interpreter_requested,
                'N/A' AS ooa_request_met,
                interpreter_ref,
                CASE 
                    WHEN booking_cancelled THEN
                        action_taken_to_investigate_summary
                END AS action_taken_to_investigate_summary,
                level_of_interpreter_met,
                booking_cancelled,
                appt_fee,
                to_char(length_of_appt_booked, 'FMHH24:MI') AS length_of_appt_booked ,
                NULL AS start_of_appt_took_place_in_appropriate_timescale,
                to_char(booking_start_datetime, 'HH24:MI') AS actual_start_time,
                CASE 
                    WHEN actual_end_time IS NULL THEN 
                        'n/a'
                    ELSE 
                        to_char(actual_end_time, 'HH24:MI') 
                END AS actual_end_time,
                CASE 
                    WHEN actual_length_of_appt IS NULL THEN 
                        'n/a'
                    ELSE 
                        to_char(actual_length_of_appt, 'FMHH24:MI') 
                END AS actual_length_of_appt,
                'Yes' AS appt_fulfilled_within_length_of_time_booked,
                NULL AS interpreter_present_within_level_timescale,
                'N/A' AS interpreter_connected_remotely_within_timescale,
                request_datetime,
                deal_closed_datetime,
                booking_start_datetime
            FROM reporting.ccg_performance_reporting_booking_pipeline_2020_21_simple 
            WHERE DATE(booking_start_datetime) >= %(start)s
              AND DATE(booking_start_datetime) <= %(end)s
              AND ccg = %(ccg)s
            ORDER BY booking_start_datetime;
        """

        params = {
            'start': self.start.strftime('%Y-%m-%d'),
            'end': self.end.strftime('%Y-%m-%d')
        }

        ccgs = pd.read_sql("""
            SELECT 
                DISTINCT(ccg) AS ccg 
            FROM reporting.ccg_performance_reporting_booking_pipeline_2020_21_simple
            WHERE ccg IS NOT NULL
        """, self.db)

        all_candidates = []

        for ccg in ccgs['ccg']:
            params['ccg'] = ccg

            legacy = pd.read_sql(q, self.db, params=params)

            if not legacy.empty:
                legacy['level'] = legacy.apply(lambda x: get_sla_level(x.request_datetime, x.booking_start_datetime), axis=1)
                legacy['confirmed_within_level_timescale'] = legacy.apply(lambda x: get_confirmation_sla_level(x.request_datetime, x.booking_start_datetime, x.deal_closed_datetime), axis=1)
                legacy['appt_fee'] = legacy.apply(lambda x: get_cost_from_appt_fee(x.appt_fee), axis=1)
                legacy['interpreter_present_within_level_timescale'] = legacy.apply(lambda x: get_present_within_timescale(x.request_datetime, x.booking_start_datetime), axis=1)
                legacy['start_of_appt_took_place_in_appropriate_timescale'] = legacy.apply(lambda x: get_start_within_timescale(x.request_datetime, x.booking_start_datetime), axis=1)
                legacy['level_of_interpreter_met'] = legacy.apply(lambda x: get_level_of_interpreter_met(x.request_datetime, x.booking_start_datetime), axis=1)
                legacy['booking_cancelled'] = legacy.apply(lambda x: get_cancellation_status(x.booking_cancelled, x.appt_fee), axis=1)
                legacy['type_of_appointment_requested'] = legacy.apply(lambda x: get_appointment_type(x.location), axis=1)
                legacy['type_of_appointment_request_met'] = legacy.apply(lambda x: get_appointment_type_met(x.location), axis=1)
                legacy['language_professional'] = legacy.apply(lambda x: get_interpreter_type(x.language_professional), axis=1)

            legacy = legacy.drop(columns=['request_datetime', 'booking_start_datetime' ,'deal_closed_datetime']).rename(columns=SPREADSHEET_COLUMNS)

            all_candidates.append({
                'ccg': ccg,
                'values': legacy,
                'period': self.start.strftime('%Y-%m')
            })

        return all_candidates

    def work(self, candidate: dict):
        # this particular worker just has one candidate which takes the form of a dataframe
        # in future it might be one dataframe per customer or similar

        filename = '{ccg} {period} {datetime}.xlsx'.format(
            ccg=candidate['ccg'],
            period=candidate['period'],
            datetime=datetime.now().strftime('%Y-%m-%d')
        )

        copyfile('ccg_template.xlsx', filename)

        with pd.ExcelWriter(filename, mode="a", engine="openpyxl", if_sheet_exists='replace') as writer:
            candidate['values'].to_excel(writer, sheet_name="Monthly Booking Log", header=True)

    def last_month(self):
        today = datetime.now()

        end_of_month = datetime(today.year, today.month, 1) - timedelta(days=1)
        start_of_month = datetime(end_of_month.year, end_of_month.month, 1)

        self.end = end_of_month
        self.start = start_of_month

    def this_month(self):
        today = datetime.now()
        year = today.year
        month = today.month

        if month == 12:
            year = year + 1
            month = 1

        end_of_month = datetime(year, month, 1) - timedelta(days=1)
        start_of_month = datetime(end_of_month.year, end_of_month.month, 1)

        self.end = end_of_month
        self.start = start_of_month

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    db_engine = get_reporting_db_engine()
    worker = ExportCCGPerformanceReportWorker(db_engine)
    worker.do_all_work()
