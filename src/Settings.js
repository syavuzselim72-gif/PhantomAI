import React from 'react';
import './Settings.css';

const Settings = ({ theme, onThemeChange, onClose }) => {
  const themes = [
    { id: 'default', name: 'Varsayılan Tema', colors: ['#667eea', '#764ba2'] },
    { id: 'dark', name: 'Koyu Tema', colors: ['#2c3e50', '#34495e'] },
    { id: 'blue', name: 'Mavi Tema', colors: ['#3498db', '#2980b9'] },
    { id: 'green', name: 'Yeşil Tema', colors: ['#2ecc71', '#27ae60'] },
    { id: 'purple', name: 'Mor Tema', colors: ['#9b59b6', '#8e44ad'] },
    { id: 'orange', name: 'Turuncu Tema', colors: ['#e67e22', '#d35400'] },
    { id: 'red', name: 'Kırmızı Tema', colors: ['#e74c3c', '#c0392b'] }
  ];

  return (
    <div className="settings-overlay" onClick={onClose}>
      <div className="settings-modal" onClick={e => e.stopPropagation()}>
        <div className="settings-header">
          <h2>Ayarlar</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        
        <div className="settings-content">
          <div className="setting-group">
            <h3>Tema Seçimi</h3>
            <div className="theme-options">
              {themes.map(themeOption => (
                <div 
                  key={themeOption.id}
                  className={`theme-option ${theme === themeOption.id ? 'selected' : ''}`}
                  onClick={() => onThemeChange(themeOption.id)}
                >
                  <div 
                    className="theme-preview"
                    style={{background: `linear-gradient(135deg, ${themeOption.colors[0]} 0%, ${themeOption.colors[1]} 100%)`}}
                  ></div>
                  <span>{themeOption.name}</span>
                </div>
              ))}
            </div>
          </div>
          
          <div className="setting-group">
            <h3>Animasyon Ayarları</h3>
            <div className="checkbox-group">
              <label className="checkbox-label">
                <input type="checkbox" defaultChecked />
                <span className="checkmark"></span>
                Mesaj Animasyonları
              </label>
              <label className="checkbox-label">
                <input type="checkbox" defaultChecked />
                <span className="checkmark"></span>
                Geçiş Efektleri
              </label>
              <label className="checkbox-label">
                <input type="checkbox" defaultChecked />
                <span className="checkmark"></span>
                Hover Efektleri
              </label>
            </div>
          </div>
        </div>
        
        <div className="settings-footer">
          <button className="save-button" onClick={onClose}>Kaydet</button>
        </div>
      </div>
    </div>
  );
};

export default Settings;