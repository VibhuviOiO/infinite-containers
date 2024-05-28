CREATE USER postgress WITH PASSWORD 'postgress';
CREATE DATABASE pdata;
GRANT ALL PRIVILEGES ON DATABASE pdata TO ct;

CREATE SEQUENCE IF NOT EXISTS recipient_seq
    START WITH 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

CREATE TABLE IF NOT EXISTS recipient
(
    id                      BIGINT                   NOT NULL,
    recipient_id            VARCHAR(255)             NOT NULL,
    first_name              VARCHAR(255)             NOT NULL,
    middle_name             VARCHAR(255)             NOT NULL,
    last_name               VARCHAR(255)             NOT NULL,
    CONSTRAINT recipient_pk PRIMARY KEY (id)
);