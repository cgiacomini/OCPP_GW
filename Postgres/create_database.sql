--- Clean up
DROP TABLE IF EXISTS charging_stations;
DROP DATABASE IF EXISTS ":dbname";
DROP USER IF EXISTS ":user";

-- Create database and user
CREATE DATABASE ":dbname";
CREATE USER :user WITH PASSWORD :password;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ":dbname" TO :user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO :user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO :user;

\connect ":dbname";

-- Create table
CREATE TABLE IF NOT EXISTS "charging_stations" (
    id SERIAL PRIMARY KEY,
    serial_number VARCHAR(25),
    iccid VARCHAR(20),
    imsi VARCHAR(20),
    firmware_version VARCHAR(50),
    charge_box_serial_number VARCHAR(255),
    charge_point_serial_number VARCHAR(255),
    meter_serial_number VARCHAR(255),
    meter_type VARCHAR(255),
    last_heartbeat TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    vendor_name VARCHAR(50) NOT NULL,
    model VARCHAR(20) NOT NULL,
    unique_id VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS connectors (
    id SERIAL PRIMARY KEY,
    charging_station_id INTEGER REFERENCES charging_stations(id) ON DELETE CASCADE,
    connector_id INTEGER NOT NULL, 
    status VARCHAR(50) NOT NULL,
    error_code VARCHAR(50),
    last_status_update TIMESTAMP, 
    connector_type VARCHAR(50) NOT NULL,
    power_type VARCHAR(50),
    power_rating INTEGER,
    voltage INTEGER,
    current INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(charging_station_id, connector_id)
);


-- Insert into charging_stations table
INSERT INTO charging_stations (serial_number, iccid, imsi, firmware_version, charge_box_serial_number, charge_point_serial_number, meter_serial_number, meter_type, last_heartbeat, status, vendor_name, model, unique_id) VALUES
('SN1234567890', 'ICCID1234567890', 'IMSI1234567890', 'v1.0.0', 'CBSN123456', 'CPSN123456', 'MSN123456', 'TypeA', '2024-07-05 10:00:00', 'Available', 'VendorA', 'ModelA', 'CP_1'),
('SN1234567891', 'ICCID1234567891', 'IMSI1234567891', 'v1.0.1', 'CBSN123457', 'CPSN123457', 'MSN123457', 'TypeB', '2024-07-05 11:00:00', 'Occupied', 'VendorB', 'ModelB', 'CP_2'),
('SN1234567892', 'ICCID1234567892', 'IMSI1234567892', 'v1.0.2', 'CBSN123458', 'CPSN123458', 'MSN123458', 'TypeC', '2024-07-05 12:00:00', 'Faulted', 'VendorC', 'ModelC', 'CP_3');

-- Insert into connectors table for the first charging station
INSERT INTO connectors (charging_station_id, connector_id, status, error_code, last_status_update, connector_type, power_type, power_rating, voltage, current) VALUES
(1, 1, 'Available', NULL, '2024-07-05 10:00:00', 'Type 2', 'AC', 22, 230, 32),
(1, 2, 'Available', NULL, '2024-07-05 10:05:00', 'CHAdeMO', 'DC', 50, 400, 125);

-- Insert into connectors table for the second charging station
INSERT INTO connectors (charging_station_id, connector_id, status, error_code, last_status_update, connector_type, power_type, power_rating, voltage, current) VALUES
(2, 1, 'Available', NULL, '2024-07-05 11:00:00', 'Type 1', 'AC', 7, 230, 16),
(2, 2, 'Available', NULL, '2024-07-05 11:05:00', 'CCS', 'DC', 100, 500, 200);

-- Insert into connectors table for the third charging station
INSERT INTO connectors (charging_station_id, connector_id, status, error_code, last_status_update, connector_type, power_type, power_rating, voltage, current) VALUES
(3, 1, 'Available', NULL, '2024-07-05 12:00:00', 'Type 2', 'AC', 11, 230, 16),
(3, 2, 'Available', NULL, '2024-07-05 12:05:00', 'CHAdeMO', 'DC', 62, 400, 150);

