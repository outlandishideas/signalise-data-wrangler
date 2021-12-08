# Type of appointment requested

This column shows the type of appointment that was requested. 
For almost all appointments the type of appointment is `Face to face`, 
however the value `N/A` is given if no location is provided for that 
appointment instead.

## Monday

This data is not provided in monday.com

## Reporting

This data is not provided in the reporting views

## Worker

A function exists in the worker, that returns "Face to face" if the
`location` data for the appointment is not empty. If it is empty
then the function returns "N/A".