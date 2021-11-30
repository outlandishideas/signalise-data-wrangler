DROP SCHEMA IF EXISTS ideal CASCADE;
CREATE SCHEMA IF NOT EXISTS ideal;

CREATE TYPE ideal.contracting_organisation_type AS ENUM ('CCG', 'University', 'other');

CREATE TABLE ideal.contracting_organisation
(
    id   INT PRIMARY KEY,
    name TEXT,
    type ideal.contracting_organisation_type,
    invoice_address TEXT
);


CREATE TYPE ideal.sex_preference AS ENUM ('No preference', 'Female', 'Male');

CREATE TABLE ideal.deaf_user
(
    id              INT PRIMARY KEY,
    name            TEXT,
    email           TEXT,
    phone_number    TEXT,
    sex_pref        ideal.sex_preference,
    notes           TEXT,
    is_service_user bool
);

CREATE TABLE ideal.signalise_staff
(
    id    INT PRIMARY KEY,
    email TEXT,
    name  TEXT
);

CREATE TABLE ideal.area
(
    id     INT PRIMARY KEY,
    name   TEXT,
    region TEXT
);

CREATE TABLE ideal.communication_professional
(
    id                                   INT PRIMARY KEY,
    name                                 TEXT,
    notes                                TEXT,
    alert                                TEXT,
    email                                TEXT,
    phone_number                         TEXT,
    is_rsli                              bool,
    is_tsli                              bool,
    is_lipspeaker                        bool,
    is_rbsli                             bool,
    reg_number                           TEXT,
    reg_expiry                           DATE,
    valid_insurance_doc                  bool,
    insurance_expiry                     DATE,
    dbs_issue_date                       DATE,
    dbs_expiry_date                      DATE,
    dbs_certificate_number               TEXT,
    is_subscribed_to_dbs_update_service  bool,
    dbs_update_service_last_checked_date bool,
    dbs_update_service_last_checked_by   INT,
    FOREIGN KEY (dbs_update_service_last_checked_by) REFERENCES ideal.signalise_staff,
    lone_working_policy_sent             DATE,
    lone_working_policy_confirmed        bool,
    main_area_id                         INT,
    FOREIGN KEY (main_area_id) REFERENCES ideal.area
);

CREATE TABLE ideal.qualification
(
    id             INT PRIMARY KEY,
    name           TEXT,
    nvq_equivalent INT
);

CREATE TABLE ideal.communications_professional_qualifications
(
    communication_professional_id INT,
    FOREIGN KEY (communication_professional_id) REFERENCES ideal.communication_professional,
    qualification_id              INT,
    FOREIGN KEY (qualification_id) REFERENCES ideal.qualification,
    qualification_notes           TEXT
);

CREATE TABLE ideal.communications_professional_area
(
    communication_professional_id INT,
    FOREIGN KEY (communication_professional_id) REFERENCES ideal.communication_professional,
    area_id                       INT,
    FOREIGN KEY (area_id) REFERENCES ideal.area
);




CREATE TABLE ideal.deaf_user_preferred_communication_professional
(
    deaf_user_id                  INT,
    FOREIGN KEY (deaf_user_id) REFERENCES ideal.deaf_user,
    communication_professional_id INT,
    FOREIGN KEY (communication_professional_id) REFERENCES ideal.communication_professional
);

CREATE TYPE ideal.sales_contacts_type AS ENUM ('Contract', 'Contact', 'Sales Qualified Lead', 'Lead');

CREATE TABLE ideal.sales_contacts
(
    id        INT PRIMARY KEY,
    name      TEXT,
    email     TEXT,
    phone     TEXT,
    job_title TEXT,
    type ideal.sales_contacts_type,
    notes TEXT,
    contracting_organisation_id INT,
    FOREIGN KEY (contracting_organisation_id) REFERENCES ideal.contracting_organisation
);

CREATE TABLE ideal.locations
(
    id                          INT PRIMARY KEY,
    name                        TEXT,
    lat                         FLOAT,
    lon                         FLOAT,
    address                     TEXT,
    postcode                    TEXT,
    phone                       TEXT,
    nhs_net_email               TEXT,
    nacs_code                   TEXT,
    sales_contact_id            INT,
    FOREIGN KEY (sales_contact_id) REFERENCES ideal.sales_contacts,
    contracting_organisation_id INT,
    FOREIGN KEY (contracting_organisation_id) REFERENCES ideal.contracting_organisation
);



CREATE TABLE ideal.enquiry
(
    id                          INT PRIMARY KEY,
    enquiry_made                timestamp,
    booking_start               timestamp,
    booking_end                 timestamp,
    contracting_organisation_id INT,
    FOREIGN KEY (contracting_organisation_id) REFERENCES ideal.contracting_organisation,
    location_id                 INT,
    FOREIGN KEY (location_id) REFERENCES ideal.locations,
    sales_contact_id            INT,
    FOREIGN KEY (sales_contact_id) REFERENCES ideal.sales_contacts,
    estimated_number_professionals_needed INT,
    requested

);


CREATE TABLE ideal.booking
(
    id                            INT PRIMARY KEY,
    enquiry_id                    INT,
    FOREIGN KEY (enquiry_id) REFERENCES ideal.enquiry,
    communication_professional_id INT,
    FOREIGN KEY (communication_professional_id) REFERENCES ideal.communication_professional,
    actual_start_time             timestamp,
    actual_end_time               timestamp
);

CREATE TABLE ideal.enquiry_deaf_user
(
    enquiry_id   INT,
    FOREIGN KEY (enquiry_id) REFERENCES ideal.enquiry,
    deaf_user_id INT,
    FOREIGN KEY (deaf_user_id) REFERENCES ideal.deaf_user
);


CREATE TABLE ideal.invoices_to_send (
  id INT PRIMARY KEY,
  enquiry_id INT,
  FOREIGN KEY (enquiry_id) REFERENCES ideal.enquiry,
  sent timestamp,
  paid timestamp
);

CREATE TABLE ideal.invoices_to_pay (
  id INT PRIMARY KEY,
  booking_id INT,
  FOREIGN KEY (booking_id) REFERENCES ideal.booking,
  received timestamp,
  paid timestamp
);

