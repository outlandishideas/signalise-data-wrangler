# Type of appointment request met?

This column shows whether the type of appointment that was requested was met. 
For almost all appointments the type of appointment is `Face to face`
and so the value for those appointments is `Yes Face to face`, 
however the value `N/A` is given if no location is provided for that 
appointment instead.

## Monday

This data is not provided in monday.com

## Reporting

This data is not provided in the reporting views

## Worker

A function exists in the worker, that returns "Yes Face to face" if the
`location` data for the appointment is not empty. If it is empty
then the function returns "N/A".