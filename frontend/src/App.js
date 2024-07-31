// App.js
import React, { useState } from 'react';
import './App.css';
import RightPanel from './components/RightPanel';

const App = () => {
  const [selectedMenu, setSelectedMenu] = useState('stations'); // 'stations' is the initial selected menu
  const [chargingStations, setChargingStations] = useState([]);
  const [version] = useState('1.0.0'); // Replace with actual version if available

  const fetchChargingStations = async () => {
    try {
      // Simulate fetching data from server
      const response = await fetch('http://localhost:5000/api/charging-stations');
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      setChargingStations(data);
    } catch (error) {
      console.error('Error fetching charging stations:', error);
    }
  };

  const handleMenuClick = (menu) => {
    setSelectedMenu(menu);
    if (menu === 'stations') {
      fetchChargingStations();
    }
  };

  return (
    <div className="App">
      <div className="left-menu">
        <button onClick={() => handleMenuClick('stations')}>Stations</button>
        <button onClick={() => handleMenuClick('about')}>About</button>
      </div>
      <RightPanel selectedMenu={selectedMenu} chargingStations={chargingStations} version={version} />
    </div>
  );
};

export default App;

