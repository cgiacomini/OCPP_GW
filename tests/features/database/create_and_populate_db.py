import sqlite3
import json

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('charging_points.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS charging_points (
    id INTEGER PRIMARY KEY,
    charge_point_id TEXT UNIQUE NOT NULL,
    location TEXT,
    address TEXT,
    connectors TEXT,
    firmware_version TEXT,
    status TEXT,
    last_heartbeat TEXT,
    meter_value_sample_interval INTEGER,
    supported_features TEXT,
    manufacturer TEXT,
    model TEXT,
    ip_address TEXT,
    mac_address TEXT,
    public_key TEXT,
    certificate_status TEXT
)
''')

# Sample data
charging_points_data = [
    {
        "charge_point_id": "CP_1",
        "location": "POINT(12.9715987 77.5945627)",
        "address": "123 Electric Ave",
        "connectors": json.dumps([
            {"connectorId": 1, "type": "Type2", "maxCurrent": 32, "voltage": 230, "status": "Available"},
            {"connectorId": 2, "type": "CCS2", "maxCurrent": 100, "voltage": 400, "status": "Occupied"}
        ]),
        "firmware_version": "v1.0",
        "status": "Available",
        "last_heartbeat": "2024-07-02T14:00:00Z",
        "meter_value_sample_interval": 300,
        "supported_features": json.dumps({"features": ["smartCharging", "iso15118"]}),
        "manufacturer": "ChargePoint Inc.",
        "model": "Model X",
        "ip_address": "192.168.1.100",
        "mac_address": "00:1B:44:11:3A:B7",
        "public_key": "public_key_data",
        "certificate_status": "Valid"
    }
]

# Insert data into table
for cp in charging_points_data:
    cursor.execute('''
    INSERT INTO charging_points (
        charge_point_id, location, address, connectors, firmware_version, status, 
        last_heartbeat, meter_value_sample_interval, supported_features, manufacturer, 
        model, ip_address, mac_address, public_key, certificate_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        cp["charge_point_id"], cp["location"], cp["address"], cp["connectors"], cp["firmware_version"],
        cp["status"], cp["last_heartbeat"], cp["meter_value_sample_interval"], cp["supported_features"],
        cp["manufacturer"], cp["model"], cp["ip_address"], cp["mac_address"], cp["public_key"],
        cp["certificate_status"]
    ))

# Commit and close
conn.commit()
conn.close()

print("Database created and populated successfully.")
