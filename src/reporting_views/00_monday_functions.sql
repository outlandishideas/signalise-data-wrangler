CREATE OR REPLACE FUNCTION zip_date_hour(timestamp, timestamp) RETURNS timestamp AS
$$
    -- Function to take the date of one datetime combined with the hour of another
-- because of the messed up way Monday stores dates and hours
SELECT (date($1) || ' ' || LPAD(EXTRACT(HOUR FROM $2)::TEXT, 2) || ':' ||
        LPAD(EXTRACT(MINUTES FROM $2)::text, 2, '0'))::timestamp;
$$
    LANGUAGE SQL;
END;



CREATE OR REPLACE FUNCTION get_sla_from_duration(interval) RETURNS int
    LANGUAGE sql AS
$$
    -- Takes a duration (between the request time and start of the request), and a status
-- could be changed to also include other statuses such as "UNABLE TO BOOK"
-- which could either be handled by making the return type a string
-- or by returning special number for other codes
-- - 404 could not find an interpreter; 400 for cancelled no fee, 402 cancelled fee
SELECT CASE
           WHEN $1 < INTERVAL '5 minutes'
               THEN 1
           WHEN $1 < INTERVAL '30 minutes'
               THEN 2
           WHEN $1 < INTERVAL '1 hour'
               THEN 3
           WHEN $1 < INTERVAL '1 day'
               THEN 4
           ELSE 5 END;
$$;
