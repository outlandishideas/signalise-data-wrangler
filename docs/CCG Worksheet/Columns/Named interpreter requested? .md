# Named interpreter requested? 

This shows Yes or No based on whether the booking
request included a request for a specific 
interpreter. 

## Monday

If a interpreter is requested, then that value
will appear in the `preferred_cp__connect_boards3`
on the `monday.booking_sales_pipeline_2020_21` table.
This will be the name of the language professional
from the `communication_professional_contacts` 
board.

## Reporting

A new column called `named_interpreter_requested`
is created in the reporting view, and is constructed
using a CASE statement so that if the value of
`preferred_cp__connect_boards3` is NULL or empty, 
then the value of `named_interpreter_requested` is
FALSE otherwise the value is TRUE.

## Worker

The Worker uses a simple CASE statement to convert
from the Boolean value from the `named_interpreter_requested`
column to a string representation as `Yes` or `No`.