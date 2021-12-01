
CREATE OR REPLACE VIEW reporting.ccg_performance_reporting_booking_pipeline_2020_21 AS
SELECT LPAD(EXTRACT(HOUR FROM start__hour)::TEXT, 2, '0') || ':' ||
       LPAD(EXTRACT(MINUTES FROM start__hour)::text, 2, '0')                              booking_time
     , booking_date__date::DATE                                                        AS booking_date
     , LPAD(EXTRACT(HOUR FROM deal_closed__date_confirmed8)::TEXT, 2, '0') || ':' ||
       LPAD(EXTRACT(MINUTES FROM deal_closed__date_confirmed8)::text, 2, '0')          AS appt_confirmation_time
     , deal_closed__date_confirmed8::DATE                                              AS appt_confirmation_date
     , sales_contacts__connect_boards5                                                 AS booker_ref
     , (SELECT nacs_code__text4
        FROM monday.ccg_framework_locations
        WHERE location__location = location__location
        LIMIT 1)                                                                       AS practice_code   -- this should be looking up based on sales contact
     , location__location                                                              AS location
     , '?'                                                                             AS type_of_appointment_requested
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
           WHEN charge__status = 'Canc no fee' OR charge__status = 'Canc 50%% fee' OR
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
