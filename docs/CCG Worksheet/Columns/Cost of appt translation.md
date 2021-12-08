# Cost of appt/translation

Shows the cost (in £s) for the appointment. 

> **Note**: Where an entry in the `booking_sales_pipeline_2020_21`
> has two communication professionals, this value will appear 
> twice, but I assume they weren't charged twice, but that
> the value was charged once. 

## Monday

The value appears in the `quote_exc_vat__quiote_exc_vat`
in the `booking_sales_pipeline_2020_21` table.

## Reporting

The value is taken directly from `quote_exc_vat__quiote_exc_vat`
unless the value of `charge__status` is 'Canc no fee' then 
the value is set to 0. The value is put in the `appt_fee`


## Worker

The value is taken from the `appt_fee` column from 
reporting and then a function is used to turn it
into a value suitable for the worksheet. 

If the value is 0, or empty or None, then the 
returned value is None. If the value is anything
else then, the £ is prepended to it and the whole
thing is returned.