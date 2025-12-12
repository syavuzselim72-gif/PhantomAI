import React, { useState } from 'react';
import axios from 'axios';
import Settings from './Settings';
import './App.css';

function App() {
  const [inputValue, setInputValue] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [theme, setTheme] = useState('default');
  const [animationSettings, setAnimationSettings] = useState({
    messageAnimations: true,
    transitionEffects: true,
    hoverEffects: true,
    floatingElements: true,
    loadingAnimations: true
  });
  const [backgroundSettings, setBackgroundSettings] = useState({
    type: 'gradient',
    gradient: 'default',
    image: '',
    color: '#ffffff'
  });

  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
  };

  const handleAnimationSettingsChange = (newSettings) => {
    setAnimationSettings(newSettings);
  };

  const handleBackgroundSettingsChange = (newSettings) => {
    setBackgroundSettings(newSettings);
  };

  const getThemeColors = () => {
    const themes = {
      default: ['#667eea', '#764ba2'],
      dark: ['#2c3e50', '#34495e'],
      blue: ['#3498db', '#2980b9'],
      green: ['#2ecc71', '#27ae60'],
      purple: ['#9b59b6', '#8e44ad'],
      orange: ['#e67e22', '#d35400'],
      red: ['#e74c3c', '#c0392b'],
      pink: ['#ff6b6b', '#ee5a24'],
      teal: ['#1dd1a1', '#10ac84'],
      indigo: ['#5f27cd', '#341f97']
    };
    return themes[theme] || themes.default;
  };

  const themeColors = getThemeColors();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputValue.trim()) return;
    
    // Add user message to chat history
    const userMessage = { text: inputValue, sender: 'user' };
    setChatHistory(prev => [...prev, userMessage]);
    
    // Clear input
    setInputValue('');
    setIsLoading(true);
    
    try {
      // Send message to backend
      const response = await axios.post('/api/chat', {
        user_input: inputValue
      });
      
      // Add bot response to chat history
      const botMessage = { text: response.data.response, sender: 'bot' };
      setChatHistory(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Hata:', error);
      const errorMessage = { text: 'Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.', sender: 'bot' };
      setChatHistory(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App" data-theme={theme}>
      {showSettings && (
        <Settings 
          theme={theme} 
          onThemeChange={handleThemeChange} 
          animationSettings={animationSettings}
          onAnimationSettingsChange={handleAnimationSettingsChange}
          backgroundSettings={backgroundSettings}
          onBackgroundSettingsChange={handleBackgroundSettingsChange}
          onClose={() => setShowSettings(false)} 
        />
      )}
      <header className="App-header">
        <div className="header-content">
          <h1>PhantomAI</h1>
          <button className="settings-button" onClick={() => setShowSettings(true)}>
            ⚙️
          </button>
        </div>
        <p className="tagline">Gelişmiş yapay zeka destekli sohbet deneyimi</p>
      </header>
      
      <div className="chat-container">
        <div className="chat-history">
          {chatHistory.length === 0 ? (
            <div className="welcome-message">
              <h2>PhantomAI'ye Hoş Geldiniz</h2>
              <p>Sohbete başlamak için aşağıya mesajınızı yazın.</p>
            </div>
          ) : (
            chatHistory.map((message, index) => (
              <div key={index} className={`message ${message.sender}-message`}>
                <div className="message-content">
                  {message.text}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="message bot-message loading">
              <div className="message-content">
                <div className="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
        </div>
        
        <form onSubmit={handleSubmit} className="chat-form">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Mesajınızı buraya yazın..."
            required
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Gönderiliyor...' : 'Gönder'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;