# Level of qualified interpreter met?

This always returns "Yes Level {level}" where
the level is derived for the appointment as a whole.
This is not an applicable column for Signalise, but
needs to be filled in.

## Monday Collector

The Level is not available from monday.com

## Reporting

The Level is not represented in the reporting view

## Worker

The output is always "Yes Level {level}"

The Level is determined by a function defined in the Worker called 
`get_sla_level`. It uses the `booking_start_datetime` and the 
`request_datetime` from the Reporting view and calculates the difference
between those two times. Based on the amount of hours or days between those 
two a Level between 1 and 5 is provided. 