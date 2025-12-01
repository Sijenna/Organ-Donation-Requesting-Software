-- -----------------------------------------------------
-- Database: organ_donation_and_requesting_software
-- -----------------------------------------------------

CREATE DATABASE IF NOT EXISTS organ_donation_and_requesting_software;
USE organ_donation_and_requesting_software;

-- -----------------------------------------------------
-- Table: HOSPITALS
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS HOSPITALS (
    Hospital_ID VARCHAR(100) UNIQUE,
    H_password VARCHAR(15) PRIMARY KEY,
    Hospital_Name VARCHAR(50) NOT NULL,
    Hospital_Location VARCHAR(100) NOT NULL,
    Contact_No DECIMAL(10)
);

-- -----------------------------------------------------
-- Table: REQUESTS
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS REQUESTS (
    From_hosp_ID VARCHAR(100),
    To_hosp_ID VARCHAR(100),
    recipient_ID INT,
    donor_ID INT,
    checked_NOT_checked ENUM('checked', 'NOT checked') DEFAULT 'NOT checked'
);

-- -----------------------------------------------------
-- Table: CONFIRMATION
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS CONFIRMATION (
    From_hosp_ID VARCHAR(100),
    To_hosp_ID VARCHAR(100),
    Confirm_availability ENUM('Available','Not Available','Reserved') NOT NULL,
    checked_NOT_checked ENUM('checked','NOT checked') NOT NULL,
    recipient_ID INT,
    donor_ID INT
);
