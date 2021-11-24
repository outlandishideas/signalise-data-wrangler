-- Function to take the date of one datetime combined with the hour of another
-- because of the messed up way Monday stores dates and hours
CREATE OR REPLACE FUNCTION zip_date_hour(timestamp, timestamp) RETURNS timestamp AS
$$
SELECT (date($1) || ' ' || LPAD(EXTRACT(HOUR FROM $2)::TEXT, 2) || ':' ||
        LPAD(EXTRACT(MINUTES FROM $2)::text, 2, '0'))::timestamp;
$$
    LANGUAGE SQL;
END;


-- Takes a duration (between the request time and start of the request), and a status
-- could be changed to also include other statuses such as "UNABLE TO BOOK"
-- which could either be handled by making the return type a string
-- or by returning special number for other codes - 404 could not find an interpreter; 400 for cancelled
CREATE OR REPLACE FUNCTION get_sla_from_duration(interval, text) RETURNS int
    LANGUAGE sql AS
$$
SELECT CASE
           WHEN $1 < INTERVAL '5 minutes' AND $2 = 'Booked'
               THEN 1
           WHEN $1 < INTERVAL '30 minutes' AND $2 = 'Booked'
               THEN 2
           WHEN $1 < INTERVAL '1 hour' AND $2 = 'Booked'
               THEN 3
           WHEN $1 < INTERVAL '1 day' AND $2 = 'Booked'
               THEN 4
           WHEN $1 < INTERVAL '3 days' AND $2 = 'Booked'
               THEN 5
           ELSE NULL END;
$$;


-- A view of the various times associated with an item
DROP VIEW IF EXISTS reporting.enquiry_booking_time CASCADE;
CREATE OR REPLACE VIEW reporting.enquiry_booking_time AS
(
SELECT item_id__item_id                                                                 item_id,
       status__status                                                                   status,
       creation_log__creation_log                                                       created,
       zip_date_hour(booking_date__date4, start__hour) AS                               start_time,
       deal_closed__date2                                                               closed,
       hr_tmp_clients__connect_boards7                                                  client,
       deal_closed__date2 - hr_tmp_enquiry.creation_log__creation_log                   deal_open_time,
       zip_date_hour(booking_date__date4, start__hour) -
       hr_tmp_enquiry.creation_log__creation_log                                        time_to_booking,
       get_sla_from_duration(zip_date_hour(booking_date__date4, start__hour) -
                             hr_tmp_enquiry.creation_log__creation_log, status__status) sla_level
FROM monday.hr_tmp_enquiry
    );

