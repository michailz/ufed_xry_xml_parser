-- Adminer 4.7.7 PostgreSQL dump

DROP TABLE IF EXISTS "accounts";
DROP SEQUENCE IF EXISTS accounts_id_seq;
CREATE SEQUENCE accounts_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."accounts" (
    "id" bigint DEFAULT nextval('accounts_id_seq') NOT NULL,
    "related_application" character varying(255) NOT NULL,
    "information_id" bigint NOT NULL,
    "file_id" bigint NOT NULL
) WITH (oids = false);


DROP TABLE IF EXISTS "devices";
DROP SEQUENCE IF EXISTS devices_id_seq;
CREATE SEQUENCE devices_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."devices" (
    "id" integer DEFAULT nextval('devices_id_seq') NOT NULL,
    "file_id" bigint NOT NULL,
    "information_id" bigint NOT NULL,
    "key" character varying(100) NOT NULL,
    "value" character varying(255) NOT NULL
) WITH (oids = false);


DROP TABLE IF EXISTS "fields";
DROP SEQUENCE IF EXISTS fields_id_seq1;
CREATE SEQUENCE fields_id_seq1 INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."fields" (
    "id" integer DEFAULT nextval('fields_id_seq1') NOT NULL,
    "account_id" bigint NOT NULL,
    "related_application" character varying(255) NOT NULL,
    "type" character varying(255) NOT NULL,
    "value" text NOT NULL
) WITH (oids = false);


DROP TABLE IF EXISTS "files";
DROP SEQUENCE IF EXISTS files_id_seq;
CREATE SEQUENCE files_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."files" (
    "id" bigint DEFAULT nextval('files_id_seq') NOT NULL,
    "md5" character varying(50) NOT NULL,
    "parsing_time" timestamp NOT NULL,
    "case_examiner_name" character varying(50),
    "case_number" character varying(50),
    "device_info_creation_time" timestamp,
    "file_name" character varying(100) NOT NULL,
    "processed" boolean DEFAULT false NOT NULL,
    CONSTRAINT "files_md5" UNIQUE ("md5")
) WITH (oids = false);


DROP TABLE IF EXISTS "information";
DROP SEQUENCE IF EXISTS information_id_seq;
CREATE SEQUENCE information_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."information" (
    "id" integer DEFAULT nextval('information_id_seq') NOT NULL,
    "description" text NOT NULL,
    "file_id" bigint,
    "information_timestamp" timestamp NOT NULL
) WITH (oids = false);


DROP TABLE IF EXISTS "relations";
DROP SEQUENCE IF EXISTS contacts_id_seq;
CREATE SEQUENCE contacts_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."relations" (
    "id" integer DEFAULT nextval('contacts_id_seq') NOT NULL,
    "information_id" bigint NOT NULL,
    "source_account_id" bigint,
    "contact_account_id" bigint,
    "file_id" bigint NOT NULL
) WITH (oids = false);


-- 2021-05-03 08:31:22.276751+00
