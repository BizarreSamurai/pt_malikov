CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
SELECT pg_create_physical_replication_slot('replication_slot');

\c db_telegram

CREATE TABLE e_table(
    id SERIAL PRIMARY KEY,
    email VARCHAR (100) NOT NULL
);
CREATE TABLE pn_table(
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR (100) NOT NULL
);

INSERT INTO e_table (email)
VALUES ('test@test.com'),
       ('good@win.org');

INSERT INTO pn_table (phone_number)
VALUES ('8-800-555-35-35'),
       ('+7(123)4567890');
COMMIT;
