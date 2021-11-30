# Signalise data rationalisation

## Overview

## Setting up

### Google Cloud setup

Go to https://console.cloud.google.com/apis/dashboard and create a new project if you don't already have one Click "
enable APIs and Services" and enable:

*
*

Go to https://console.cloud.google.com/apis/credentials and create a new Service Account. Download the
service-account.json and keep it safe.

## Collectors

Collectors fetch data from an external source (such as a CRM or spreadsheet).

* They should only fetch data from one source
* They should save data to a schema specific to the source they fetch from (e.g. gsuite, monday)
* They should minimise manipulation of the data so that the data they save is as close as possible to the data they
  fetched. If the data needs to be transformed that should happen in Reporting Views (see below)

## Reporting views

Reporting Views are SQL views on the underlying schemas that are populated by the collectors.

They can combine data from multiple sources/schema and aggregate data to make it convenient for Workers and other
reporting to uses.

## Workers

Query the warehouse and do an action on one or more external services.

### Workers must not save data to the data warehouse!

The data warehouse should not be the canonical store for any data - save it somewhere else. Another database, Google
sheets, Monday, etc.

They should subclass `Worker` and should implement a

* `find_candidates` function which finds items to do work on - e.g. identify booked appointments without corresponding
  calendar events
* `do_work` function which processes a single item (e.g. adding a calendar event and marking it as processed in the CRM)

## Standalone workers

Standalone workers are like workers by they do not read from (or write to) the data warehouse.

They can create automations within an existing tool (e.g. copying info from one Monday board to another) or between
tools. In general you should only yse a standalone worker where a standard data-warehouse-approach-worker would be
impractical.

All the standalone workers are (
currently) [Python Google Cloud Functions](https://cloud.google.com/functions/docs/quickstart-python). They should
follow this pattern:

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

`entrypoint` should be the name of the main function in `main.py` which should be called when the Cloud Function is
invoked
