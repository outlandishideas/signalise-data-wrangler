# Length of appt booked (hours and minutes)

This shows the amount of time that was booked 
by being the difference between the start and 
end.

## Monday

The start time and the end time are both captured
in the Monday table, but the actual difference 
between the two are not available. 

The Start time is the `start__hour` and the End time
in the `end__hour9`. 

## Reporting

If the end time is null, or if the end time has 
a TIME value of 00:00 then we set the value of `length_of_appt_booked` 
to NULL.

Otherwise we create a time diff between the start time and 
the end time of the booking and add it to the column
`length_of_appt_booked` in reporting. 

## Worker

We format the value of `length_of_appt_booked`
as `HH:MM`.