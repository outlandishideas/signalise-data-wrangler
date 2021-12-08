# Level

The Level of an appointment is determined by the 
time from when the appointment was requested to the time
that it is to take place. 

## Monday Collector

The Level is not available from monday.com

## Reporting

The Level is not represeted in the reporting view

## Worker

The Level is determined by a function defined in the Worker called 
`get_sla_level`. It uses the `booking_start_datetime` and the 
`request_datetime` from the Reporting view and calculates the difference
between those two times. Based on the amount of hours or days between those 
two a Level between 1 and 5 is provided. 