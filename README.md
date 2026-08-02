# YZTA-Bootcamp-Team40

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/0d4c4959-e9d1-455a-9c75-730801c39f45" />

## Takım Rolleri

| İsim | Rol | LinkedIn |
| :--- | :--- | :---: |
| **Helin Melike ÇAL** | *Product Owner* | <a href="https://www.linkedin.com/in/helin-melike-%C3%A7al-592680222/" target="_blank"><img src="https://img.icons8.com/color/1200/linkedin.jpg" alt="LinkedIn" height="30"></a> |
| **Ilım Naz ŞENOL** | *Scrum Master* | <a href="https://www.linkedin.com/in/%C4%B1l%C4%B1mnaz%C5%9Fenol" target="_blank"><img src="https://img.icons8.com/color/1200/linkedin.jpg" alt="LinkedIn" height="30"></a> |
| **Emre GERGİN** | *Developer* | <a href="https://www.linkedin.com/in/emregergin/" target="_blank"><img src="https://img.icons8.com/color/1200/linkedin.jpg" alt="LinkedIn" height="30"></a> |

# ÜRÜN BİLGİLERİ
<img width="1123" height="794" alt="Adsız tasarım (1)" src="https://github.com/user-attachments/assets/1792b645-8420-442f-abd0-db6dede4a5a1" />

## Ürün İsmi
**AskQL - SQL AI Analyst** — Doğal dil ile veritabanı sorgulama asistanı

## Ürün Açıklaması
Veritabanına bağlanıp Türkçe soru sorarak, SQL bilmeden veri analizi yapmayı
sağlayan yapay zeka destekli analiz asistanı. Kullanıcının sorusunu SQL'e
çevirir, güvenlik denetiminden geçirir, çalıştırır ve sonucu tablo, grafik ve
Türkçe yorum olarak sunar.

## Ürün Özellikleri
- Kendi SQL Server veritabanına bağlanma ve şemayı otomatik okuma
- Türkçe doğal dil sorusunu T-SQL sorgusuna çevirme
- Rol tabanlı yetkilendirme (Analist: yalnızca SELECT / Yönetici: onaylı yazma işlemleri)
- Kod tarafında sorgu türü doğrulaması ile güvenlik denetimi
- Sonuçları Türkçe yorumlama ve içgörü çıkarma
- Sonuca uygun grafik türünü otomatik seçme ve görselleştirme
- Yazma işlemleri için kullanıcı onay ekranı (human-in-the-loop)
- Üretilen SQL'in kullanıcıya şeffaf şekilde gösterilmesi

## Hedef Kitle
- SQL bilmeyen ancak veriye ihtiyaç duyan pazarlama, satış ve operasyon çalışanları
- Veri ekibi olmayan veya veri ekibi yoğun olan şirketler
- Küçük ve orta ölçekli işletmelerde raporlama ihtiyacı olan yöneticiler

## AskQL Kullanım ve Kurulum Kılavuzu

- [Kullanım kılavuzuna ulaşmak için tıklayın.](./AskQL%20Kullanim%20Kilavuzu.pdf)
- [Kurulum kılavuzu için tıklayın.](<./AskQL Kurulum Kılavuzu>)


## Sistem Mimarisi

<img width="1693" height="929" alt="image" src="https://github.com/user-attachments/assets/ed3f235d-790c-40cd-b334-e8070ce7bf23" />


## Product Backlog
- Product Backlog, [Notion](https://app.notion.com/p/41311c5edb9446e5ab44098fb74f39dd?v=3bd3e3d92a8a4d4dbc1d1263cbfecb69&source=copy_link) board'u üzerinde önceliklendirilmiş görev kartları halinde yönetilmektedir.
- [Bootcamp süreci](https://canva.link/0zsy7vjj6uxodpf) ile ilgili tüm görseller buradadır.
  
### Puanlama Sistemi

Backlog item'ları önceliklerine göre puanlanmıştır. Öncelik, bir görevin
projenin ilerlemesi için ne kadar kritik olduğuna göre belirlenmiştir:

| Öncelik | Puan |
|---------|------|
| High (Yüksek)  | 3 |
| Medium (Orta)  | 2 |
| Low (Düşük)    | 1 |

# SPRINT 1
- **Sprint Tarih Aralığı:** 28 Haziran – 5 Temmuz
- [Sprint 1 süreci](https://canva.link/0zsy7vjj6uxodpf) ile ilgili tüm görseller buradadır.

## Sprint içi puan değerlendirmesi 
**Sprint içi puan değerlendirmesi:** 22 puan olarak belirlenmiş olup, **Sprint 1 tamamlanma puanı: 17 / 22**

Sprint için hedeflenen 22 puanın 17'si tamamlanmıştır. Kalan item'lar
ikinci sprintin backlog'una taşınmıştır.

## Daily Scrum 
Ekip içi iletişim; Notion üzerinde yürütülen görev kartları, Google Meet aracılığıyla gerçekleştirilen düzenli toplantılar ve WhatsApp görüşmeleri ile sağlanmıştır.

### Kullanılan Araçlar 
- [Notion](https://app.notion.com/p/41311c5edb9446e5ab44098fb74f39dd?v=3bd3e3d92a8a4d4dbc1d1263cbfecb69&source=copy_link) (görev takibi, proje veritabanı, board yönetimi)
- WhatsApp
- Google Meet

## Sprint 1 Board Durumu 
<img width="1572" height="867" alt="image" src="https://github.com/user-attachments/assets/e936bf22-bf89-4301-8c87-960239f9352a" />

### Done (5) 
- Proje mimarisi tasarımı — Toplantı kaydı → STT → özet/karar tespiti → görev-kişi eşleştirme → onay ekranı → Agent → Notion/Mail akışının belirlenmesi. (Öncelik: High)
- Frontend mockup hazırlama — Ilım Naz (Öncelik: High)
- Backend API entegrasyonu — Emre (Öncelik: High)
- LLM sınıflandırma, özetleme ve karar tespiti — Helin (Öncelik: High)
- Sprint 1 Kapanış Toplantısı yapıldı. — Helin, Ilım Naz, Ahmet Bera, Emre, Servet (Öncelik: High)

### In Progress (2) 
- Hafıza modülü kurulumu — Servet (Öncelik: Medium, Sprint 1 & Sprint 2)
- STT model denemeleri — Ahmet Bera (Öncelik: Medium, Sprint 1 & Sprint 2)

### Planned (1) 
- Sprint 2 taskleri için toplantı planlanacak — Helin, Ilım Naz, Ahmet Bera, Emre, Servet (Öncelik: High)

## Ürün Durumu

Sprint 1 sürecinde JotMail'in ana ekranına ait arayüz mock'u hazırlanmıştır. Ekran; bir toplantının konuşmacı ayrımlı transkriptini, görev ve kararların renkli olarak vurgulandığı analiz görünümünü ve sağ tarafta yapılandırılmış çıktıyı (özet, kararlar, kişilere atanmış görevler) bir arada gösterir. Böylece toplantı kaydından onaya hazır aksiyonlara uzanan akış tek ekranda görüntülenebilmektedir.

<img width="1351" height="591" alt="image (1)" src="https://github.com/user-attachments/assets/ecd08562-2aa6-4d4e-9a9e-151a7caaebeb" />

Ürüne ait diğer arayüz ekranları ve tasarım görsellerine [bu Canva bağlantısından](https://canva.link/0zsy7vjj6uxodpf) ulaşabilirsiniz.

## Sprint Review 
- Proje mimarisi netleştirilmiş, 5 rol arasında görev dağılımı yapılmış ve her modülün ilk teknik adımları atılmıştır. 
- Frontend mockup'ı ve Backend API bağlantıları tamamlanmış, LLM sınıflandırma/özetleme akışı kurulmuştur. 
- STT model denemeleri ve hafıza modülü kurulumu Sprint 2'ye taşınarak devam etmektedir.

### Sprint Review Katılımcıları 
- Helin, Ilım Naz, Ahmet Bera, Emre, Servet

## Sprint Retrospective 
- Proje mimarisinin net biçimde tanımlanması ekibin paralel çalışmasını kolaylaştırmıştır.
- STT ve Hafıza modüllerinin süre gerektirmesi nedeniyle bu iki iş kalemi Sprint 2'ye devam ettirilmiştir.
- Sprint 2 planlaması için ayrı bir toplantı yapılması kararlaştırılmıştır.
- Sprint 2 sürecinde ürünü daha iyi yansıtacak bir logo tasarımı için detaylı çalışmalar yapılmasına karar verilmiştir.
- Sprint 1 kapanış toplantısı yapılarak tamamlanan işler gözden geçirilmiş, tamamlanamayan maddelerin (STT model denemeleri ve hafıza modülü kurulumu) ikinci sprinte aktarılmasına karar verilmiştir.


# SPRINT 2

- **Sprint Tarih Aralığı:** 6 Temmuz – 19 Temmuz
- [Sprint 2 süreci](https://canva.link/0zsy7vjj6uxodpf) ile ilgili tüm görseller buradadır.

## Proje Kapsamının Yeniden Değerlendirilmesi

Sprint 2'nin başında proje kapsamı yeniden değerlendirilmiştir. İlk sprintte tasarlanan JotMail (toplantı asistanı) projesi; STT, konuşmacı ayrımı, agent orkestrasyonu ve çoklu dış servis entegrasyonu (Notion, Gmail) gibi kapsamlı bileşenler içermektedir. Hem bu bileşenlerin gerektirdiği geliştirme süresi hem de ses işleme modellerinin ihtiyaç duyduğu donanımın ekibin mevcut imkanlarıyla karşılanamaması nedeniyle, projenin kalan sürede sağlıklı bir şekilde tamamlanamayacağı görülmüştür.

Kapsam değişikliği kararı sonrasında ürün fikri, mimari ve backlog yeniden
oluşturulmuş ve geliştirmeye aynı sprint içinde başlanmıştır.

## Sprint içi puan değerlendirmesi
**Sprint içi puan değerlendirmesi:** 34 puan olarak belirlenmiş olup, **Sprint 2 tamamlanma puanı: 29 / 34**

Sprint için hedeflenen 34 puanın 29'u tamamlanmıştır.


## Geliştirilen Yapı

Sprint 2 sonunda uçtan uca çalışan bir uygulama ortaya çıkarılmıştır.

### Teknoloji Yığını
| Katman | Teknoloji |
|---|---|
| Web çatısı | Flask 3.0.3 |
| LLM | OpenAI gpt-4o-mini (JSON mode) |
| Veritabanı | Microsoft SQL Server (pyodbc) |
| Görselleştirme | matplotlib |
| Arayüz | HTML / CSS / Vanilla JavaScript |
| Veri işleme | pandas |

### Modüller

**`app.py` — Flask uygulaması ve API katmanı**
Uygulamanın giriş noktası ve tüm modülleri birbirine bağlayan katman.

**`llm.py` — LLM pipeline**
Sıralı ve sabit üç LLM çağrısı içerir.
- `generate_sql()` — Türkçe soru + veritabanı şeması + kullanıcı rolü → T-SQL
  sorgusu. JSON çıktı: `sql`, `query_type`, `aciklama`, `uyari`
- `fix_sql()` — sorgu hata verirse tek seferlik düzeltme denemesi (döngü değil)
- `interpret_results()` — sorgu sonucu → Türkçe yorum + grafik önerisi.
  JSON çıktı: `yorum`, `chart_type`, `x_column`, `y_column`, `title`

**`db.py` — Veritabanı katmanı ve güvenlik**
- SQL Server bağlantı yönetimi (pyodbc)
- `INFORMATION_SCHEMA.COLUMNS` üzerinden otomatik şema okuma
- `get_schema_text()` — şemayı LLM promptuna gömülecek okunabilir metne çevirir
- `classify_query()` — SQL'in gerçek türünü (select/write) regex ile tespit eder
- `run_select()` — yalnızca SELECT çalıştırır, satır sayısını sınırlar (max 500)
- `run_write()` — yazma sorguları için, hata durumunda rollback yapar

**`chart.py` — Görselleştirme**
LLM'in önerdiği grafik türüne göre (bar / line / pie) matplotlib ile grafik
üretir ve base64 PNG olarak döner. Veri grafiğe uygun değilse grafik üretmez.

**Arayüz (`templates/`, `static/`)**
Sprint 2'de arayüz, sistemin uçtan uca çalıştığını doğrulamak amacıyla işlevsel düzeyde geliştirilmiştir. 
Tasarım ve kullanıcı deneyimi iyileştirmeleri Sprint 3 kapsamında planlanmıştır.

### Güvenlik Yaklaşımı

Ürünün ayırt edici yanı, SQL bilmeyen bir kullanıcının üretilen sorgunun
tehlikeli olup olmadığını değerlendiremeyeceği gerçeğinden yola çıkan çok
katmanlı güvenlik denetimidir:

1. **Rol tabanlı yetkilendirme:** Analist rolü yalnızca SELECT çalıştırabilir;
   yazma işlemleri yalnızca Yönetici rolüne açıktır.
2. **Kod tarafı doğrulama:** LLM'in beyan ettiği sorgu türüne güvenilmez;
   sorgunun gerçek türü `classify_query()` ile bağımsız olarak tespit edilir ve
   uyuşmazlık durumunda kod tarafındaki sonuç esas alınır.
3. **Fonksiyon seviyesinde koruma:** `run_select()` SELECT dışındaki sorguları,
   `run_write()` ise okuma sorgularını reddeder.
4. **Kullanıcı onayı (human-in-the-loop):** Yazma sorguları çalıştırılmadan önce
   SQL, açıklaması ve uyarısıyla birlikte kullanıcıya sunulur; yalnızca onay
   sonrasında ayrı bir uç noktada çalıştırılır.
5. **Prompt seviyesinde kısıt:** WHERE koşulu olmayan DELETE/UPDATE üretilmemesi,
   şemada olmayan tablo/kolon uydurulmaması ve SELECT sorgularına TOP sınırı
   eklenmesi model talimatlarına dahil edilmiştir.

### Demo Veri Seti
Geliştirme ve test sürecinde Türkçe kolon adları içeren bir satış veri seti
kullanılmıştır (Tarih, Ürün Kategorisi, Ürün Adı, Birim Fiyat, Satış Miktarı,
Satış Tutarı, Satış Bölgesi).

## Daily Scrum 
Ekip içi iletişim; Notion üzerinde yürütülen görev kartları, Google Meet aracılığıyla gerçekleştirilen toplantılar ve WhatsApp görüşmeleri ile sağlanmıştır.

### Kullanılan Araçlar 
- [Notion](https://app.notion.com/p/41311c5edb9446e5ab44098fb74f39dd?v=3bd3e3d92a8a4d4dbc1d1263cbfecb69&source=copy_link) (görev takibi, proje veritabanı, board yönetimi)
- WhatsApp
- Google Meet


## Sprint 2 Board Durumu
<img width="1600" height="761" alt="image" src="https://github.com/user-attachments/assets/7103c766-0ed1-4443-823e-93dfd62a646c" />

### Done (10)
- Proje kapsamının yeniden değerlendirilmesi
- Yeni ürün fikrinin ve mimarisinin oluşturulması 
- Demo veritabanı ve veri seti hazırlığı 
- Veritabanı bağlantı ve şema okuma modülü 
- SQL üretim modülü (LLM-1)
- Sonuç yorumlama ve grafik önerisi modülü (LLM-2)
- Güvenlik katmanı ve rol tabanlı yetkilendirme
- Arayüz geliştirme (işlevsel düzey)
- Sprint 2 kapanış toplantısı
- Github repository düzenleme

### In Progress (3)
- README'nin yeni projeye göre güncellenmesi 
- Yeni ürünün logo tasarımı
- Yeni ürüne isim bulunması

### Planned (3)
- Sprint 3 için hazırlık toplantısı yapılacak.
- Backend sistem çalışmaları
- Kullanıcı deneyimi iyileştirme

## Ürün Durumu
Sprint 2 sürecinde SQL AI Analyst'in uçtan uca çalışan sürümü geliştirilmiştir. Uygulama; kullanıcının kendi SQL Server veritabanına bağlanmasını, rolünü (Analist / Yönetici) seçmesini ve veritabanına Türkçe soru sormasını sağlar. Her cevapta üretilen SQL sorgusu, sonuç tablosu, otomatik seçilen grafik ve sonucun Türkçe yorumu tek ekranda gösterilir. Yazma işlemlerinde sorgu çalıştırılmadan önce açıklaması ve uyarısıyla birlikte kullanıcı onayına sunulur. Böylece soru sormaktan onaylı sonuca uzanan akış tek ekranda takip edilebilmektedir.

<img width="1600" height="761" alt="image" src="https://github.com/user-attachments/assets/1817a6ca-d7ac-4bc6-a47a-29827a4fe0e9" />

Ürüne ait diğer arayüz ekranları ve tasarım görsellerine [bu Canva bağlantısından](https://canva.link/0zsy7vjj6uxodpf) ulaşabilirsiniz.

## Sprint Review
- Proje kapsamı yeniden değerlendirilmiş ve kalan süreye uygun, çalışır bir ürün
  ortaya koyabilmek adına SQL AI Analyst projesine geçiş yapılmıştır.
- Doğal dil sorusundan SQL üretimi, güvenlik denetimi, sorgu çalıştırma, sonuç
  yorumlama ve grafik üretimini kapsayan uçtan uca akış tamamlanmıştır.
- Rol tabanlı yetkilendirme ve yazma işlemleri için onay mekanizması kurulmuştur.
- Arayüz geliştirilmiş; üretilen SQL, sonuç tablosu, grafik ve yorum tek ekranda
  gösterilir hale getirilmiştir.


### Sprint Review Katılımcıları
- Helin, Ilım Naz.

## Sprint Retrospective
- Kapsamın erken gözden geçirilmesi ve gerçekçi bir hedefe yönelinmesi, ekibin
  kalan sürede çalışır bir ürün ortaya koyabilmesini sağlamıştır.
- Agent mimarisi yerine sıralı ve öngörülebilir bir LLM pipeline'ı tercih edilmesi,
  hem geliştirme hem hata ayıklama süresini belirgin şekilde kısaltmıştır.
- Güvenliğin yalnızca model talimatlarına bırakılmaması, kod tarafında bağımsız
  bir doğrulama katmanı kurulması gerektiği görülmüştür.
- Sprint 2 kapanış toplantısı yapılarak sprint tamamlanmıştır.


# SPRINT 3

- **Sprint Tarih Aralığı:** 20 Temmuz – 2 Ağustos
- Bu sprint, projenin **son sprintidir**; proje bu sprintte tamamlanmıştır.
- [Sprint 3 süreci](https://canva.link/0zsy7vjj6uxodpf) ile ilgili tüm görseller buradadır.

## Sprint içi puan değerlendirmesi
**Sprint içi puan değerlendirmesi:** 50 puan olarak belirlenmiş olup, **Sprint 3 tamamlanma puanı: 50 / 50**

Sprint kapsamındaki görevlerin çoğu High (Yüksek) öncelikli kabul edilerek 3'er puan, marka kimliği/isim/logo çalışması ise Medium (Orta) öncelikli kabul edilerek 2 puan üzerinden değerlendirilmiş ve hedeflenen 50 puanın tamamı tamamlanmıştır.

## Geliştirilen Yapı

Sprint 2 sonunda uçtan uca çalışan hale getirilen uygulama, Sprint 3'te kimlik doğrulama, yetkilendirme, kurumsal kullanım (şirket/çalışan yönetimi) ve arayüz açısından olgunlaştırılarak sunuma hazır hale getirilmiştir.

### Teknoloji Yığını
| Katman | Teknoloji |
|---|---|
| E-posta Servisi | Brevo |
| Web çatısı | Flask 3.0.3 |
| LLM orkestrasyonu | LangChain |
| LLM | OpenAI gpt-4o-mini (JSON mode) |
| Veritabanı (iş verisi) | Microsoft SQL Server (pyodbc) |
| Kullanıcı / şirket verisi | Supabase |
| Yayına alma | Railway |
| Görselleştirme | matplotlib |
| Arayüz | HTML / CSS / Vanilla JavaScript |
| Tipografi | Inter, Space Grotesk, JetBrains Mono |
| Veri işleme | pandas |

### Modüller

**Kimlik doğrulama (users_db.py + Brevo + Supabase)
Kimlik doğrulama katmanı Supabase üzerinde çalışmaktadır. Kullanıcı ve şirket bilgileri Supabase'de tutulurken, hesap oluşturma sırasında gönderilen 6 haneli doğrulama kodu ile e-posta doğrulaması Brevo üzerinden gerçekleştirilmektedir. Hesap doğrulanmadan sisteme giriş yapılamaz. Ayrıca yönetici tarafından eklenen çalışanlara geçici şifre oluşturularak Brevo aracılığıyla e-posta olarak iletilmektedir.

**app.py — API Katmanı
/api/register, /api/verify, /api/resend_code, /api/login, /api/logout, /api/change_password ve diğer API uç noktaları geliştirilmiştir. Kimlik doğrulaması gerektiren tüm işlemler login_required ile korunmaktadır. Ayrıca "Beni Hatırla" seçeneği sayesinde 30 güne kadar kalıcı oturum desteği sunulmaktadır.

**db.py — Veritabanı ve Yetkilendirme
SQL Server bağlantısı çok şirketli (multi-tenant) mimariye uygun şekilde yönetilmektedir. Üretilen SQL sorguları çalıştırılmadan önce sunucu tarafında bağımsız olarak sınıflandırılır (SELECT / DML / DDL) ve kullanıcının unvanına göre yetkilendirilir. SELECT ve yazma işlemleri farklı fonksiyonlar üzerinden yürütülmektedir.

**Şirket ve çalışan yönetimi
Sisteme ilk kayıt olan kullanıcı otomatik olarak Yönetici unvanını alır ve şirketini oluşturur. Yönetici daha sonra şirkete Çalışan veya Müdür unvanıyla yeni kullanıcılar ekleyebilir. Yetkilendirme tamamen sunucu tarafında saklanan unvan bilgisine göre yapılmaktadır.

**Grafik oluşturma
Sorgu sonucuna en uygun grafik türü LLM tarafından belirlenmekte; grafik oluşturma işlemi ise ayrı bir modül tarafından gerçekleştirilmektedir. Bar, Line, Pie, Area, Scatter ve Histogram grafikleri desteklenmektedir.

**Dışa aktarma
Sorgu sonuçları CSV ve PDF formatlarında dışa aktarılabilmektedir. PDF raporları çok sayfalı tablo olarak oluşturulmaktadır.

**Raporlar Paneli
Kullanıcıların gerçekleştirdiği sorgular oturum geçmişinde saklanmakta ve daha sonra tekrar görüntülenebilmektedir. Önceki sorgular aynı zamanda LLM'e bağlam sağlayarak çok adımlı doğal dil konuşmalarını desteklemektedir.

**Arayüz
Arayüz tamamen yenilenerek marka kimliği oluşturulmuş; giriş, kayıt, e-posta doğrulama ve veritabanı bağlantısı adımları birbirinden ayrılmıştır. Responsive tasarım uygulanmış ve kullanıcı deneyimi iyileştirilmiştir.

**Güvenlik Yaklaşımı
Sprint 2'deki çok katmanlı güvenlik yapısı bu sprintte geliştirilmiştir.

Yetkilendirme tamamen sunucu tarafında yapılmaktadır. Kullanıcının unvanı (Çalışan / Müdür / Yönetici) Supabase'den okunur; istemciden gönderilen hiçbir rol bilgisine güvenilmez.
Her SQL sorgusu kod tarafında bağımsız olarak doğrulanır. Üretilen sorgu önce SELECT, DML veya DDL olarak sınıflandırılır; ardından kullanıcının yetkisine göre çalıştırılıp çalıştırılamayacağına karar verilir. LLM'in ürettiği sorgu doğrudan çalıştırılmaz.
LLM yalnızca SQL üretir. SQL'in çalıştırılması, güvenlik kontrolleri ve rol denetimleri tamamen Python kodu tarafından gerçekleştirilir. Ayrıca hata oluşması durumunda sınırlı sayıda self-healing retry mekanizması ile sorgu yeniden üretilir.
Kimlik doğrulama ile yetkilendirme birbirinden ayrılmıştır. E-posta ve şifre uygulamaya erişimi sağlarken, kullanıcının unvanı hangi SQL işlemlerini gerçekleştirebileceğini belirler.
Şifre güvenliği Supabase üzerinde hash'lenerek saklanmakta; doğrulama kodları süreli (15 dakika) olarak oluşturulmaktadır.

### Demo Veri Seti
Sprint 2'deki veri seti değişmeden kullanılmaya devam etmiştir.

## Daily Scrum
Ekip içi iletişim; Notion üzerinde yürütülen görev kartları, Google Meet aracılığıyla gerçekleştirilen toplantılar ve WhatsApp görüşmeleri ile sağlanmıştır.

### Kullanılan Araçlar
- [Notion](https://app.notion.com/p/41311c5edb9446e5ab44098fb74f39dd?v=3bd3e3d92a8a4d4dbc1d1263cbfecb69&source=copy_link) (görev takibi, proje veritabanı, board yönetimi)
- WhatsApp
- Google Meet

## Sprint 3 Board Durumu

<img width="1366" height="648" alt="image" src="https://github.com/user-attachments/assets/451701f4-9790-4fb7-8cc4-9ceb7e30b6fc" />


### Done (17)
- Mevcut kod tabanının (frontend mimarisi, UI, UX, erişilebilirlik) uçtan uca gözden geçirilmesi
- Form etiketlerinin (`label`) input'lara `for`/`id` ile programatik bağlanması
- Hata mesajları ve dinamik içerik için `aria-live`/`role="alert"` eklenmesi
- Kontrast oranı ölçülüp WCAG AA eşiğinin altında kalan hata renginin düzeltilmesi
- Ürün isminin kesinleşmesi (AskQL), logonun şeffaf arka planlı hale getirilip favicon dahil arayüze entegre edilmesi ve marka kimliğine uygun, responsive giriş ekranı tasarımı
- Uygulama seviyesinde kimlik doğrulama sisteminin eklenmesi (kayıt, giriş, çıkış, beni hatırla)
- Yerel kullanıcı deposundan Supabase'e geçiş
- E-posta ile gönderilen şifre üzerinden sisteme giriş desteklenmesi
- Giriş/kayıt ve veritabanı bağlantı adımlarının birbirinden ayrıştırılması
- Şirket kaydı özelliğinin eklenmesi
- Üç kademeli unvan sistemiyle (Çalışan / Müdür / Yönetici) çalışan ekleme
- Yetkilendirme modelinin, sunucu tarafında okunan şirket unvanına dayanan modele taşınması
- Uygulamanın Railway üzerinde canlıya alınması
- Sorgu sonuçlarının PDF ve CSV olarak dışa aktarılması
- Raporlar paneli — geçmiş sorguların listelenmesi
- Backend sistem çalışmaları
- Kullanıcı deneyimi iyileştirmesi

### In Progress (0)
- Yok — proje bu sprintte tamamlanmıştır.

### Planned (0)
- Yok. Değerlendirilip bilinçli olarak kapsam dışı bırakılan tek özellik Google ile giriştir; OAuth altyapısı gerektirdiğinden, sahte/işlevsiz bir görünüm sunmamak için eklenmemiştir.

## Ürün Durumu
AskQL, bu sprintle birlikte sunuma hazır, uçtan uca çalışan ve Railway üzerinde canlıda bir ürün haline gelmiştir. Kullanıcı önce kendi hesabıyla (e-posta ile gönderilen şifre üzerinden) giriş yapıyor; şirketini kaydedip çalışanlarını unvanlarına göre (Çalışan / Müdür / Yönetici) ekleyebiliyor. SQL Server'a bağlanıp veritabanına Türkçe sorular sorulabiliyor; her cevapta üretilen SQL, sonuç tablosu, grafik ve Türkçe yorum tek ekranda sunuluyor, sonuçlar PDF/CSV olarak dışa aktarılabiliyor ve geçmiş sorgular raporlar panelinden görülebiliyor. Yazma işlemleri kullanıcı onayından geçiyor; yetki artık kullanıcı beyanına değil, çalışana şirket yöneticisi tarafından atanan ve sunucu tarafında okunan unvana göre otomatik belirleniyor.

<img width="1600" height="759" alt="image" src="https://github.com/user-attachments/assets/64172391-3599-4007-bcda-864873710865" />

Ürüne ait güncel arayüz ekranları ve tasarım görsellerine [bu Canva bağlantısından](https://canva.link/0zsy7vjj6uxodpf) ulaşabilirsiniz.

## Sprint Review
- Kod tabanı uçtan uca gözden geçirildi; erişilebilirlik ve kontrast düzeltmeleri yapıldı.
- Kimlik doğrulama ve yetkilendirme katmanları bilinçli olarak ayrıştırıldı.
- Yetkilendirme, istemciden gelen bir değere değil, sunucu tarafında okunan şirket unvanına dayanan bir modele taşındı.
- Şirket kaydı, unvana dayalı çalışan yönetimi ve raporlar paneli eklendi.
- Giriş deneyimi ayrı adımlara bölünüp marka kimliğine kavuşturuldu.
- Uygulama Railway üzerinde canlıya alındı; sonuç dışa aktarma özelliği eklendi.
- Proje, sunuma hazır durumdadır.

### Sprint Review Katılımcıları
- Helin, Ilım Naz, Emre.

## Sprint Retrospective
- Bu sprintte ekip kompozisyonunda değişiklik yaşanmış, bazı ekip arkadaşlarıyla yollar ayrılmıştır; kalan ekip (Helin, Ilım Naz ve Emre), projeyi tamamlayarak sunuma hazır hale getirmiştir.
- Net bir tasarım referansı belirlenene kadar birden çok iterasyon denenmesi zaman aldı.
- Kimlik doğrulama ile veritabanı yetkilendirmesinin ayrı katmanlar olarak kurulması, güvenlik modelinin bozulmadan korunmasını sağladı.
- Güvenliğin istemci tarafına bırakılmaması gerektiği, bu sprintte somut bir düzeltmeyle bir kez daha teyit edildi.
- Sprint 3 kapanış toplantısı yapılarak, proje bu sprint ile tamamlanmıştır.



