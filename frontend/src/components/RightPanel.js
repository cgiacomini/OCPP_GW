// RightPanel.js
import React from 'react';

const RightPanel = ({ selectedMenu, chargingStations, version }) => {
  return (
    <div className="right-panel">
      <h1>Singleton-ev</h1>
      {selectedMenu === 'stations' && (
        <div>
          <h2>Charging Stations</h2>
          <table className="stations-table">
            <thead>
              <tr>
                <th>Serial Number</th>
                <th>ICCID</th>
                <th>IMSI</th>
                <th>Firmware Version</th>
                <th>Charge Box Serial Number</th>
                <th>Charge Point Serial Number</th>
                <th>Meter Serial Number</th>
                <th>Meter Type</th>
                <th>Last Heartbeat</th>
                <th>Status</th>
                <th>Vendor Name</th>
                <th>Model</th>
                <th>Unique ID</th>
              </tr>
            </thead>
            <tbody>
              {chargingStations.map(station => (
                <tr key={station.id}>
                  <td>{station.serial_number}</td>
                  <td>{station.iccid}</td>
                  <td>{station.imsi}</td>
                  <td>{station.firmware_version}</td>
                  <td>{station.charge_box_serial_number}</td>
                  <td>{station.charge_point_serial_number}</td>
                  <td>{station.meter_serial_number}</td>
                  <td>{station.meter_type}</td>
                  <td>{station.last_heartbeat}</td>
                  <td>{station.status}</td>
                  <td>{station.vendor_name}</td>
                  <td>{station.model}</td>
                  <td>{station.unique_id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedMenu === 'about' && (
        <div>
          <h2>About</h2>
          <p>Version: {version}</p>
        </div>
      )}
    </div>
  );
};

export default RightPanel;

