# Confirmed within appropriate Level timescale?

This column determines whether the appointment was
confirmed in the expected timescale based on the level
of the appointment. The output is "{Yes|No} Level {level}".

## Monday Collector

The Level is not available from monday.com and so this does
not appear in the `monday` schema.

## Reporting

The Level is not represented in the reporting view and so this
column does not appear in the `reporting` views.

## Worker

The worker uses a function defined in the Worker file called 
`get_confirmation_sla_level`. This takes the `booking_start_datetime`, 
`request_datetime` and the `deal_closed_datetime` and outputs a string. 

Firstly it determines the level for the appointment using the `get_sla_level`
method, and passes it the `booking_start_datetime` and the `request_datetime`.
Then it uses the difference between the `request_datetime` and the `deal_closed_datetime`
as well as the Level to determine whether the appointment was confirmed in
the appropriate timescale. 