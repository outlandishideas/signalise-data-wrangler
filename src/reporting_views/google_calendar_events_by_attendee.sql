CREATE OR REPLACE VIEW reporting.events_by_attendee AS
(
select event_id, attendees ->> 'email' as email, start_time, end_time, summary, description
from (
         select id                              as event_id,
                start_datetime  as start_time,
                end_datetime            as end_time,
                jsonb_array_elements(attendees) as attendees,
                summary,
                description
         from gsuite.events
         where jsonb_typeof(attendees) = 'array') as event_attendees

    );
