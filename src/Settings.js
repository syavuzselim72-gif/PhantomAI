import React, { useState } from 'react';
import './Settings.css';

const Settings = ({ 
  theme, 
  onThemeChange, 
  animationSettings,
  onAnimationSettingsChange,
  backgroundSettings,
  onBackgroundSettingsChange,
  onClose 
}) => {
  const [localAnimationSettings, setLocalAnimationSettings] = useState(animationSettings || {
    messageAnimations: true,
    transitionEffects: true,
    hoverEffects: true,
    floatingElements: true,
    loadingAnimations: true
  });
  
  const [localBackgroundSettings, setLocalBackgroundSettings] = useState(backgroundSettings || {
    type: 'gradient',
    gradient: 'default',
    image: '',
    color: '#ffffff'
  });

  const themes = [
    { id: 'default', name: 'Varsayılan Tema', colors: ['#667eea', '#764ba2'] },
    { id: 'dark', name: 'Koyu Tema', colors: ['#2c3e50', '#34495e'] },
    { id: 'blue', name: 'Mavi Tema', colors: ['#3498db', '#2980b9'] },
    { id: 'green', name: 'Yeşil Tema', colors: ['#2ecc71', '#27ae60'] },
    { id: 'purple', name: 'Mor Tema', colors: ['#9b59b6', '#8e44ad'] },
    { id: 'orange', name: 'Turuncu Tema', colors: ['#e67e22', '#d35400'] },
    { id: 'red', name: 'Kırmızı Tema', colors: ['#e74c3c', '#c0392b'] },
    { id: 'pink', name: 'Pembe Tema', colors: ['#ff6b6b', '#ee5a24'] },
    { id: 'teal', name: 'Turkuaz Tema', colors: ['#1dd1a1', '#10ac84'] },
    { id: 'indigo', name: 'Çivit Mavi Tema', colors: ['#5f27cd', '#341f97'] }
  ];

  const gradients = [
    { id: 'default', name: 'Varsayılan Gradient', colors: ['#667eea', '#764ba2'] },
    { id: 'sunset', name: 'Gün Batımı', colors: ['#ff9a9e', '#fecfef'] },
    { id: 'ocean', name: 'Okyanus', colors: ['#667eea', '#764ba2'] },
    { id: 'forest', name: 'Orman', colors: ['#11998e', '#38ef7d'] },
    { id: 'midnight', name: 'Gece Yarısı', colors: ['#2c3e50', '#4ca1af'] }
  ];

  const handleAnimationChange = (setting) => {
    const newSettings = { ...localAnimationSettings, [setting]: !localAnimationSettings[setting] };
    setLocalAnimationSettings(newSettings);
    onAnimationSettingsChange(newSettings);
  };

  const handleBackgroundTypeChange = (type) => {
    const newSettings = { ...localBackgroundSettings, type };
    setLocalBackgroundSettings(newSettings);
    onBackgroundSettingsChange(newSettings);
  };

  const handleGradientChange = (gradientId) => {
    const newSettings = { ...localBackgroundSettings, gradient: gradientId };
    setLocalBackgroundSettings(newSettings);
    onBackgroundSettingsChange(newSettings);
  };

  return (
    <div className="settings-overlay" onClick={onClose}>
      <div className="settings-modal" onClick={e => e.stopPropagation()}>
        <div className="settings-header">
          <h2>Ayarlar</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        
        <div className="settings-content">
          {/* Tema Seçimi */}
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
          
          {/* Arkaplan Ayarları */}
          <div className="setting-group">
            <h3>Arkaplan Ayarları</h3>
            <div className="radio-group">
              <label className="radio-label">
                <input 
                  type="radio" 
                  name="background-type" 
                  checked={localBackgroundSettings.type === 'gradient'}
                  onChange={() => handleBackgroundTypeChange('gradient')}
                />
                <span className="radio-checkmark"></span>
                Gradient Arkaplan
              </label>
              <label className="radio-label">
                <input 
                  type="radio" 
                  name="background-type" 
                  checked={localBackgroundSettings.type === 'color'}
                  onChange={() => handleBackgroundTypeChange('color')}
                />
                <span className="radio-checkmark"></span>
                Düz Renk
              </label>
              <label className="radio-label">
                <input 
                  type="radio" 
                  name="background-type" 
                  checked={localBackgroundSettings.type === 'image'}
                  onChange={() => handleBackgroundTypeChange('image')}
                />
                <span className="radio-checkmark"></span>
                Görsel Arkaplan
              </label>
            </div>
            
            {localBackgroundSettings.type === 'gradient' && (
              <div className="gradient-options">
                <h4>Gradient Seçimi</h4>
                <div className="theme-options">
                  {gradients.map(gradient => (
                    <div 
                      key={gradient.id}
                      className={`theme-option ${localBackgroundSettings.gradient === gradient.id ? 'selected' : ''}`}
                      onClick={() => handleGradientChange(gradient.id)}
                    >
                      <div 
                        className="theme-preview"
                        style={{background: `linear-gradient(135deg, ${gradient.colors[0]} 0%, ${gradient.colors[1]} 100%)`}}
                      ></div>
                      <span>{gradient.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            {localBackgroundSettings.type === 'color' && (
              <div className="color-picker">
                <h4>Renk Seçimi</h4>
                <input 
                  type="color" 
                  value={localBackgroundSettings.color}
                  onChange={(e) => {
                    const newSettings = { ...localBackgroundSettings, color: e.target.value };
                    setLocalBackgroundSettings(newSettings);
                    onBackgroundSettingsChange(newSettings);
                  }}
                />
              </div>
            )}
            
            {localBackgroundSettings.type === 'image' && (
              <div className="image-upload">
                <h4>Görsel Yükle</h4>
                <input 
                  type="text" 
                  placeholder="Görsel URL'si girin"
                  value={localBackgroundSettings.image}
                  onChange={(e) => {
                    const newSettings = { ...localBackgroundSettings, image: e.target.value };
                    setLocalBackgroundSettings(newSettings);
                    onBackgroundSettingsChange(newSettings);
                  }}
                />
              </div>
            )}
          </div>
          
          {/* Animasyon Ayarları */}
          <div className="setting-group">
            <h3>Animasyon Ayarları</h3>
            <div className="checkbox-group">
              <label className="checkbox-label">
                <input 
                  type="checkbox" 
                  checked={localAnimationSettings.messageAnimations}
                  onChange={() => handleAnimationChange('messageAnimations')}
                />
                <span className="checkmark"></span>
                Mesaj Animasyonları
              </label>
              <label className="checkbox-label">
                <input 
                  type="checkbox" 
                  checked={localAnimationSettings.transitionEffects}
                  onChange={() => handleAnimationChange('transitionEffects')}
                />
                <span className="checkmark"></span>
                Geçiş Efektleri
              </label>
              <label className="checkbox-label">
                <input 
                  type="checkbox" 
                  checked={localAnimationSettings.hoverEffects}
                  onChange={() => handleAnimationChange('hoverEffects')}
                />
                <span className="checkmark"></span>
                Hover Efektleri
              </label>
              <label className="checkbox-label">
                <input 
                  type="checkbox" 
                  checked={localAnimationSettings.floatingElements}
                  onChange={() => handleAnimationChange('floatingElements')}
                />
                <span className="checkmark"></span>
                Yüzen Elementler
              </label>
              <label className="checkbox-label">
                <input 
                  type="checkbox" 
                  checked={localAnimationSettings.loadingAnimations}
                  onChange={() => handleAnimationChange('loadingAnimations')}
                />
                <span className="checkmark"></span>
                Yükleme Animasyonları
              </label>
            </div>
          </div>
          
          {/* Diğer Ayarlar */}
          <div className="setting-group">
            <h3>Diğer Ayarlar</h3>
            <div className="checkbox-group">
              <label className="checkbox-label">
                <input type="checkbox" defaultChecked />
                <span className="checkmark"></span>
                Karanlık Mod
              </label>
              <label className="checkbox-label">
                <input type="checkbox" defaultChecked />
                <span className="checkmark"></span>
                Bildirim Sesleri
              </label>
              <label className="checkbox-label">
                <input type="checkbox" defaultChecked />
                <span className="checkmark"></span>
                Otomatik Kaydırma
              </label>
            </div>
          </div>
        </div>
        
        <div className="settings-footer">
          <button className="reset-button" onClick={() => {
            // Reset settings logic
          }}>Sıfırla</button>
          <button className="save-button" onClick={onClose}>Kaydet</button>
        </div>
      </div>
    </div>
  );
};

export default Settings;