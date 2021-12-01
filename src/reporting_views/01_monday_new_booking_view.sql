
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
       hr_tmp_enquiry.creation_log__creation_log                                        time_to_booking
FROM monday.hr_tmp_enquiry
    );



-- new HR TMP View
CREATE OR REPLACE VIEW reporting.ccg_performance_reporting_hr_tmp AS
SELECT LPAD(EXTRACT(HOUR FROM start__hour)::TEXT, 2, '0') || ':' ||
       LPAD(EXTRACT(MINUTES FROM start__hour)::text, 2, '0')                              booking_time
     , booking_date__date4::DATE                                                       AS booking_date
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

