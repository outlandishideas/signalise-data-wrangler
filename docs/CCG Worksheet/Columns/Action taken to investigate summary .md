# Action taken to investigate summary 

This column is filled in with notes about any actions
taken. This appears to only be filled in when the 
appointment has been cancelled. 

> **Note**: Two assumptions have been made here:
> 1) that the value to be shown is derived from 
> invoice_notes__notes, and
> 2) that the value should only be shown if the 
> appointment was cancelled.

## Monday

It was not clear what the value should have been 
but the `invoice_notes__notes` column from the 
`monday.booking_sales_pipeline_2020_21` table
appeared to fit the bill. 

## Reporting

The value from `invoice_notes__notes` was 
copied over as `action_taken_to_investigate_summary`. 

## Worker

If the appointment was cancelled, then the value
from `action_taken_to_investigate_summary` was used, 
otherwise the value was left blank.