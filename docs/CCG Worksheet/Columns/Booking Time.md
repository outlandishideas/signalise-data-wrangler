# Booking Time

The Booking Time is the hour:minute that the appointment 
takes place at.

## Monday Collector

Booking Time is available in the `monday.booking_sales_pipeline_2020_21`
as `start__hour`.

## Reporting

When creating the Reporting View, the time from `start__hour` is joined
with the `booking_date__date` from the same `monday` table to create the 
`booking_start_datetime` column in the `reporting.ccg_performance_reporting_booking_pipeline_2020_21_simple` view.

## Worker

The Worker formats the datetime from `booking_start_datetime` in the reporting
view and outputs the time in a 24hr format with `HH24:MI`. 