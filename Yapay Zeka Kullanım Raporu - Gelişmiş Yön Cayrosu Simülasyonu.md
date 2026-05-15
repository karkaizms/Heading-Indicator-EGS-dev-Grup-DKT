# **YAPAY ZEKA KULLANIM RAPORU**

## **PROJE: GELİŞMİŞ YÖN CAYROSU (HSI) SİMÜLASYONU**

**Bölüm / Görev:** Aviyonik (Havacılık Elektrik ve Elektroniği)   
**Tarih:** 15 Mayıs 2026

## ---

**1\. GİRİŞ**

Bu rapor, "Gelişmiş Yön Cayrosu (Directional Gyro / HSI) Simülasyonu" projesinin araştırma, geliştirme ve test süreçlerinde Yapay Zeka (AI) asistanının (Google Gemini tabanlı kodlama asistanı) entegrasyonunu belgelemek amacıyla hazırlanmıştır. Çalışma boyunca yapay zeka, sadece bir kod üretici değil, aynı zamanda aviyonik sistem mantığını yazılıma aktaran bir **Eşli Programcı (Pair Programmer)** olarak konumlandırılmıştır.

## **2\. AI ENTEGRASYONU VE KULLANIM ALANLARI**

### **2.1. Temel Altyapı ve Kod Üretimi (Code Generation)**

* **Grafik Motoru ve Döngü Yönetimi:** Grafiksel kullanıcı arayüzünün (GUI) performanslı çalışması adına, pygame kütüphanesinin iskelet yapısı, 60 FPS kararlı oyun döngüsü (game loop) ve asenkron olay dinleme (event handling) mekanizmaları AI desteğiyle kurulmuştur.  
* **Trigonometrik Modelleme:** Pusula kartının dairesel rotasyonu, uçağın anlık rotasının dereceden radyana çevrilerek ekrana dinamik basılması ve enstrüman çizgilerinin matematiksel konumlandırılması sağlanmıştır.

### **2.2. Gelişmiş Simülasyon Mekanikleri ve Aviyonik Hesaplamalar**

* **Jiroskop Kayması (Gyro Drift):** Gerçek uçuş koşullarında yer alan fiziksel sapmalar ve dünya dönüşü/sürtünme kaynaklı mekanik hatalar, zaman tabanlı dinamik bir algoritma ile koda dökülmüştür.  
* **Otopilot ve İnterpolasyon:** autoplay\_mode aktif edildiğinde uçağın hedef baş değerine ani keskin dönüşler yerine, havacılık standartlarına uygun yumuşaklıkta (interpole edilerek) dönmesini sağlayan matematiksel formüller kurgulanmıştır.  
* **Hata (Failure) ve Alarm Mantığı:** Sistem arızaları ve rota sapma (Heading Deviation) durumları için time.time() fonksiyonu kullanılarak zamanlayıcıya bağlı, görsel olarak yanıp sönen (flashing) uyarı mekanizmaları ve koşullu mantık mimarisi geliştirilmiştir.

### **2.3. Kullanıcı Arayüzü (UI) ve Etkileşim Tasarımı**

* **Seçici Kontrolleri (Heading Bug):** Kullanıcının rota seçiciyi fareyle yönlendirebilmesi için farenin pusula merkezine göre açısını hesaplayan math.atan2 tabanlı hassas bir arayüz algoritması yazılmıştır.  
* **Ergonomi ve Çevresel Koşullar:** Pilot yükünü azaltmayı hedefleyen, gece ve gündüz uçuş operasyonlarına uygun kontrastta iki farklı renk paleti optimize edilmiştir.  
* **Veri Loglama:** Uçuş verilerinin analizi için arka planda sistemi yormayacak şekilde, saniyelik periyotlarla çalışan bir .csv kayıt sistemi entegre edilmiştir.

### **2.4. Dokümantasyon ve Teknik Raporlama**

* Kod bloklarının sürdürülebilirliği için endüstri standartlarında açıklama satırları (clean code comments) eklenmiştir.  
* Projenin ana teknik dokümanı olan PROJE\_RAPORU.md dosyası ve bu kullanım raporu yapılandırılmış akademik bir dille derlenmiştir.

## **3\. AI KULLANIMININ AVANTAJLARI VE SÜRECE KATKISI**

| Geliştirme Alanı | Geleneksel Yöntem (Tahmini Süre) | AI Destekli Süreç | Sağlanan Katma Değer   |
| :---- | :---- | :---- | :---- |
| **Trigonometrik Altyapı** | Saatler süren deneme-yanılma | Saniyeler içinde optimizasyon | Sıfır matematiksel hata ile kararlı çizimler. |
| **Algoritma Geliştirme** | Kompleks modüler aritmetik testleri | Hazır shortest\_angle\_diff mantığı | Otopilot dönüşlerinde en kısa ve doğru yön seçimi. |
| **Hata Ayıklama (Debugging)** | Manuel log inceleme ve crash takibi | Proaktif hata tespiti | Disk yazma darboğazlarının engellenmesi, performans artışı. |

**Eğitimsel Rehberlik:** AI, sadece ham kod üretmekle kalmamış; havacılık enstrümanlarının (Drift, HDG Bug, Sync) çalışma prensiplerinin yazılım mimarisine nasıl kusursuz yedirileceği konusunda bir danışman görevi görmüştür.

## **4\. SONUÇ**

Bu proje, modern aviyonik yazılım süreçlerinde **İnsan-Yapay Zeka İşbirliğinin (Human-AI Collaboration)** verimliliğini somut bir şekilde ortaya koymuştur. Geliştiricinin havacılık alan bilgisi, sistem vizyonu ve doğru yönlendirmeleri, yapay zekanın yüksek hızlı kodlama ve optimizasyon yeteneğiyle birleşmiştir. Sonuç olarak ortaya; akademik ve profesyonel standartlara uygun, hatasız, dinamik ve interaktif bir Yön Cayrosu simülasyonu çıkmıştır.