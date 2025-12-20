# PhantomAI Chatbot

Modern web ve desktop tabanlı Türkçe chatbot uygulaması. HTML/CSS/JavaScript frontend, FastAPI backend ve Tkinter desktop uygulaması.

## Kurulum

1. Python 3.8+ yüklü olduğundan emin olun.
2. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. `.env` dosyasında Mistral AI API anahtarınızı ayarlayın:
   ```env
   MISTRAL_API_KEY=your_actual_api_key_here
   SERVER_URL=http://localhost:8001
   ```

## Çalıştırma

### Backend Server (Diğer cihazların bağlanabilmesi için)
```bash
python server.py
```
Server `0.0.0.0:8001` adresinde çalışır ve ağdaki tüm cihazlar bağlanabilir.

### Web Arayüzü
Web tarayıcınızda açın:
```
http://localhost:8001/static/index.html
```
Veya ağdaki diğer cihazlardan:
```
http://[SUNUCU_IP_ADRESI]:8001/static/index.html
```

### Desktop Uygulaması
```bash
python main.py
```
Desktop uygulaması otomatik olarak server'a bağlanır ve ayarlar menüsünden bağlantıyı değiştirebilirsiniz.

## Ağ Bağlantısı

Diğer cihazların bağlanabilmesi için:

1. **Firewall'u açın**: Port 8001'i açın
2. **IP adresinizi öğrenin**: `ipconfig` (Windows) veya `ifconfig` (Linux/Mac)
3. **Server'ı başlatın**: `python server.py`
4. **Bağlanın**: `http://[SUNUCU_IP]:8001/static/index.html`

### Desktop Uygulaması Ağ Ayarları

Desktop uygulamasında:
- **Ayarlar > Server Bağlantısı** menüsüne gidin
- Host/IP'yi değiştirin (örneğin: `192.168.1.100`)
- "Yerel IP adresini kullan" seçeneğini işaretleyin
- Port'u ayarlayın (varsayılan: 8001)

## Özellikler

### Web Arayüzü
- **Modern Web UI**: Şık gradient tasarım, animasyonlar
- **Responsive Tasarım**: Mobil uyumlu
- **Gerçek Zamanlı Chat**: AJAX ile anlık mesajlaşma
- **Türkçe AI**: PhantomAI kişiliği
- **Hata Yönetimi**: Bağlantı ve API hatalarını yakalar
- **Typing Animasyonu**: Karakter karakter görünen metin
- **Kod Blokları**: Otomatik sözdizimi renklendirmesi
- **GitHub Yayın**: Tek dosya olarak yayınlanabilir

## GitHub'da Yayınlama

`static/index.html` dosyasını GitHub'da tek başına yayınlayabilirsiniz:

1. **Dosyayı düzenleyin**: `static/index.html` içinde `window.SERVER_URL` değişkenini değiştirin
2. **GitHub'a yükleyin**: Dosyayı GitHub repository'sine ekleyin
3. **GitHub Pages'i etkinleştirin**: Repository ayarlarından Pages'i açın
4. **URL'yi paylaşın**: Oluşan GitHub Pages URL'sini kullanın

### Örnek Server URL Ayarı:
```javascript
// GitHub Pages'ten yayınlarken
window.SERVER_URL = 'http://192.168.1.101:8001'; // Server IP'nizi yazın

// Veya domain kullanıyorsanız
window.SERVER_URL = 'https://your-server.com';
```

### Desktop Uygulaması - NEON EDITION 🌟
```bash
python main.py
```
- **Otomatik Server Algılama**: Açıldığında otomatik olarak server'ı bulur
- **Akıllı IP Taraması**: Aynı ağdaki tüm cihazları tarar
- **Neon Tasarım**: Koyu arka plan, neon renkler (pembe, cyan, turuncu)
- **Particle Efektleri**: Hareketli yıldız/partikül animasyonları
- **Glow Efektleri**: Işık saçan butonlar ve metinler
- **Animasyonlar**: Yazma göstergesi, hover efektleri, pulsing durum noktası
- **Modern UI**: Card tabanlı tasarım, gradient efektler

**Otomatik Çalışma:**
1. Uygulama açılır → Otomatik server arama başlar
2. Localhost denenir → Ağ taraması yapılır
3. Server bulunursa → Otomatik bağlanır
4. Bulunamazsa → Manuel giriş için hazır olur

**Özellikler:**
- 🎨 **Neon Renk Paleti**: #ff0080, #00ffff, #ff8000, #8000ff, #00ff80
- ✨ **Particle Sistemi**: 60 FPS animasyonlu arka plan efektleri
- 💫 **Glow Efektleri**: Işık saçan UI öğeleri
- 🎯 **Hover Animasyonları**: İnteraktif buton efektleri
- 📊 **Gerçek Zamanlı Durum**: Bağlantı göstergesi ve animasyonları
- 🎪 **Büyüleyici Tasarım**: Görenleri etkileyecek görsel efektler
- 🔍 **Otomatik Algılama**: Server'ı kendiliğinden bulur

## API Endpoints

- `POST /chat`: Chat mesajı gönder
- `GET /health`: Server durumunu kontrol et
- `GET /`: Ana sayfa bilgisi
- `/static/index.html`: Web UI

## Sistem Prompt'u

PhantomAI aşağıdaki özelliklerle donatılmıştır:
- Türkçe konuşma
- Kod yazma uzmanlığı
- Web geliştirme uzmanlığı
- Samimi ve yardımcı davranış
- PhantomCore motoru
- Phantom AI Corp. ürünü

## Sorun Giderme

- **"API anahtarı geçersiz"**: `.env` dosyasında geçerli bir API anahtarı olduğundan emin olun
- **Web UI açılmıyor**: Server'ın çalıştığından emin olun
- **Mesaj gönderilemiyor**: Ağ bağlantısını kontrol edin

## Geliştirme

Kod değişikliklerinden sonra uygulamayı yeniden başlatın. PyQt6 ile modern GUI bileşenleri kullanılmıştır.