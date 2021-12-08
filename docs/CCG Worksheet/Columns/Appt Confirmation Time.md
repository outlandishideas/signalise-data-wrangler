# Appt Confirmation Time

This is the time that the appointment was confirmed. 

## Monday Collector 

This is represented as a `datetime` in Monday and appears
in the `monday.booking_sales_pipeline_2020_21` table
as column `deal_closed__date_confirmed8`.

## Reporting

This data is copied directly from the `deal_closed__date_confirmed8`
and renamed as `deal_closed_datetime`.

## Worker


The Worker formats the datetime from `deal_closed_datetime` in the reporting
view and outputs the time in a 24hr format with `FMHH24:MI`. It applies 
`FM` to remove the leading zero from the hour, as this was how it was
formatted in the sample data.