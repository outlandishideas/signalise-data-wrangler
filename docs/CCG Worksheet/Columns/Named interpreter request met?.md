# Named interpreter request met?

This shows Yes or No based on whether the booking
request included a request for a specific 
interpreter and whether that specific interpreter
was booked. 

In the spreadsheet, the value is No if the 
a "Named interpreter requested?" value is No, 
or if it was Yes, but that interpreter was not booked. 

## Monday

If a interpreter is requested, then that value
will appear in the `preferred_cp__connect_boards3`
on the `monday.booking_sales_pipeline_2020_21` table.
This will be the name of the language professional
from the `communication_professional_contacts` 
board.

The name(s) of the booked professionals are in the 
`cp_1_connect_boards6` and `cp_2__connect_boards`
column.

## Reporting

A new column called `named_interpreter_request_met`
is created in the reporting view, and is constructed
using a CASE statement so that if the value of
`preferred_cp__connect_boards3` is NULL or empty, 
then the value of `named_interpreter_request_met` is
FALSE. 

If the value of `preferred_cp__connect_boards3` is 
not empty, then that value is compared against the 
values in `cp_1_connect_boards6` and `cp_2__connect_boards`
and if at least one matches, then the value is set as
TRUE otherwise it is FALSE.

## Worker

The Worker uses a simple CASE statement to convert
from the Boolean value from the `named_interpreter_request_met`
column to a string representation as `Yes` or `No`.