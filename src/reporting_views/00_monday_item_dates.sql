
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

CREATE or replace function met_sla_booking_time (timestamp, timestamp, timestamp) RETURNS bool
    LANGUAGE sql
    AS

    'select false';
    --calculate the gap between request and start to get level
    --calculate the gap between request and booking to get booking time
    --check SLA times per level to see if booking time is less than SLA


;

SELECT location__location, count(nacs_code__text4) from monday.ccg_framework_locations group by location__location order by count desc;

CREATE OR REPLACE VIEW reporting.ccg_performance_reporting_booking_pipeline_2020_21 AS
SELECT LPAD(EXTRACT(HOUR FROM start__hour)::TEXT, 2, '0') || ':' ||
       LPAD(EXTRACT(MINUTES FROM start__hour)::text, 2, '0')                              booking_time
     , booking_date__date::DATE                                                        AS booking_date
     , get_sla_from_duration(zip_date_hour(booking_date__date, start__hour) - deal_closed__date_confirmed8,
                             stage__status7)                                           AS level
     , LPAD(EXTRACT(HOUR FROM deal_closed__date_confirmed8)::TEXT, 2, '0') || ':' ||
       LPAD(EXTRACT(MINUTES FROM deal_closed__date_confirmed8)::text, 2, '0')             appt_confirmation_time
     , deal_closed__date_confirmed8::DATE                                              AS appt_confirmation_date
     , met_sla_booking_time(zip_date_hour(booking_date__date, start__hour), deal_closed__date_confirmed8, deal_closed__date_confirmed8)                                                              AS confirmed_within_appropriate_level_timescale
     , sales_contacts__connect_boards5                                                 AS booker_ref
     , (SELECT nacs_code__text4 from monday.ccg_framework_locations where location__location = location__location LIMIT 1)  as practice_code -- this should be looking up based on sales contact
     , location__location                                                              AS location
     , '?'                                                     AS type_of_appointment_requested
     , '?'                                                                             AS type_of_appointment_request_met
     , booking_type__session_notes                                                     AS details_of_request
     , type_of_professional__type_of_professional                                      AS language_professional
     , CASE
           WHEN preferred_cp__connect_boards3 IS NULL OR preferred_cp__connect_boards3 = '' THEN FALSE
           ELSE TRUE END                                                               AS named_interpreter_requested
     , CASE
           WHEN preferred_cp__connect_boards3 IS NULL OR preferred_cp__connect_boards3 = '' THEN NULL
           WHEN preferred_cp__connect_boards3 = cp_1__connect_boards6 OR
                preferred_cp__connect_boards3 = cp_2__connect_boards THEN TRUE
           ELSE FALSE END                                                                 asnamed_interpreter_request_met
--      , preferred_cp__connect_boards3
--      , cp_1__connect_boards6
--      , cp_2__connect_boards
     , CASE WHEN pref__sex___status0 = 'No preference' THEN FALSE ELSE TRUE END        AS preferred_sex_of_interpreter_requested
     , 'sex of each CP needs to be added to communication_professional_contacts_board' AS sex_pref_met
     , (SELECT member__status0
        FROM monday.communication_professional_contacts
        WHERE communication_professional_contacts._item_name = cp_1__connect_boards6)  AS members_status_to_demo_how_sex_pref_met_should_work
     , '?'                                                                             AS ooa_interpreter_requested
     , '?'                                                                             AS ooa_request_met
     , cp_1__connect_boards6                                                           AS interpreter_ref --todo handle cp2. Could turn this whole view into a unison with exactly the same, but filtered on cp2 - need to know exactly what is desired in the report
     , '?'                                                                             AS action_taken_to_investigate_summary
     , '?'                                                                             AS level_of_interpreter_met
     , CASE
           WHEN charge__status = 'Canc no fee' OR charge__status = 'Canc 50% fee' OR
                charge__status = 'Cancelled Full Fee' THEN TRUE
           ELSE FALSE END                                                              AS booking_cancelled
     , CASE
           WHEN charge__status = 'Canc no fee' THEN '0'
           ELSE quote_exc_vat__quote_exc_vat END                                       AS appt_fee
     , zip_date_hour(booking_date__date, end__hour9) -
       zip_date_hour(booking_date__date, start__hour)                                  AS length_of_appt_booked
     , '?'                                                                             AS start_of_appt_took_place_in_appropriate_timescale
     , '?'                                                                             AS actual_start_time
     , actual_end_time__hour2                                                          AS actual_end_time
     , zip_date_hour(booking_date__date, end__hour9) -
       zip_date_hour(booking_date__date, actual_end_time__hour2)                       AS actual_length_of_appt
     , '?'                                                                             AS appt_fulfilled_withing_length_of_time_booked
     , '?'                                                                             AS interpreter_present_within_level_timescale
     , '?'                                                                             AS interpreter_connected_remotely_within_timescale

FROM monday.booking_sales_pipeline_2020_21;

-- new HR TMP View
CREATE OR REPLACE VIEW reporting.ccg_performance_reporting_hr_tmp AS
SELECT LPAD(EXTRACT(HOUR FROM start__hour)::TEXT, 2, '0') || ':' ||
       LPAD(EXTRACT(MINUTES FROM start__hour)::text, 2, '0')                              booking_time
     , booking_date__date4::DATE                                                       AS booking_date
     , get_sla_from_duration(zip_date_hour(booking_date__date4, start__hour) - deal_closed__date2,
                             b.status__status)                                         AS level
     , LPAD(EXTRACT(HOUR FROM deal_closed__date2)::TEXT, 2, '0') || ':' ||
       LPAD(EXTRACT(MINUTES FROM deal_closed__date2)::text, 2, '0')                       appt_confirmation_time
     , deal_closed__date2::DATE                                                        AS appt_confirmation_date
     , CASE
           WHEN deal_closed__date2 - creation_log__creation_log <
                INTERVAL '1 hour' THEN TRUE
           ELSE FALSE END                                                              AS confirmed_within_appropriate_level_timescale
     , person__person                                                                  AS booker_ref
     , location__location                                                              AS practice_code
     , location__location                                                              AS location
     , booking_type__dropdown                                                          AS type_of_appointment_requested
     , '?'                                                                             AS type_of_appointment_request_met
     , '?'                                                                             AS details_of_request
     , '?'                                                                             AS language_professional
     , CASE
           WHEN preferred_cps__mirror IS NULL OR preferred_cps__mirror = '' THEN FALSE
           ELSE TRUE END                                                               AS named_interpreter_requested
     , CASE
           WHEN preferred_cps__mirror IS NULL OR preferred_cps__mirror = '' THEN NULL
           WHEN preferred_cps__mirror = communication_professional_contacts__connect_boards1 THEN TRUE
           ELSE FALSE END                                                                 asnamed_interpreter_request_met
--      , preferred_cp__connect_boards3
--      , cp_1__connect_boards6
--      , cp_2__connect_boards
     , CASE
           WHEN pref_sex___pref_sex_::TEXT = 'No preference' THEN FALSE
           ELSE TRUE END                                                               AS preferred_sex_of_interpreter_requested
     , 'sex of each CP needs to be added to communication_professional_contacts_board' AS sex_pref_met
     , (SELECT member__status0
        FROM monday.communication_professional_contacts
        WHERE communication_professional_contacts._item_name =
              communication_professional_contacts__connect_boards1)                    AS members_status_to_demo_how_sex_pref_met_should_work
     , '?'                                                                             AS ooa_interpreter_requested
     , '?'                                                                             AS ooa_request_met
     , communication_professional_contacts__connect_boards1                            AS interpreter_ref --todo handle cp2. Could turn this whole view into a unison with exactly the same, but filtered on cp2 - need to know exactly what is desired in the report
     , '?'                                                                             AS action_taken_to_investigate_summary
     , '?'                                                                             AS level_of_interpreter_met
     , '?'                                                                             AS booking_cancelled
     , (SELECT SUM(agreed_price__numbers::float)
        FROM monday.hr_tmp_booking
        WHERE b.enquiry_ref__text = en._item_id
          AND agreed_price__numbers > '')                                              AS appt_fee
     , zip_date_hour(booking_date__date4, end__hour_1) -
       zip_date_hour(booking_date__date4, start__hour)                                 AS length_of_appt_booked
     , '?'                                                                             AS start_of_appt_took_place_in_appropriate_timescale
     , '?'                                                                             AS actual_start_time
     , '*'                                                                             AS actual_end_time
     , '*'                                                                             AS actual_length_of_appt
     , '?'                                                                             AS appt_fulfilled_withing_length_of_time_booked
     , '?'                                                                             AS interpreter_present_within_level_timescale
     , '?'                                                                             AS interpreter_connected_remotely_within_timescale

FROM monday.hr_tmp_enquiry en
         LEFT JOIN monday.hr_tmp_booking b ON b.enquiry_ref__text = en._item_id;


SELECT SUM(agreed_price__numbers::float)
FROM monday.hr_tmp_booking
WHERE agreed_price__numbers > ''
