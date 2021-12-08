# Venue of appointment (inc. video)

This shows the street address of the appointment, 
or `n/a` if the street address is not available. 

## Monday

This data is available from the `location__location` column in the 
`monday.booking_sales_pipeline_2020_21`. It is also available from
the `ccg_framework_locations` table, and this can be joined to the 
`booking_sales_pipeline_2020_21` table via the `sales_contacts` table.

## Reporting

Because we need to the the data from the `ccg_framework_locations`
table for other parts of the data, we actually take the
location data from the same table as well. This is associated
with each appointment via the `sales_contacts` table, joining
from `booking_sales_pipeline_2020_21` to `sales_contacts`
using the `sales_contacts__connect_boards5` column, and then
connecting the `sales_contacts` table with the `ccg_framework_locations` #
table using the `ccg_framework_locations__connect_boards` column. 

The location data is put into the reporting view as `location`.

## Worker

The `location` from the `reporting` view is used directly.