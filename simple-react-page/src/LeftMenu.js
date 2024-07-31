import React from 'react';
import './App.css';

const LeftMenu = ({ onOkClick, onNokClick }) => {
    return (
        <div className="left-menu">
            <div className="menu-button" onClick={onOkClick}>OK</div>
            <div className="menu-button" onClick={onNokClick}>NOK</div>
        </div>
    );
};

export default LeftMenu;

