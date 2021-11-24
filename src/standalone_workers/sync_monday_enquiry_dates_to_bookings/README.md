#Monday data sync function

Monday built in automations do not allow you to copy an hour column from one board to another.

As a workarond this cloud function checks for any t

## Deploy
Load the Monday API key from .env and then deploy the cloud function
```bash 
source .env
gcloud functions deploy sync_monday_booking_dates \
--runtime python39 \
--trigger-topic  sync-monday-booking-times \
--source ./src/standalone_workers/sync_monday_enquiry_dates_to_bookings \
--project calendar-sync-tmp \
--entry-point sync_monday_enquiry_dates_to_bookings \
--region europe-west2 \
--memory 128mb \
--max-instances 1
--set-env-vars MONDAY_API_KEY=$MONDAY_API_KEY
```

#Set up pub/sub topic to trigger the function every minute
https://console.cloud.google.com/cloudpubsub/topic/detail/sync-monday-booking-times?project=calendar-sync-tmp