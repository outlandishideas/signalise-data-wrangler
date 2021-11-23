import base64
import requests
from os import getenv

API_KEY = getenv('MONDAY_API_KEY')
API_URL = "https://api.monday.com/v2"
HEADERS = {"Authorization": API_KEY}

BOOKING_BOARD_ID = 1915136720
BOOKING_BOARD_DATE_COLUMN_ID = 'text3'

ENQUIRY_BOARD_START_COLUMN_ID = 'hour'
ENQUIRY_BOARD_END_COLUMN_ID = 'hour1'
ENQUIRY_BOARD_DATE_COLUMN_ID = 'date4'


def sync_monday_enquiry_dates_to_bookings(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    items_to_update = get_items_to_update()
    enquiry_dates = get_dates_from_enquiries(items_to_update.values())

    responses = []
    for booking_id, enquiry_id in items_to_update.items():
        responses.append(update_booking_date(booking_id, enquiry_dates[enquiry_id]))
    print(responses, {"event": event, "context": context})


def get_items_to_update():
    query = f'''{{items_by_column_values (
    board_id: {BOOKING_BOARD_ID}, 
    column_id: "{BOOKING_BOARD_DATE_COLUMN_ID}", 
    column_value: "Pending") 
    {{
  id
  column_values{{
          id
          title
          text
          value
        }}
  }}}}'''
    data = {'query': query}

    r = requests.post(url=API_URL, json=data, headers=HEADERS)  # make request
    response = r.json()

    # create a dict of booking_id->enquiry_id
    items_to_update = {}
    for booking in response['data']['items_by_column_values']:
        enquiry_id = column_value(booking, 'text')
        if enquiry_id:
            items_to_update[booking['id']] = enquiry_id
        else:
            print(f"booking {booking['id']} has no Enquiry ID so cannot be updated")

    return items_to_update


def get_dates_from_enquiries(enquiry_ids):
    query = f"""
          {{
              items (ids: [{','.join(enquiry_ids)}]) {{
                name
                column_values{{
                      id
                      title
                      text
                      value
                    }}
            }}
          }}
        """
    data = {'query': query}

    r = requests.post(url=API_URL, json=data, headers=HEADERS)  # make request
    response = r.json()
    enquiry_dates = {}
    for enquiry in response['data']['items']:
        start = column_value(enquiry, ENQUIRY_BOARD_START_COLUMN_ID)
        end = column_value(enquiry, ENQUIRY_BOARD_END_COLUMN_ID)
        date = column_value(enquiry, ENQUIRY_BOARD_DATE_COLUMN_ID)
        enquiry_id = column_value(enquiry, 'item_id')
        enquiry_dates[enquiry_id] = f"{date} {start}-{end}"

    return enquiry_dates


def update_booking_date(booking_id: int, date: str):
    mutation = f"""mutation{{ 
    change_simple_column_value (
        board_id: {BOOKING_BOARD_ID}, 
        item_id: {booking_id}, 
        column_id: "{BOOKING_BOARD_DATE_COLUMN_ID}", 
        value: "{date}"
    ){{ 
            id
          }}}}"""
    data = {"query": mutation}
    r = requests.post(url=API_URL, json=data, headers=HEADERS)
    return r.json()


def column_value(item, column_id):
    return [column['text'] for column in item['column_values'] if column['id'] == column_id][0]


if __name__ == '__main__':
    sync_booking_dates({}, {})
