
DROP VIEW IF EXISTS reporting.ccg_performance_reporting_booking_pipeline_2020_21_simple;
CREATE OR REPLACE VIEW reporting.ccg_performance_reporting_booking_pipeline_2020_21_simple AS
SELECT zip_date_hour(booking_date__date, start__hour)                                  AS  booking_start_datetime
     , zip_date_hour(booking_date__date, end__hour9)                                  AS  booking_end_datetime
     , zip_date_hour(deal_closed__date_confirmed8, deal_closed__date_confirmed8)       AS  deal_closed_datetime
     , creation_log__creation_log                                                      AS  request_datetime
     , booking._item_name                                                              AS  booker_ref
     , sales_contacts__connect_boards5                                                 AS  sales_contact
     , ccg.nacs_code__text4                                                            AS  practice_code
     , booking.location__location                                                      AS  location
     , ccg.contract__status                                                             AS  ccg
     , booking_type__session_notes                                                     AS  details_of_request
     , type_of_professional__type_of_professional                                      AS  language_professional
     , CASE
           WHEN preferred_cp__connect_boards3 IS NULL OR preferred_cp__connect_boards3 = '' THEN FALSE
           ELSE TRUE END                                                               AS  named_interpreter_requested
     , CASE
           WHEN preferred_cp__connect_boards3 IS NULL OR preferred_cp__connect_boards3 = '' THEN NULL
           WHEN preferred_cp__connect_boards3 = cp_1__connect_boards6 OR
                preferred_cp__connect_boards3 = cp_2__connect_boards THEN TRUE
           ELSE FALSE END                                                              AS  named_interpreter_request_met
     , CASE WHEN pref__sex___status0 = 'No preference' THEN FALSE ELSE TRUE END        AS  preferred_sex_of_interpreter_requested
     , CASE
           WHEN pref__sex___status0 = 'No preference' THEN NULL
           WHEN pref__sex___status0 = interpreters.sex__status04 THEN TRUE
           WHEN preferred_interpreters.sex__status04 = interpreters.sex__status04 THEN TRUE
           ELSE FALSE
     END AS sex_pref_met
     , (SELECT member__status0
        FROM monday.communication_professional_contacts
        WHERE communication_professional_contacts._item_name = cp_1__connect_boards6)  AS  members_status_to_demo_how_sex_pref_met_should_work
     , interpreters.reg_number__text2                                                           AS  interpreter_ref --todo handle cp2. Could turn this whole view into a unison with exactly the same, but filtered on cp2 - need to know exactly what is desired in the report
     , invoice_notes__notes                                                            AS  action_taken_to_investigate_summary
     , NULL AS level_of_interpreter_met
     , CASE
           WHEN charge__status = 'Canc no fee' OR charge__status = 'Canc 50%% fee' OR
                charge__status = 'Cancelled Full Fee' THEN TRUE
           ELSE FALSE END                                                              AS  booking_cancelled
     , CASE
           WHEN charge__status = 'Canc no fee' THEN '0'
           ELSE quote_exc_vat__quote_exc_vat END                                       AS  appt_fee
     , CASE
           WHEN end__hour9 IS NULL THEN
               NULL
           WHEN EXTRACT(HOUR FROM end__hour9) = '00'
            AND EXTRACT(MINUTE FROM end__hour9) = '00' THEN
               NULL
           ELSE
               zip_date_hour(booking_date__date, end__hour9) -
               zip_date_hour(booking_date__date, start__hour)
       END                                  AS  length_of_appt_booked
     , zip_date_hour(booking_date__date, start__hour)                                  AS  actual_start_time
     , CASE
           WHEN actual_end_time__hour2 IS NULL THEN
               NULL
           WHEN EXTRACT(HOUR FROM actual_end_time__hour2) = '00'
            AND EXTRACT(MINUTE FROM actual_end_time__hour2) = '00' THEN
               NULL
           ELSE
               zip_date_hour(booking_date__date, actual_end_time__hour2)
       END                                                                             AS  actual_end_time
     , CASE
           WHEN actual_end_time__hour2 IS NULL THEN
               NULL
           WHEN EXTRACT(HOUR FROM actual_end_time__hour2) = '00'
            AND EXTRACT(MINUTE FROM actual_end_time__hour2) = '00' THEN
               NULL
           ELSE
               zip_date_hour(booking_date__date, actual_end_time__hour2) -
                zip_date_hour(booking_date__date, start__hour)
       END                                  AS  actual_length_of_appt
FROM monday.booking_sales_pipeline_2020_21 AS booking
LEFT JOIN monday.sales_contacts AS contacts
    ON contacts._item_name = booking.sales_contacts__connect_boards5
LEFT JOIN monday.communication_professional_contacts AS interpreters
    ON interpreters._item_name = booking.cp_1__connect_boards6
LEFT JOIN monday.communication_professional_contacts AS preferred_interpreters
    ON preferred_interpreters._item_name = booking.preferred_cp__connect_boards3
LEFT JOIN monday.ccg_framework_locations AS ccg
    ON contacts.ccg_framework_locations__connect_boards =
       ccg._item_name
WHERE ccg.contract__status IS NOT NULL

UNION

SELECT zip_date_hour(booking_date__date, start__hour)                               AS  booking_start_datetime
     , zip_date_hour(booking_date__date, end__hour9)                                  AS  booking_end_datetime
     , zip_date_hour(deal_closed__date_confirmed8, deal_closed__date_confirmed8)       AS  deal_closed_datetime
     , creation_log__creation_log                                                      AS  request_datetime
     , booking._item_name                                                              AS  booker_ref
     , sales_contacts__connect_boards5                                                 AS  sales_contact
     , ccg.nacs_code__text4                                                            AS  practice_code
     , booking.location__location                                                          AS  location
     , ccg.contract__status                                                             AS  ccg
     , booking_type__session_notes                                                     AS  details_of_request
     , type_of_professional__type_of_professional                                      AS  language_professional
     , CASE
           WHEN preferred_cp__connect_boards3 IS NULL OR preferred_cp__connect_boards3 = '' THEN FALSE
           ELSE TRUE END                                                               AS  named_interpreter_requested
     , CASE
           WHEN preferred_cp__connect_boards3 IS NULL OR preferred_cp__connect_boards3 = '' THEN NULL
           WHEN preferred_cp__connect_boards3 = cp_1__connect_boards6 OR
                preferred_cp__connect_boards3 = cp_2__connect_boards THEN TRUE
           ELSE FALSE END                                                              AS  named_interpreter_request_met
     , CASE WHEN pref__sex___status0 = 'No preference' THEN FALSE ELSE TRUE END        AS  preferred_sex_of_interpreter_requested
     , CASE
           WHEN pref__sex___status0 = 'No preference' THEN NULL
           WHEN pref__sex___status0 = interpreters.sex__status04 THEN TRUE
           WHEN preferred_interpreters.sex__status04 = interpreters.sex__status04 THEN TRUE
           ELSE FALSE
     END                                                                         AS  sex_pref_met
     , (SELECT member__status0
        FROM monday.communication_professional_contacts
        WHERE communication_professional_contacts._item_name = cp_2__connect_boards)  AS  members_status_to_demo_how_sex_pref_met_should_work
     , interpreters.reg_number__text2                                                           AS  interpreter_ref
     , invoice_notes__notes                                                           AS  action_taken_to_investigate_summary
     , NULL AS  level_of_interpreter_met
     , CASE
           WHEN charge__status = 'Canc no fee' OR charge__status = 'Canc 50%% fee' OR
                charge__status = 'Cancelled Full Fee' THEN TRUE
           ELSE FALSE END                                                              AS  booking_cancelled
     , CASE
           WHEN charge__status = 'Canc no fee' THEN '0'
           ELSE quote_exc_vat__quote_exc_vat END                                       AS  appt_fee
     , CASE
           WHEN end__hour9 IS NULL THEN
               NULL
           WHEN EXTRACT(HOUR FROM end__hour9) = '00'
            AND EXTRACT(MINUTE FROM end__hour9) = '00' THEN
               NULL
           ELSE
               zip_date_hour(booking_date__date, end__hour9) -
               zip_date_hour(booking_date__date, start__hour)
       END                                                                             AS  length_of_appt_booked
     , zip_date_hour(booking_date__date, start__hour)                                  AS  actual_start_time
     , CASE
           WHEN actual_end_time__hour2 IS NULL THEN
               NULL
           WHEN EXTRACT(HOUR FROM actual_end_time__hour2) = '00'
            AND EXTRACT(MINUTE FROM actual_end_time__hour2) = '00' THEN
               NULL
           ELSE
               zip_date_hour(booking_date__date, actual_end_time__hour2)
       END                                                                              AS  actual_end_time
     , CASE
           WHEN actual_end_time__hour2 IS NULL THEN
               NULL
           WHEN EXTRACT(HOUR FROM actual_end_time__hour2) = '00'
            AND EXTRACT(MINUTE FROM actual_end_time__hour2) = '00' THEN
               NULL
           ELSE
               zip_date_hour(booking_date__date, actual_end_time__hour2) -
                zip_date_hour(booking_date__date, start__hour)
       END                      AS  actual_length_of_appt
FROM monday.booking_sales_pipeline_2020_21 AS booking
LEFT JOIN monday.sales_contacts AS contacts
    ON contacts._item_name = booking.sales_contacts__connect_boards5
LEFT JOIN monday.communication_professional_contacts AS interpreters
    ON interpreters._item_name = booking.cp_2__connect_boards
LEFT JOIN monday.communication_professional_contacts AS preferred_interpreters
    ON preferred_interpreters._item_name = booking.preferred_cp__connect_boards3
LEFT JOIN monday.ccg_framework_locations AS ccg
    ON contacts.ccg_framework_locations__connect_boards =
       ccg._item_name
WHERE ccg.contract__status IS NOT NULL
AND cp_2__connect_boards IS NOT NULL
AND cp_2__connect_boards != '';