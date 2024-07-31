import sqlite3
import json

def update_connector_status(charge_point_id, connector_id, new_status):
    # Connect to SQLite database
    conn = sqlite3.connect('charging_points.db')
    cursor = conn.cursor()

    # Fetch the current connectors data
    cursor.execute('SELECT connectors FROM charging_points WHERE charge_point_id = ?', (charge_point_id,))
    result = cursor.fetchone()

    if result:
        connectors = json.loads(result[0])
        
        # Update the status of the specified connector
        for connector in connectors:
            if connector['connectorId'] == connector_id:
                connector['status'] = new_status
                break

        # Update the database with the new connectors data
        cursor.execute('UPDATE charging_points SET connectors = ? WHERE charge_point_id = ?',
                       (json.dumps(connectors), charge_point_id))
        conn.commit()
        print(f"Connector {connector_id} status updated to {new_status} for charge point {charge_point_id}.")
    else:
        print(f"No data found for charge point ID: {charge_point_id}")

    # Close the connection
    conn.close()

# Example usage
update_connector_status('CP_1', 2, 'Faulted')

