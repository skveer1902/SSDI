import React from 'react';
import './PersonIcon.css';

export default function PersonIcon({ small }) {
  return (
    <div className={`person-icon ${small ? 'small' : ''}`}>
      <div className="head"></div>
      <div className="body"></div>
    </div>
  );
}
