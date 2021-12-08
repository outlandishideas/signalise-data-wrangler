# Actual appt finish time

This is the recorded actual end time for the appointment.

## Monday

This is the same as the `actual_end_time__hour2` from 
`monday.booking_sales_pipeline_2020_21`.

## Reporting

The `actual_end_time` is set as the booking as the
same as `actual_end_time__hour2`. However if `actual_end_time__hour2`
is NULL or `00:00` then we set the `actual_end_time` as NULL as well.

## Worker 

The value of `actual_end_time` is outputed
as `HH:MM` or `n/a` if NULL