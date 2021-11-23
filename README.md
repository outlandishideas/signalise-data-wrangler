# Signalise data rationalisation

## Overview 
## Setting up


## Collectors

## Reporting views

## Workers

## Standalone workers
Standalone workers are like workers by they do not read from (or write to) the data warehouse.

They can create automations within an existing tool (e.g. copying info from one Monday board to another) or between 
tools. In general you should only yse a standalone worker where a standard data-warehouse-approach-worker would be 
impractical.

All the standalone workers are (currently) [Python Google Cloud Functions](https://cloud.google.com/functions/docs/quickstart-python). They should follow this pattern:

```

standalone_workers
        └  function_name
                └  main.py
                └ requirements.txt
```

You can deploy a function like this: 

```bash
 gcloud functions deploy sync_monday_booking_dates \
 --runtime python39 \
 --trigger-topic \
 sync-monday-booking-times \
 --source ./src/standalone_workers/sync_monday_enquiry_dates_to_bookings \
 --project calendar-sync-tmp \
 --entry-point sync_monday_enquiry_dates_to_bookings \
 --region europe-west2 \
 --memory 128mb \
 --max-instances 1
```

`entrypoint` should be the name of the main function in `main.py` which should be called when the Cloud Function is invoked
