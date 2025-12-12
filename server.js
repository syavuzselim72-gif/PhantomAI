const express = require('express');
const cors = require('cors');
const axios = require('axios');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3006;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Serve static files from the React app build directory
app.use(express.static(path.join(__dirname, 'build')));

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Chat endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const { user_input } = req.body;
    
    if (!user_input) {
      return res.status(400).json({ error: 'Kullanıcı girişi gereklidir' });
    }
    
    // Log the incoming request
    console.log(`Processing message: ${user_input}`);
    
    // Call Mistral API
    const response = await axios.post(
      'https://api.mistral.ai/v1/chat/completions',
      {
        model: 'mistral-tiny',
        messages: [{ role: 'system', content: 'Sen Türkçe konuşan, samimi ve profesyonel bir yapay zeka asistansın. Lütfen tüm yanıtlarını Türkçe olarak ver. Yanıtlarında sadece gerçekten gerekli olduğunda İngilizce kelimeler kullan. Kullanıcıya her zaman nazik ve yardımcı ol. Mümkünse teknik terimleri Türkçe karşılıklarıyla ifade et.' }, { role: 'user', content: user_input }]
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${process.env.MISTRAL_API_KEY}`
        },
        timeout: 30000 // 30 second timeout
      }
    );
    
    const botResponse = response.data.choices[0].message.content;
    console.log(`Response sent: ${botResponse.substring(0, 50)}...`);
    res.json({ response: botResponse });
  } catch (error) {
    console.error('Mistral API çağrısında hata oluştu:', error.message);
    
    // More detailed error handling
    if (error.response) {
      // The request was made and the server responded with a status code
      console.error('Error response data:', error.response.data);
      console.error('Error response status:', error.response.status);
      res.status(error.response.status).json({ 
        error: 'Mistral API hatası oluştu', 
        details: error.response.data 
      });
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received:', error.request);
      res.status(500).json({ 
        error: 'Mistral API\'den yanıt alınamadı', 
        details: 'Zaman aşımı veya bağlantı hatası' 
      });
    } else {
      // Something happened in setting up the request
      console.error('Error setting up request:', error.message);
      res.status(500).json({ 
        error: 'İstek hazırlanırken hata oluştu', 
        details: error.message 
      });
    }
  }
});

// Catchall handler: send back React's index.html file for any non-API routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`PhantomAI sunucusu ${PORT} portunda çalışıyor`);
  console.log(`Yerel erişim: http://localhost:${PORT}`);
});