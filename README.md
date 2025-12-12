# PhantomAI

PhantomAI, Mistral AI API tarafından desteklenen gelişmiş bir web tabanlı sohbet robotudur. React frontend ve Node.js/Express backend kullanılarak oluşturulmuştur.

## Özellikler

- Gerçek zamanlı sohbet arayüzü
- Gelişmiş animasyonlar ve geçiş efektleri
- Tamamen Türkçeleştirilmiş kullanıcı arayüzü
- Özelleştirilebilir tema sistemi (7 farklı tema seçeneği)
- Mistral AI API entegrasyonu
- Responsive tasarım (mobil uyumlu)
- Çevresel değişken yapılandırması
- Veritabanı gerektirmeyen hafif mimari

## Kurulum

1. Repoyu klonlayın:
   ```bash
   git clone https://github.com/syavuzselim72-gif/PhantomAI.git
   cd PhantomAI
   ```

2. Bağımlılıkları yükleyin:
   ```bash
   npm install
   ```

3. `.env.example` dosyasını kopyalayarak kendi `.env` dosyanızı oluşturun:
   ```bash
   cp .env.example .env
   ```

4. Mistral API anahtarınızı `.env` dosyasında ayarlayın

5. Uygulamayı geliştirme modunda çalıştırın:
   ```bash
   npm run dev
   ```

   Veya frontend ve backend'i ayrı ayrı çalıştırın:
   ```bash
   # Terminal 1
   npm run client
   
   # Terminal 2
   npm run server
   ```

## Kullanım

Uygulama başlatıldıktan sonra tarayıcınızda `http://localhost:3007` adresine gidin. Sağ üst köşedeki ayarlar butonu ile farklı temalar seçebilirsiniz.

## Dağıtım

Bu uygulama, sağlanan yapılandırma dosyaları kullanılarak Render.com'a kolayca dağıtılabilir.

## Üretim İçin Derleme

React frontend'i üretim için derlemek üzere:
```bash
npm run build
```

Bu, Node.js sunucusunun sunacağı derlenmiş React uygulamasını içeren bir `build` dizini oluşturacaktır.

## GitHub ve Render.com Uyumluluğu

- `.gitignore` dosyası ile hassas bilgiler korunmaktadır
- `render.yaml` yapılandırması ile Render.com'da kolay dağıtım
- Çevresel değişkenler ile güvenli API anahtarı yönetimi

### Render.com Üzerinde API Anahtarı Ayarlama

Render.com üzerinde uygulamanızı deploy ederken, aşağıdaki adımları izleyerek API anahtarınızı güvenli bir şekilde ayarlayın:

1. Render.com dashboard'u açın
2. Uygulamanızın ayarlarına gidin
3. "Environment Variables" sekmesine tıklayın
4. Aşağıdaki değişkeni ekleyin:
   - Key: `MISTRAL_API_KEY`
   - Value: Mistral API anahtarınız (bu değer asla public repo'da saklanmaz)
5. Uygulamanızı yeniden deploy edin

## Güvenlik

- API anahtarları tamamen sunucu tarafında korunur
- .env dosyası .gitignore içinde olduğu için GitHub'a yüklenmez
- Tüm gizli bilgiler çevresel değişkenler aracılığıyla yönetilir

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.