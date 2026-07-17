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
- Hatalı sorgular için tek seferlik otomatik düzeltme
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
- Product Backlog, [Notion](NOTION_LINKI) board'u üzerinde önceliklendirilmiş
  görev kartları halinde yönetilmektedir.

# SPRINT 1
- **Sprint Tarih Aralığı:** 28 Haziran – 5 Temmuz
- [Sprint 1 süreci](https://canva.link/0zsy7vjj6uxodpf) ile ilgili tüm görseller buradadır.

## Sprint içi puan değerlendirmesi 
**Sprint içi puan değerlendirmesi:** 22 puan olarak belirlenmiştir.

### Puanlama Sistemi

Backlog item'ları önceliklerine göre puanlanmıştır. Öncelik, bir görevin
projenin ilerlemesi için ne kadar kritik olduğuna göre belirlenmiştir:

| Öncelik | Puan |
|---------|------|
| High (Yüksek)  | 3 |
| Medium (Orta)  | 2 |
| Low (Düşük)    | 1 |

Her sprintte tamamlanan item'ların puanları toplanarak sprintin tamamlanma
puanı hesaplanmıştır.

**Sprint 1 tamamlanma puanı: 17 / 22**

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
