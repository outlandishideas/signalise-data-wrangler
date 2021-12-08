# Booking ref

This is currently the name of the person
who made the booking. 

> **Note:** In the existing data, the name is not used
but a string like `CCG1234` is used instead. This data is not 
available in monday.com, so the name is used instead. 
>
> If the Booking ref should not be the person's name, then that data
> will need to be added to the Sales Contacts table on monday.com, 
> so it can be made available here.

## Monday

The name of the person used as the Booking ref is from the Sales
Contacts board, and is available in the `sales_contacts__connect_boards5`
column in the `monday.booking_sales_pipeline_2020_21`.

## Reporting

The name from the column `sales_contacts__connect_boards5` is put into
a column in the `reporting` view called `booker_ref`.

> If some other value from the `Sales Contacts` table should be 
>used instead, then it would be easy enough to join the `monday.booking_sales_pipeline_2020_21`
> to the `monday.sales_contacts` table by the `sales_contacts__connect_boards5` and
> the `_item_name` column and use the value of another column
> on the `sales_contacts` table from there.

## Worker

The value is taken directly from `booker_ref`.