import sqlite3
import json

# Connect to SQLite database
conn = sqlite3.connect('charging_points.db')
cursor = conn.cursor()

# Query the database
cursor.execute('SELECT * FROM charging_points WHERE charge_point_id = ?', ('CP_1',))
result = cursor.fetchone()

# Check if the result is not None
if result:
    # Unpack the result
    (id, charge_point_id, location, address, connectors, firmware_version, status, 
     last_heartbeat, meter_value_sample_interval, supported_features, manufacturer, 
     model, ip_address, mac_address, public_key, certificate_status) = result

    # Print the results
    print(f"ID: {id}")
    print(f"Charge Point ID: {charge_point_id}")
    print(f"Location: {location}")
    print(f"Address: {address}")
    print(f"Connectors: {json.loads(connectors)}")
    print(f"Firmware Version: {firmware_version}")
    print(f"Status: {status}")
    print(f"Last Heartbeat: {last_heartbeat}")
    print(f"Meter Value Sample Interval: {meter_value_sample_interval}")
    print(f"Supported Features: {json.loads(supported_features)}")
    print(f"Manufacturer: {manufacturer}")
    print(f"Model: {model}")
    print(f"IP Address: {ip_address}")
    print(f"MAC Address: {mac_address}")
    print(f"Public Key: {public_key}")
    print(f"Certificate Status: {certificate_status}")
else:
    print("No data found for the specified charge point ID.")

# Close the connection
conn.close()

