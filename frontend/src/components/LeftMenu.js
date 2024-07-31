// components/LeftMenu.js
import React from 'react';
import '../App.css';

const LeftMenu = ({ onSelect }) => {
    return (
        <div className="left-menu">
            <div className="menu-item" onClick={() => onSelect('stations')}>
                Stations
            </div>
            <div className="menu-item" onClick={() => onSelect('about')}>
                About
            </div>
        </div>
    );
};

export default LeftMenu;

