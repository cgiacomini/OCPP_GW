from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://singleton:@localhost:5432/singleton-ev'  # Update with your PostgreSQL URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define ChargingStation model
class ChargingStation(db.Model):
    __tablename__ = 'charging_stations'

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(25))
    iccid = db.Column(db.String(20))
    imsi = db.Column(db.String(20))
    firmware_version = db.Column(db.String(50))
    charge_box_serial_number = db.Column(db.String(255))
    charge_point_serial_number = db.Column(db.String(255))
    meter_serial_number = db.Column(db.String(255))
    meter_type = db.Column(db.String(255))
    last_heartbeat = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50))
    vendor_name = db.Column(db.String(50))
    model = db.Column(db.String(20))
    unique_id = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<ChargingStation {self.id}>'

# Route to fetch all charging stations
@app.route('/api/charging-stations', methods=['GET'])
def get_charging_stations():
    try:
        stations = ChargingStation.query.all()
        return jsonify([{
            'id': station.id,
            'serial_number': station.serial_number,
            'iccid': station.iccid,
            'imsi': station.imsi,
            'firmware_version': station.firmware_version,
            'charge_box_serial_number': station.charge_box_serial_number,
            'charge_point_serial_number': station.charge_point_serial_number,
            'meter_serial_number': station.meter_serial_number,
            'meter_type': station.meter_type,
            'last_heartbeat': station.last_heartbeat.isoformat() if station.last_heartbeat else None,
            'status': station.status,
            'vendor_name': station.vendor_name,
            'model': station.model,
            'unique_id': station.unique_id
        } for station in stations])
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# Optionally add more routes for interacting with CSMS server

if __name__ == '__main__':
    app.run(debug=True)


