# Booking Date

The Booking Date is the day/month/year that the appointment
is booked to happen on.

## Monday Collector

Booking Date is available in the `monday.booking_sales_pipeline_2020_21`
as `booking_date__date`.

## Reporting

When creating the Reporting View, the time from `start__hour` is joined
with the `booking_date__date` from the same `monday` table to create the 
`booking_start_datetime` column in the `reporting.ccg_performance_reporting_booking_pipeline_2020_21_simple` view.

## Worker

The Worker formats the datetime from `booking_start_datetime` in the reporting
view and outputs the date as "d/m/y" using `FMDD/MM/YYYY`. 

Note `FM` is added here to remove any leading zeros from the day as 
this was how it was formatted in the sample document.