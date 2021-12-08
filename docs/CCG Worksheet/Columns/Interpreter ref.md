# Interpreter ref

This is currently the name of the language professional
who was booked for the appointment. 

> **Note:** In the existing data, the name is not used
but a string like `LN12345` is used instead. This data is not 
available in monday.com, so the name is used instead. 
>
> If the Interpreter ref should not be the person's name, then that data
> will need to be added to the Communication Professional Contacts table on monday.com, 
> so it can be made available here.

## Monday

The name of the person used as the Interpreter ref is from the Sales
Communication Professional Contacts board, and is available in the `cp_1__connect_boards6`
and `cp_2_connect_boards` columns in the `monday.booking_sales_pipeline_2020_21`.

## Reporting

The name from the column `cp_1__connect_boards6` is put into
a column in the `reporting` view called `interpreter_ref`.

Because we need separate lines for each Booking rather than
each appointment, the reporting view is constructed from two queries, 
one which gets the values from the `cp_1__connect_boards6` and one 
which gets the values from `cp_2__connect_boards` if it has a value. 

> If some other value from the `Communication Professional Contacts` table should be 
>used instead, then it would be easy enough to join the `monday.booking_sales_pipeline_2020_21`
> to the `monday.communication_professional_contacts` table by the `cp_1__connect_boards6` and
> the `_item_name` column and use the value of another column
> on the `sales_contacts` table from there.

## Worker

The value is taken directly from `interpreter_ref`.