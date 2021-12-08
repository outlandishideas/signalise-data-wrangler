# Actual length of appt

This is the actual length of the appointment based
on the actual start time and end time.

## Monday

This data doesn't exist on monday.com

## Reporting

The `actual_length_of_appt` is diff between the 
`actual_start_time` and `actual_end_time`. If
the `actual_end_time` is NULL then we set the
`actual_length_of_appt` is set to also be NULL

## Worker 

The value of `actual_length_of_appt` is outputed
as `HH:MM` or `n/a` if NULL