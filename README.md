# YZTA-Bootcamp-Team40

## Takım Rolleri

| İsim | Rol | LinkedIn |
| :--- | :--- | :---: |
| **Helin Melike ÇAL** | *Product Owner* | <a href="https://www.linkedin.com/in/helin-melike-%C3%A7al-592680222/" target="_blank"><img src="https://img.icons8.com/color/1200/linkedin.jpg" alt="LinkedIn" height="30"></a> |
| **Ilım Naz ŞENOL** | *Scrum Master* | <a href="https://www.linkedin.com/in/%C4%B1l%C4%B1mnaz%C5%9Fenol" target="_blank"><img src="https://img.icons8.com/color/1200/linkedin.jpg" alt="LinkedIn" height="30"></a> |
| **Ahmet Bera ONAR** | *Developer* | <a href="https://www.linkedin.com/in/ahmetberaonar/" target="_blank"><img src="https://img.icons8.com/color/1200/linkedin.jpg" alt="LinkedIn" height="30"></a> |
| **Emre GERGİN** | *Developer* | <a href="https://www.linkedin.com/in/emregergin/" target="_blank"><img src="https://img.icons8.com/color/1200/linkedin.jpg" alt="LinkedIn" height="30"></a> |
| **Servet ACAR** | *Developer* | <a href="https://www.linkedin.com/in/servetacar/" target="_blank"><img src="https://img.icons8.com/color/1200/linkedin.jpg" alt="LinkedIn" height="30"></a> |

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

## Sistem Mimarisi

Akış: Kullanıcı sorusu → Şema okuma → LLM-1 (SQL üretimi) → Güvenlik denetimi
(kod tarafı + rol kontrolü) → Sorgu çalıştırma → LLM-3 (yorumlama + grafik
önerisi) → Grafik üretimi → Kullanıcıya sunum

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
- [BURAYA: Sprint 2 görselleri linki]

## Proje Kapsamının Yeniden Değerlendirilmesi

Sprint 2'nin başında proje kapsamı yeniden değerlendirilmiştir. İlk sprintte
tasarlanan JotMail (toplantı asistanı) projesi; STT, konuşmacı ayrımı, agent
orkestrasyonu ve çoklu dış servis entegrasyonu (Notion, Gmail) içerdiğinden,
kalan sürede sağlıklı bir şekilde tamamlanamayacağı görülmüştür.

Bu nedenle ekip, aynı doğal dil işleme yetkinliklerini kullanan ancak kapsamı
kalan süreye uygun, çalışır bir ürün ortaya koyabileceğimiz **SQL AI Analyst**
projesine geçiş yapmıştır. Yeni proje; agent mimarisi, ses ve görüntü işleme
içermeyen, sıralı LLM çağrılarından oluşan doğrusal bir pipeline üzerine
kurulmuştur.

Kapsam değişikliği kararı sonrasında ürün fikri, mimari ve backlog yeniden
oluşturulmuş ve geliştirmeye aynı sprint içinde başlanmıştır.

## Sprint içi puan değerlendirmesi

**Sprint içi puan değerlendirmesi:** [BURAYA: hedef puan] puan olarak belirlenmiştir.

Puanlama sistemi Sprint 1 ile aynıdır (High: 3, Medium: 2, Low: 1).

**Sprint 2 tamamlanma puanı: [BURAYA: X] / [BURAYA: Y]**

[BURAYA: Kısa açıklama — hedefe ulaşıldıysa belirtin, ulaşılmadıysa kalan
item'ların Sprint 3'e taşındığını yazın]

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
Uç noktalar:
- `POST /api/connect` — veritabanı bağlantısı kurar, şemayı okur
- `POST /api/disconnect` — bağlantıyı kapatır
- `GET /api/status` — bağlantı durumunu döner
- `POST /api/ask` — doğal dil sorusunu işler, SQL üretir, çalıştırır, yorumlar
- `POST /api/execute` — kullanıcı onayından sonra yazma sorgusunu çalıştırır

**`llm.py` — LLM pipeline**
Sıralı ve sabit üç LLM çağrısı içerir. Bu bir agent değildir; LLM hiçbir zaman
kendi kendine ne zaman çalışacağına karar vermez, akış kod tarafından belirlenir.
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
Sohbet akışı şeklinde tasarlanmış tek sayfalık arayüz. Bağlantı paneli, rol
seçimi, soru kutusu; her cevapta üretilen SQL, sonuç tablosu, grafik ve yorum
gösterilir. Yazma işlemlerinde onay bileşeni devreye girer.

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
[BURAYA: Sprint 2 daily scrum notları / ekran görüntüleri]

## Sprint 2 Board Durumu
[BURAYA: Notion board ekran görüntüsü]

### Done ([BURAYA: sayı])
- [BURAYA: tamamlanan item'lar — sorumlu ve öncelik ile]

### In Progress ([BURAYA: sayı])
- [BURAYA: devam eden item'lar]

### Planned ([BURAYA: sayı])
- [BURAYA: planlanan item'lar]

## Ürün Durumu
[BURAYA: Çalışan uygulamanın ekran görüntüleri — bağlantı ekranı, bir soruya
verilen cevap (SQL + tablo + grafik + yorum), onay ekranı]

## Sprint Review
- Proje kapsamı yeniden değerlendirilmiş ve kalan süreye uygun, çalışır bir ürün
  ortaya koyabilmek adına SQL AI Analyst projesine geçiş yapılmıştır.
- Doğal dil sorusundan SQL üretimi, güvenlik denetimi, sorgu çalıştırma, sonuç
  yorumlama ve grafik üretimini kapsayan uçtan uca akış tamamlanmıştır.
- Rol tabanlı yetkilendirme ve yazma işlemleri için onay mekanizması kurulmuştur.
- Arayüz geliştirilmiş; üretilen SQL, sonuç tablosu, grafik ve yorum tek ekranda
  gösterilir hale getirilmiştir.
- [BURAYA: eklemek istediğiniz diğer maddeler]

### Sprint Review Katılımcıları
- [BURAYA: katılımcılar]

## Sprint Retrospective
- Kapsamın erken gözden geçirilmesi ve gerçekçi bir hedefe yönelinmesi, ekibin
  kalan sürede çalışır bir ürün ortaya koyabilmesini sağlamıştır.
- Agent mimarisi yerine sıralı ve öngörülebilir bir LLM pipeline'ı tercih edilmesi,
  hem geliştirme hem hata ayıklama süresini belirgin şekilde kısaltmıştır.
- Güvenliğin yalnızca model talimatlarına bırakılmaması, kod tarafında bağımsız
  bir doğrulama katmanı kurulması gerektiği görülmüştür.
- [BURAYA: Sprint 3 için alınan kararlar]
