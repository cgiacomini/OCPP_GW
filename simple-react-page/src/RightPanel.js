import React from 'react';
import './App.css';

const RightPanel = ({ data }) => {
    return (
        <div className="right-panel">
            <h2>Scrolled List Header</h2>
            <div className="scrolled-list">
                <ul>
                    {data.map(item => (
                        <li key={item.id}>{item.name}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default RightPanel;

