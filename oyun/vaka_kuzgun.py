"""Vaka: Kuzgun Köşkü — Selim Aydın'ın ölümü.

Bu dosya yalnızca veri içerir. Yeni bir vaka yazmak için aynı yapıda
(KIMLIK, TOHUM, BRIFING, SUPHELILER, KANITLAR, IZINLER, SORULAR, IPUCLARI, COZUM)
bir modül oluşturmak yeterli.
"""
from datetime import datetime
from textwrap import dedent

KIMLIK = "kuzgun-kosku-v1"
BASLIK = "KUZGUN KÖŞKÜ"
YIL = 2026
TOHUM = 1403
OLAY_GECESI = (datetime(2026, 3, 13, 17, 0), datetime(2026, 3, 14, 8, 0))


def _z(s):
    return datetime.strptime(f"{s} {YIL}", "%d.%m %H:%M %Y") if s else None


def K(anahtar, tur, zaman, baslik, icerik, kisiler=(), kaynak="", konum="", paket=None):
    return dict(anahtar=anahtar, tur=tur, zaman=_z(zaman), baslik=baslik,
                icerik=dedent(icerik).strip(), kisiler=tuple(kisiler),
                kaynak=kaynak, konum=konum, paket=paket)


SELIM, LEYLA, DENIZ = "Selim Aydın", "Leyla Aydın", "Deniz Aydın"
BURAK, NERMIN, KEMAL = "Burak Tan", "Nermin Kaya", "Kemal Sarp"
ECE, ORHAN = "Ece Yıldız", "Orhan Demir"

BRIFING = """
14 Mart 2026, Cumartesi. Sarıyer, Kuzgun Köşkü.

Aydın Holding'in kurucusu Selim Aydın (62), sabah 07:10'da kâhyası Nermin Kaya
tarafından çalışma odasında, masasının başında ölü bulundu. Kapı akıllı kilitle
içeriden kilitliydi, pencere içeriden mandallıydı. Selim Bey kalp hastasıydı;
olay yerine ilk gelen ekip "kalp krizi" dedi ve dosyayı kapatmaya hazırlandı.

Komiser Aslı Güneş ikna olmadı. Otopsi ve toksikoloji sonuçları geldi; köşkün
kameraları, telefonlar, ifadeler, faturalar, fotoğraflar toplandı. Hepsi
önündeki arşivde. Çoğu önemsiz gündelik kayıt. Bazıları her şeyi değiştiriyor.

"Bana bir isim getirme," dedi Komiser Güneş. "Bana ne olduğunu getir.
Kim, nasıl, ne zaman, neden. Kanıtıyla."

GÖREVİN: Suçun nasıl gerçekleştiğini bul. Hazır olduğunda 'sucla' yaz.
"""

MAKTUL = (
    "Selim Aydın (62) — Aydın Holding'in kurucusu ve yönetim kurulu başkanı. "
    "Kalp yetmezliği ve ritim bozukluğu nedeniyle günde bir tablet digoksin (0,25 mg) kullanıyordu. "
    "Disiplinli, inatçı, sırlarını kendine saklayan biri olarak tanınıyordu."
)

SUPHELILER = {
    "leyla": dict(ad=LEYLA, yas=41, rol="Selim'in ikinci eşi",
                  profil="Altı yıldır evliler. Eski galeri sahibi. Evliliklerinde sorunlar "
                         "olduğu, aile doktoruyla fazla yakın olduğu konuşuluyor. Olay gecesi köşkteydi."),
    "deniz": dict(ad=DENIZ, yas=29, rol="Selim'in ilk evliliğinden oğlu",
                  profil="Holding'de 'danışman' unvanı var ama işe nadiren uğruyor. Ciddi borçları "
                         "olduğu söyleniyor. Olay akşamı babasıyla para yüzünden tartıştı."),
    "burak": dict(ad=BURAK, yas=47, rol="Aydın Holding Finans Direktörü",
                  profil="On beş yıldır Selim'in sağ kolu, aileden biri gibi. Olay akşamı köşke "
                         "gelip Selim'le çalışma odasında toplantı yaptı."),
    "nermin": dict(ad=NERMIN, yas=55, rol="Köşkün kâhyası",
                   profil="Yirmi yıldır ailenin yanında. Bahçedeki müştemilatta yaşıyor. Selim'in "
                          "akşam çayını o hazırlar. Cesedi bulan kişi."),
    "kemal": dict(ad="Dr. Kemal Sarp", yas=50, rol="Aile doktoru",
                  profil="Selim'in kalp ilacını yazan hekim. Leyla Aydın'la yakınlığı dikkat çekiyor."),
}

KANITLAR = [
    # ------------------------------------------------------------------ BELGELER
    K("otopsi", "belge", "14.03 16:30", "Otopsi raporu", """
        ADLİ TIP KURUMU — ÖN OTOPSİ RAPORU
        Maktul: Selim Aydın, 62, erkek

        Dış muayene: Darp izi, boğma izi, savunma yarası YOK. İğne izi YOK.
        Kalp: Kronik kalp yetmezliğiyle uyumlu genişleme. Taze enfarktüs (kalp krizi) bulgusu YOK.

        Toksikoloji (kan):
          Digoksin ........ 9,8 ng/mL   (tedavi aralığı: 0,5 – 2,0 ng/mL)
          Alkol ........... negatif
          Benzodiazepin / uyku ilacı ... negatif

        Mide içeriği: Ihlamur çayı (yaklaşık 250 mL), az miktarda sindirilmiş yemek
        (akşam yemeği ~19:30 ile uyumlu).

        SONUÇ: Ölüm, akut digoksin zehirlenmesine bağlı ölümcül kalp ritim bozukluğu
        sonucu gerçekleşmiştir. Kan düzeyi, tek seferde yaklaşık 2,5–3,5 mg digoksin
        (0,25 mg'lık tabletten 10–14 adet) alınmasıyla uyumludur.

        Tahmini ölüm zamanı: 14.03.2026 00:30 – 01:30.
    """, [SELIM], kaynak="Adli Tıp Kurumu"),

    K("lab_cay", "belge", "14.03 18:05", "Toksikoloji raporu — sıvı örnekleri", """
        KRİMİNAL LABORATUVAR — SIVI ÖRNEKLERİ ANALİZİ

        Örnek                                   Digoksin
        ─────────────────────────────────────── ──────────
        1) Termos (çalışma odası, masa üstü)     YÜKSEK
        2) Porselen fincan (çalışma odası)       YÜKSEK
        3) Demlik (mutfak, ocak üstü)            NEGATİF
        4) Demlikte kalan ıhlamur                NEGATİF
        5) Çay süzgeci (mutfak, bulaşık sepeti)  NEGATİF

        Termostaki konsantrasyon, çözünmüş tablet ile uyumludur; çözünmemiş
        tablet kaplaması parçacıkları mevcuttur (tabletler ezilerek katılmış).
    """, [SELIM], kaynak="Kriminal Laboratuvar"),

    K("hap_sayimi", "belge", "14.03 11:20", "İlaç sayım tutanağı", """
        OLAY YERİ İNCELEME — İLAÇ SAYIM TUTANAĞI
        Konum: Çalışma masası, sağ üst çekmece

        İlaç: Digoksin 0,25 mg tablet (eczane etiketi: 01.03.2026, 30 tablet, "günde 1")
        Şişede bulunan: 4 tablet

        Haftalık ilaç kutusu (masa üstü):
          Pzt–Cuma bölmeleri boş (alınmış), Cumartesi ve Pazar bölmeleri dolu.

        Aile beyanı: Selim Bey haftalık kutuyu her pazar şişeden kendisi doldururdu.

        Hesap (inceleme ekibi notu):
          01.03 (Pazar) 30 tablet — kutuya 7 → şişede 23
          08.03 (Pazar) kutuya 7 → şişede 16
          14.03 sabahı şişede olması gereken: 16
          Bulunan: 4  →  EKSİK: 12 tablet
    """, [SELIM], kaynak="Olay yeri inceleme ekibi", konum="Çalışma odası"),

    K("saat_verisi", "belge", "13.03 23:40", "Akıllı saat verisi — Selim Aydın", """
        AKILLI SAAT DIŞA AKTARIMI (bulut hesabından, savcılık talebiyle)

        Saat    Nabız   Ritim            Adım (son 10 dk)
        21:00    72     normal              14
        21:50    75     normal              31
        21:58    78     normal             186
        22:10    80     normal               9
        22:20    74     normal              22
        23:00    70     normal               5
        23:30    66     normal               0
        23:40    58     DÜZENSİZ uyarısı     3
        23:50    51     DÜZENSİZ            12
        00:10    44     DÜZENSİZ             0
        00:30    38     DÜZENSİZ             0
        00:50    31     DÜZENSİZ             0
        01:05    22     DÜZENSİZ             0
        01:12    ---    sinyal kaybı / nabız algılanamadı

        Not: Saat 23:41'de "düzensiz ritim" bildirimi gönderdi; bildirim okunmadı.
    """, [SELIM], kaynak="Akıllı saat üreticisi"),

    K("kilit_kaydi", "belge", "13.03 22:14", "Akıllı kilit kayıtları — çalışma odası", """
        AKILLI KİLİT OLAY GÜNLÜĞÜ — Çalışma odası kapısı

        13.03 08:51  Kilit açıldı — içeriden, döner topuz
        13.03 22:14  Kilitlendi   — içeriden, döner topuz
        14.03 02:14  Dışarıdan kol denemesi (kilitli, açılmadı)
        14.03 07:10  Kilit açıldı — yönetici kodu #2 (Nermin Kaya'ya tanımlı)

        Teknik not: Bu model dışarıdan yalnızca kod ya da telefon uygulamasıyla
        kilitlenebilir; bu tür bir işlem kayıtlarda yok. 13.03 22:14 ile 14.03 07:10
        arasında kilit açılmamıştır.
    """, [SELIM, NERMIN], kaynak="Kilit üreticisi bulut kaydı", konum="Çalışma odası"),

    K("hts_selim", "belge", "13.03 21:51", "HTS kaydı — Selim Aydın", """
        HTS (ARAMA KAYITLARI) — Selim Aydın, 13.03.2026

        09:40  Giden    Av. Orhan Demir                     4 dk 02 sn
        14:20  SMS      Burak Tan
        18:05  Gelen    Deniz Aydın                         1 dk 12 sn
        21:51  Gelen    Ece Yıldız (Aydın Holding – Finans) 6 dk 40 sn
        23:47  WhatsApp Leyla Aydın (3 mesaj)
        23:49  Giden    Nermin Kaya          cevapsız → sesli mesaja düştü
        23:51  Giden    Leyla Aydın          cevapsız
        23:53  Giden    (tuşlanmaya başlanmış, tamamlanmamış: "11")
    """, [SELIM, ECE, NERMIN, LEYLA, DENIZ, ORHAN], kaynak="Operatör / savcılık"),

    K("ece_ifade", "belge", "14.03 15:10", "İfade tutanağı — Ece Yıldız", """
        İFADE TUTANAĞI — Ece Yıldız (28), Burak Tan'ın yönetici asistanı

        "Burak Bey dün öğlen bana bir iş verdi: akşam 21:50 civarı Selim Bey'i arayıp
        Ege Lojistik sözleşmesinin 7. maddesini sormamı istedi. 'Uzun uzun sor,
        acelesi yok, detaylara gir' dedi. Garip buldum, çünkü o maddeyi Burak Bey
        benden çok daha iyi bilir. Hem neden kendisi sormuyor, zaten Selim Bey'in
        yanında olacaktı?

        21:49'da Burak Bey'den 'Şimdi ara.' diye mesaj geldi, aradım. Selim Bey biraz
        sinirliydi ama konuştuk. Hat cızırdadı, 'dur koridora çıkıyorum, odada
        çekmiyor' dedi. Yaklaşık yedi dakika konuştuk.

        Gece Burak Bey 'teşekkürler' yazdı, bir de bu konuşmayı kimseye söylememe
        gerek olmadığını. Sabah haberi duyunca... size gelmem gerektiğini düşündüm."
    """, [ECE, BURAK, SELIM], kaynak="Sarıyer Emniyet — Cinayet Büro"),

    K("burak_ifade", "belge", "14.03 13:00", "İfade tutanağı — Burak Tan", """
        İFADE TUTANAĞI — Burak Tan (47), Aydın Holding Finans Direktörü

        "Saat 21:30 gibi köşke vardım. Rutin bir bütçe toplantısıydı. Selim gayet
        iyiydi, keyfi yerindeydi. Toplantı boyunca Selim odadan hiç çıkmadı, ben de
        çıkmadım. 22:00 gibi ayrıldım, doğruca arabama gidip evime döndüm.

        Ege Lojistik mi? Hayır, onu konuşmadık, gündemde önemli bir konu yoktu.
        Selim'in ilaçlarını nerede tuttuğunu bilmem, hiç ilgilenmedim.

        On beş yıllık dostumu kaybettim. Başka söyleyecek bir şeyim yok."
    """, [BURAK, SELIM], kaynak="Sarıyer Emniyet — Cinayet Büro"),

    K("nermin_ifade", "belge", "14.03 09:30", "İfade tutanağı — Nermin Kaya", """
        İFADE TUTANAĞI — Nermin Kaya (55), kâhya

        "Selim Bey her akşam 21:00'de ıhlamur ister. Demler, termosa koyup odasına
        bırakırım. Hemen içmez, 23:00'ten sonra içer, 'gece çayım' derdi.

        Çalışırken kapısını içeriden kilitler, rahatsız edilmek istemezdi. Odada
        telefon çekmez; hep koridora çıkıp pencerenin önünde konuşurdu. Bunu evde
        herkes bilir, sık gelen Burak Bey de bilir.

        İlaçlarını masasının sağ çekmecesinde tutardı. Geçen ay Burak Bey toplantıdayken
        Selim Bey'in ilacını çekmeceden kendisi çıkarıp vermişti, hatırlıyorum.

        Dün 21:05'te termosu bıraktım; Selim Bey masasındaydı, başını kaldırmadı bile.
        Sonra arka kapıdan müştemilattaki odama geçtim. Telefonum sessizdeydi; sabah
        bir cevapsız arama ve sesli mesaj gördüm... dinleyemedim bile.
        07:10'da kapıyı çaldım, açılmayınca kodumla açtım. Selim Bey masanın başındaydı."

        Not (ifadeyi alan memur): Mutfakta yalnızca sarı kauçuk bulaşık eldiveni
        kullandığını, evde başka tür eldiven bulunmadığını beyan etti.
    """, [NERMIN, SELIM, BURAK], kaynak="Sarıyer Emniyet — Cinayet Büro"),

    K("leyla_ifade", "belge", "14.03 10:40", "İfade tutanağı — Leyla Aydın", """
        İFADE TUTANAĞI — Leyla Aydın (41), maktulün eşi

        "Akşam 20:30 gibi çalışma odasında tartıştık, evet. Birileri ona Kemal'le
        ilgili bir şeyler anlatmış. Pazartesi avukatıyla görüşüp vasiyeti
        değiştireceğini söyledi. Çok kırıldım.

        Salonda oturdum, sonra 22:40 gibi uyku ilacımı alıp yattım. Telefonum
        her gece olduğu gibi sessizdeydi. Mesajlarını sabah 07:14'te gördüm...
        Beni çağırmış. Uyanmadım."
    """, [LEYLA, SELIM, KEMAL, ORHAN], kaynak="Sarıyer Emniyet — Cinayet Büro"),

    K("deniz_ifade", "belge", "14.03 12:15", "İfade tutanağı — Deniz Aydın", """
        İFADE TUTANAĞI — Deniz Aydın (29), maktulün oğlu

        "Babamdan para istedim, vermedi. Sinirlendim, 'pişman olacaksın' dedim, lafın
        gelişi. Akşam 21:00 gibi çıktım, önce Emre'yle Bebek sahilinde yürüdük, sonra
        Kolonya Bar'a geçtik.

        02:00 gibi taksiyle döndüm. Babamın kapısını açmaya çalıştım, konuşmak,
        özür dilemek istiyordum. Kilitliydi. Uyuyor sandım. Kapıyı zorlamadım."
    """, [DENIZ, SELIM], kaynak="Sarıyer Emniyet — Cinayet Büro"),

    K("kemal_ifade", "belge", "14.03 14:00", "İfade tutanağı — Dr. Kemal Sarp", """
        İFADE TUTANAĞI — Dr. Kemal Sarp (50), aile hekimi

        "Selim Bey'in digoksinini ben yazıyorum, günde bir tablet. Şubat'taki kan
        düzeyi tedavi aralığındaydı. Çok disiplinli bir hastaydı, ilacını asla
        aksatmaz, fazla da almazdı.

        O gece Boğaz Hastanesi'nde nöbetteydim. Leyla Hanım'la ilişkim... bu benim
        özel hayatım, ölümle bir ilgisi yok."
    """, [KEMAL, SELIM, LEYLA], kaynak="Sarıyer Emniyet — Cinayet Büro"),

    K("orhan_ifade", "belge", "14.03 17:20", "İfade tutanağı — Av. Orhan Demir", """
        İFADE TUTANAĞI — Av. Orhan Demir (58), Selim Aydın'ın avukatı

        "Pazartesi 10:00 randevumuz vasiyetle ilgili değildi. Selim Bey, Ege Lojistik
        hesaplarında Burak Tan'ın imzasıyla yapılmış 4,2 milyon liralık usulsüzlük
        tespit etmişti. Birlikte savcılığa suç duyurusunda bulunacaktık.

        Konuyu kimseye, eşine bile söylemek istemedi. 'Soran olursa vasiyet işi
        deriz' dedi. Burak'la konuşmamasını da tembihledim ama inatçıydı:
        'On beş yıllık dostum, yüzüne söyleyeceğim' dedi."
    """, [ORHAN, SELIM, BURAK, LEYLA], kaynak="Sarıyer Emniyet — Cinayet Büro"),

    K("orhan_eposta", "belge", "12.03 22:47", "E-posta: Selim Aydın → Av. Orhan Demir", """
        Kimden: Selim Aydın
        Kime:   Av. Orhan Demir
        Konu:   Pazartesi

        Orhan,
        Ege Lojistik hesaplarını baştan sona inceledim. Son 18 ayda Burak'ın imzasıyla
        "Marmara Tedarik" ve "Kıyı Danışmanlık" adlı iki firmaya toplam 4,2 milyon TL
        çıkmış. İki firma da hiçbir iş yapmamış. Pazartesi 10:00'da seninle savcılığa
        gidelim, dosyayı hazırladım.
        Kimseye söylemiyorum, Leyla'ya bile. Soran olursa vasiyet işi deriz.
        — S.

        ---- Yanıt (12.03 23:05) ----
        Anlaşıldı. Dosyanın bir kopyasını bende de bırak. Burak'a sakın belli etme.
        — O.
    """, [SELIM, ORHAN, BURAK, LEYLA], kaynak="Selim Aydın'ın e-posta hesabı"),

    K("muhasebe_eposta", "belge", "09.03 10:02", "E-posta: Muhasebe → Selim Aydın (bilgi: Burak Tan)", """
        Kimden: Aydın Holding Muhasebe
        Kime:   Selim Aydın
        Bilgi:  Burak Tan
        Konu:   Talep ettiğiniz döküm

        Selim Bey,
        Talep ettiğiniz Ege Lojistik'e ait son 18 aylık ödeme dökümü ve fatura
        listesi ektedir. Ek bilgi gerekirse lütfen haber veriniz.
        Saygılarımızla.
    """, [SELIM, BURAK], kaynak="Aydın Holding e-posta sunucusu"),

    K("vasiyet", "belge", "14.03 12:40", "Vasiyetname (2019) — noter onaylı suret", """
        VASİYETNAME — Selim Aydın (düzenleme tarihi: 17.06.2019)

        - Aydın Holding hisseleri: %40 Leyla Aydın, %40 Deniz Aydın, %20 Aydın Eğitim Vakfı
        - Kuzgun Köşkü: Leyla Aydın
        - Nermin Kaya'ya 1.000.000 TL ve köşkün müştemilatında ömür boyu oturma hakkı

        Vasiyetname 2019'dan bu yana değiştirilmemiştir.
    """, [SELIM, LEYLA, DENIZ, NERMIN], kaynak="Noterlik"),

    K("bilet", "belge", "10.03 19:22", "Rezervasyon: İstanbul — Lizbon", """
        UÇUŞ REZERVASYONU — Onay kodu: KZ7Q2M

        Yolcular: Selim Aydın, Leyla Aydın
        Gidiş: 10.04.2026 İstanbul → Lizbon 09:40
        Dönüş: 20.04.2026 Lizbon → İstanbul 16:15
        Otel: 10 gece, deniz manzaralı süit

        Rezervasyonu yapan: Selim Aydın (10.03.2026 19:22)
        Not alanı: "Evlilik yıldönümü — sürpriz, Leyla'ya söyleme."
    """, [SELIM, LEYLA], kaynak="Selim Aydın'ın e-posta hesabı"),

    K("kemal_nobet", "belge", "14.03 13:30", "Boğaz Hastanesi — personel giriş/çıkış kaydı", """
        ÖZEL BOĞAZ HASTANESİ — PERSONEL KART KAYITLARI
        Personel: Dr. Kemal Sarp (Dahiliye)

        13.03 19:52  Giriş — personel kapısı
        13.03 23:10–23:40  Acil serviste 3 hasta muayene kaydı (imzalı)
        14.03 01:05  Yoğun bakım konsültasyonu (imzalı)
        14.03 03:30  Servis vizitesi
        14.03 08:06  Çıkış — personel kapısı

        Arada binadan çıkış kaydı yok. Otopark kamerası aracın gece boyunca yerinde
        kaldığını gösteriyor.
    """, [KEMAL], kaynak="Hastane güvenlik birimi"),

    K("deniz_bar", "belge", "14.03 01:48", "Kolonya Bar — adisyon ve kamera özeti", """
        KOLONYA BAR (Bebek) — Masa 7

        Adisyon açılış: 13.03 22:14   Kapanış: 14.03 01:48
        Ödeme: Kredi kartı — Deniz Aydın — 4.860 TL

        Bar kamerası özeti (işletme tarafından teslim edildi):
          22:10  Deniz Aydın ve bir arkadaşı içeri giriyor
          22:10–01:52 arası Deniz Aydın mekândan ayrılmıyor (tuvalet dahil tüm
          çıkışlar kamerada)
          01:52  Mekândan çıkıyor, taksiye biniyor
    """, [DENIZ], kaynak="Kolonya Bar işletmesi"),

    K("eczane_leyla", "belge", "12.03 17:10", "Eczane fişi — Leyla Aydın", """
        SAHİL ECZANESİ — Satış fişi

        Hasta: Leyla Aydın
        Reçeteli: Zolpidem 10 mg, 20 tablet (Dr. Kemal Sarp)
        Diğer: El kremi, C vitamini
        Tutar: 612,40 TL
    """, [LEYLA, KEMAL], kaynak="Leyla Aydın'ın cüzdanı"),

    K("erecete", "belge", "01.03 10:15", "e-Reçete kaydı — Selim Aydın", """
        e-REÇETE
        Hasta: Selim Aydın
        Hekim: Dr. Kemal Sarp
        İlaç: Digoksin 0,25 mg — 30 tablet — Günde 1 x 1
        Karşılandı: 01.03.2026, Sahil Eczanesi
    """, [SELIM, KEMAL], kaynak="Sağlık Bakanlığı sistemi"),

    K("ik_nermin", "belge", "11.03 16:00", "İK yazısı taslağı — Nermin Kaya", """
        AYDIN AİLESİ — PERSONEL YAZISI (TASLAK)

        Konu: Nermin Kaya'nın emekliliği
        Selim Bey'in talimatıyla: Nermin Hanım 1 Haziran itibarıyla emekliye
        ayrılacak. Kendisine 1,5 milyon TL teşekkür ikramiyesi ödenecek; müştemilatta
        oturmaya devam edecek. Yerine gelecek kişiyi kendisi yetiştirecek.
        Selim Bey'in notu: "Yirmi yıl. Hak ettiğinden fazlasını almalı."
    """, [NERMIN, SELIM], kaynak="Selim Aydın'ın bilgisayarı"),

    K("kamera_senkron", "belge", "04.03 10:00", "Güvenlik sistemi bakım raporu", """
        GÜVENLİK SİSTEMİ PERİYODİK BAKIM RAPORU — Kuzgun Köşkü

        - 9 kamera aktif: Ana kapı, Koridor-1, Mutfak, Arka kapı, Garaj, Bahçe-1,
          Bahçe-2, Havuz, Ön cephe.
        - Tüm kameralar zaman sunucusuyla senkron; sapma < 1 saniye.
        - Koridor-1 kamerası çalışma odası kapısını, misafir WC kapısını ve yatak
          odaları kanadına geçişi kesintisiz görüyor. Hareket algılamalı kayıt.
        - Çalışma odası ve misafir WC içinde kamera YOK (mahremiyet).
        - Çalışma odası penceresi dışarıdan açılamaz tipte, alarm sensörlü.
    """, [], kaynak="Güvenlik firması"),

    # ------------------------------------------------------------------ KAMERA
    K("kam_leyla_giris", "kamera", "13.03 20:24", "Koridor-1 kamerası", """
        ▶ Kayıt 20:24:05 – 20:41:30
        20:24  Leyla Aydın çalışma odasının kapısını çalmadan açıp içeri giriyor.
        20:41  Hızlı adımlarla çıkıyor, kapıyı sertçe kapatıyor, salona yöneliyor.
               Elinde bir şey yok.
    """, [LEYLA], kaynak="Köşk güvenlik sistemi", konum="Koridor-1"),

    K("kam_deniz_cikis", "kamera", "13.03 20:52", "Ana kapı kamerası", """
        ▶ Kayıt 20:52:14 – 20:53:40
        Deniz Aydın dışarı çıkıyor, siyah BMW'sine binip köşkten ayrılıyor.
    """, [DENIZ], kaynak="Köşk güvenlik sistemi", konum="Ana kapı"),

    K("kam_mutfak", "kamera", "13.03 20:58", "Mutfak kamerası", """
        ▶ Kayıt 20:58:02 – 21:03:15
        Nermin Kaya demliği ocaktan alıyor. Ihlamuru süzgeçle doğrudan termosa
        döküyor, kapağını kapatıyor. Tezgâhta başka kap, paket ya da şişe yok;
        elleri kayıt boyunca görüş alanında. Süzgeci bulaşık sepetine bırakıyor.
        21:03'te termosla mutfaktan çıkıyor.
    """, [NERMIN], kaynak="Köşk güvenlik sistemi", konum="Mutfak"),

    K("kam_nermin_termos", "kamera", "13.03 21:05", "Koridor-1 kamerası", """
        ▶ Kayıt 21:05:10 – 21:07:02
        Nermin Kaya elinde termosla çalışma odasının kapısını çalıp giriyor.
        21:07'de eli boş çıkıyor, mutfak yönüne gidiyor.
        (Kapı açıkken içerisi kısmen görünüyor: Selim Aydın masasında oturuyor.)
    """, [NERMIN, SELIM], kaynak="Köşk güvenlik sistemi", konum="Koridor-1"),

    K("kam_nermin_arka", "kamera", "13.03 21:09", "Arka kapı kamerası", """
        ▶ Kayıt 21:09:40 – 21:10:05
        Nermin Kaya arka kapıdan çıkıp bahçedeki müştemilata yürüyor, içeri giriyor.
        Bu kayıttan sonra arka kapıda bir sonraki hareket: 14.03 07:04
        (Nermin Kaya ana binaya geçiyor).
    """, [NERMIN], kaynak="Köşk güvenlik sistemi", konum="Arka kapı"),

    K("kam_burak_gelis", "kamera", "13.03 21:36", "Ana kapı kamerası", """
        ▶ Kayıt 21:36:20 – 21:37:45
        Gri Volvo kapı önüne park ediyor. Burak Tan iniyor; elinde siyah deri evrak
        çantası var. Zili çalmadan kendi kartıyla giriyor (aileye yakın kişilere
        tanımlı giriş kartı).
    """, [BURAK], kaynak="Köşk güvenlik sistemi", konum="Ana kapı"),

    K("kam_burak_oda", "kamera", "13.03 21:38", "Koridor-1 kamerası", """
        ▶ Kayıt 21:38:02 – 21:38:30
        Burak Tan çalışma odasının kapısını çalıyor, içeri giriyor. Kapı kapanıyor.
    """, [BURAK], kaynak="Köşk güvenlik sistemi", konum="Koridor-1"),

    K("kam_selim_koridor", "kamera", "13.03 21:52", "Koridor-1 kamerası", """
        ▶ Kayıt 21:52:00 – 21:58:52
        21:52:00  Selim Aydın telefon kulağında, çalışma odasından çıkıyor. Kapıyı
                  arkasından çekiyor. Koridorun sonundaki pencerenin önüne yürüyor,
                  sırtı odaya dönük konuşuyor, bir ara pencereden dışarı bakıyor.
        21:58:40  Telefonu kapatıp odaya geri giriyor.

        Bu süre boyunca çalışma odasına giren ya da çıkan kimse yok.
        (Burak Tan odada.)
    """, [SELIM, BURAK], kaynak="Köşk güvenlik sistemi", konum="Koridor-1"),

    K("kam_burak_wc", "kamera", "13.03 22:12", "Koridor-1 kamerası", """
        ▶ Kayıt 22:12:05 – 22:15:30
        22:12:05  Burak Tan çalışma odasından çıkıyor, çantası elinde. Kapıyı kapatıyor.
        22:12:40  Giriş holüne değil, misafir WC'ye giriyor.
        22:15:05  WC'den çıkıyor, giriş holüne yürüyor.
    """, [BURAK], kaynak="Köşk güvenlik sistemi", konum="Koridor-1"),

    K("kam_burak_cikis", "kamera", "13.03 22:17", "Ana kapı kamerası", """
        ▶ Kayıt 22:17:10 – 22:19:30
        Burak Tan köşkten çıkıyor, Volvo'suna biniyor. Araç 22:19'da ayrılıyor.
        Bu saatten sonra gece boyunca ana kapıdan giriş: yalnızca 14.03 02:09.
    """, [BURAK], kaynak="Köşk güvenlik sistemi", konum="Ana kapı"),

    K("kam_leyla_yatak", "kamera", "13.03 22:36", "Koridor-1 kamerası", """
        ▶ Kayıt 22:36:15 – 22:36:40
        Leyla Aydın elinde bir bardak suyla salondan yatak odaları kanadına geçiyor.
        Çalışma odası kapısına yaklaşmıyor.
        Bu kamerada bir sonraki hareket algılaması: 14.03 02:14.
    """, [LEYLA], kaynak="Köşk güvenlik sistemi", konum="Koridor-1"),

    K("kam_deniz_donus", "kamera", "14.03 02:09", "Ana kapı kamerası", """
        ▶ Kayıt 02:09:20 – 02:10:10
        Bir taksi kapıda duruyor. Deniz Aydın iniyor, sendeleyerek içeri giriyor.
    """, [DENIZ], kaynak="Köşk güvenlik sistemi", konum="Ana kapı"),

    K("kam_deniz_kapi", "kamera", "14.03 02:14", "Koridor-1 kamerası", """
        ▶ Kayıt 02:14:02 – 02:15:20
        Deniz Aydın çalışma odasının kapı kolunu indiriyor; kapı açılmıyor. Hafifçe
        iki kez vuruyor, bir süre alnını kapıya dayayıp bekliyor. 02:15'te yatak
        odaları kanadına gidiyor.
    """, [DENIZ], kaynak="Köşk güvenlik sistemi", konum="Koridor-1"),

    K("kam_nermin_sabah", "kamera", "14.03 07:09", "Koridor-1 kamerası", """
        ▶ Kayıt 07:09:10 – 07:12:40
        Nermin Kaya çalışma odasının kapısını çalıyor, bekliyor, yeniden çalıyor.
        07:10 tuş takımına kod giriyor, kapıyı açıyor. 07:11 geri fırlıyor, elleri
        yüzünde, bağırarak yatak odaları kanadına koşuyor.
    """, [NERMIN], kaynak="Köşk güvenlik sistemi", konum="Koridor-1"),

    # ------------------------------------------------------------------ MESAJLAR
    K("selim_burak_msg", "mesaj", "13.03 14:20", "Selim Aydın → Burak Tan", """
        [13.03 14:20] Selim Aydın: Bu akşam köşke gel. Ege hesaplarını da getir. Konuşmamız lazım.
        [13.03 14:26] Burak Tan: Tabii. 21:30 gibi oradayım.
    """, [SELIM, BURAK], kaynak="Selim Aydın'ın telefonu"),

    K("deniz_selim_msg", "mesaj", "13.03 18:07", "Deniz Aydın → Selim Aydın", """
        [13.03 18:07] Deniz Aydın: Baba 300 bin lazım. Son kez. Yemin ederim son kez.
        [13.03 18:09] Selim Aydın: Bir kuruş daha yok. Kendi ayaklarının üstünde dur artık.
        [13.03 18:10] Deniz Aydın: Pişman olacaksın.
    """, [DENIZ, SELIM], kaynak="Selim Aydın'ın telefonu"),

    K("deniz_emre_msg", "mesaj", "13.03 17:45", "Deniz Aydın → Emre Koç", """
        [13.03 17:45] Deniz Aydın: Tolga abiye pazartesiye kadar 300 vermem lazım
        [13.03 17:46] Emre Koç: babandan iste
        [13.03 17:48] Deniz Aydın: vermez. babam ölse bu dertlerin hepsi biter ha ha
        [13.03 17:48] Emre Koç: saçmalama
        [13.03 17:52] Emre Koç: akşam bebek? kafanı dağıtırız
        [13.03 17:53] Deniz Aydın: 9 gibi çıkarım
    """, [DENIZ, "Emre Koç"], kaynak="Emre Koç'un telefonu (gönüllü teslim)"),

    K("selim_leyla_msg", "mesaj", "13.03 23:47", "Selim Aydın → Leyla Aydın", """
        [13.03 23:47] Selim Aydın: Leyla midem çok bulanıyor. Her şey sarı sarı görünüyor
        [13.03 23:48] Selim Aydın: Uyanık mısın
        [13.03 23:52] Selim Aydın: kapıyı a
        (Okundu: 14.03 07:14)
    """, [SELIM, LEYLA], kaynak="Selim Aydın'ın telefonu"),

    K("nermin_zeynep_msg", "mesaj", "12.03 19:20", "Nermin Kaya → Zeynep Kaya", """
        [12.03 19:20] Nermin Kaya: Selim Bey beni emekliye ayırmak istiyormuş. Yirmi yıl Zeynep.
        [12.03 19:21] Nermin Kaya: Bir gün hepsi görecek. Anlatacağım her şeyi.
        [12.03 19:30] Zeynep Kaya: Sakin ol abla. Belki iyi bir şeydir, sen de dinlen artık.
        [12.03 19:44] Nermin Kaya: Kitabımı yazacağım o zaman. Bu evin yirmi yılını :)
    """, [NERMIN, "Zeynep Kaya"], kaynak="Nermin Kaya'nın telefonu (gönüllü teslim)"),

    K("burak_ece_msg_acik", "mesaj", "13.03 12:31", "Burak Tan → Ece Yıldız", """
        [13.03 12:31] Burak Tan: Ece akşam sana küçük bir iş vereceğim, telefonun açık olsun.
        [13.03 12:33] Ece Yıldız: Tamam Burak Bey.
    """, [BURAK, ECE], kaynak="Ece Yıldız'ın telefonu (gönüllü teslim)"),

    # ------------------------------------------------------------------ SES
    K("tartisma_ses", "ses", "13.03 20:31", "Akıllı hoparlör kaydı — çalışma odası", """
        ▶ Yanlışlıkla tetiklenen kayıt, 42 sn (uyandırma kelimesi algılandı)

        LEYLA: ...o dedikodulara inanıyorsan açık açık söyle!
        SELİM: Pazartesi Orhan'la görüşüyorum. Vasiyet dahil her şeyi yeniden düzenleyeceğim.
        LEYLA: Yap o zaman! Ama pişman olursun Selim.
        SELİM: Kapıyı kapat çıkarken.
        [kapı çarpması — kayıt sonu]
    """, [LEYLA, SELIM, ORHAN], kaynak="Akıllı hoparlör bulut kaydı", konum="Çalışma odası"),

    K("hoparlor_cay", "ses", "13.03 22:01", "Akıllı hoparlör kaydı — çalışma odası", """
        ▶ Yanlışlıkla tetiklenen kayıt, 31 sn

        BURAK: ...otur Selim, çayın soğuyor. Koyayım mı bir bardak?
        SELİM: Sonra içerim, gece çayım o. Konuyu değiştirme.
        SELİM: Ege'den çıkan o paralar Burak. Marmara Tedarik. Kıyı Danışmanlık.
               Eniştenin şirketleri. Pazartesi...
        [kayıt sonu]
    """, [BURAK, SELIM], kaynak="Akıllı hoparlör bulut kaydı", konum="Çalışma odası"),

    K("selim_sesli_not", "ses", "13.03 22:20", "Sesli not — Selim Aydın'ın telefonu", """
        ▶ Sesli not, 19 sn

        SELİM: Not. Burak her şeyi inkâr etti. Gözümün içine baka baka.
               Pazartesi saat on, Orhan, savcılık. Ege dosyasını kasaya koy... Yarın.
    """, [SELIM, BURAK, ORHAN], kaynak="Selim Aydın'ın telefonu"),

    K("nermin_sesli", "ses", "13.03 23:49", "Sesli mesaj — Nermin Kaya'nın telefonu", """
        ▶ Sesli mesaj, 14 sn (arayan: Selim Aydın)

        SELİM: [ağır nefes] Nermin... bana biraz... su getirir misin. Kendimi iyi
               hissetmiyorum. Kalbim... [öksürük] Gözlerim... her şey sapsarı...
               [uzun sessizlik — kayıt sonu]
    """, [SELIM, NERMIN], kaynak="Nermin Kaya'nın telefonu (gönüllü teslim)"),

    # ------------------------------------------------------------------ FOTOĞRAFLAR
    K("foto_genel", "foto", "14.03 07:52", "Olay yeri fotoğrafı #3", """
        Çalışma odası, genel görünüm.
        Selim Aydın masasının başında, koltuğunda öne doğru yığılmış. Sağ elinin
        yanında telefonu; son açık ekran: arama tuş takımı, tuşlanmış "11".
        Masada: termos, yarısı içilmiş porselen fincan, açık dosyalar, gözlük.
        Sağ üst çekmece yarı açık. Kapı içten kilitli bulunmuş, anahtar gerektirmeyen
        akıllı kilit.
    """, [SELIM], kaynak="Olay yeri inceleme ekibi", konum="Çalışma odası"),

    K("foto_termos", "foto", "14.03 07:55", "Olay yeri fotoğrafı #4", """
        Yakın plan: çelik termos ve porselen fincan.
        Fincanın dibinde ince, beyazımsı bir tortu. Termosun kapağı gevşek.
        Termosun gövdesinde yalnızca Nermin Kaya ve Selim Aydın'ın parmak izleri
        bulundu (sonradan eklenen not).
    """, [SELIM, NERMIN], kaynak="Olay yeri inceleme ekibi", konum="Çalışma odası"),

    K("foto_pencere", "foto", "14.03 07:58", "Olay yeri fotoğrafı #6", """
        Çalışma odası penceresi. Kol kilitli konumda, mandal içeriden takılı.
        Dış pervazdaki toz tabakası bozulmamış. Alarm sensörü gece boyunca
        tetiklenmemiş.
    """, [], kaynak="Olay yeri inceleme ekibi", konum="Çalışma odası"),

    K("masa_toz", "foto", "14.03 08:05", "Olay yeri fotoğrafı #9", """
        Yakın plan: deri masa sümeninin sol kenarı, ağır pirinç kâğıt ağırlığının hemen
        yanı. Sümenin dikiş çizgisine sıkışmış ince beyaz toz kalıntısı. Kâğıt
        ağırlığının taban kenarında da aynı toz.

        Laboratuvar ön test notu (14.03 13:40): Toz — DİGOKSİN POZİTİF.
        Ezilmiş tablet ile uyumlu. Kâğıt ağırlığında parmak izi yok (silinmiş).
    """, [], kaynak="Olay yeri inceleme ekibi", konum="Çalışma odası"),

    K("foto_ilac_kutusu", "foto", "14.03 08:08", "Olay yeri fotoğrafı #11", """
        Masa üstündeki haftalık ilaç kutusu (Pzt–Paz) ve çekmecedeki ilaç şişesi.
        Kutuda Pazartesi'den Cuma'ya bölmeler boş, Cumartesi ve Pazar dolu.
        Şişenin kapağı açık, içinde birkaç tablet.
    """, [SELIM], kaynak="Olay yeri inceleme ekibi", konum="Çalışma odası"),

    K("selim_not_foto", "foto", "14.03 08:14", "Olay yeri fotoğrafı #14", """
        Masa sümeninin altında bulunan el yazısı not (Selim Aydın'ın el yazısı):

          "B.T. — Ege — 4,2 M
           Marmara Tedarik / Kıyı Danışm. → kimin?
           → ikisi de Burak'ın eniştesi!!
           Pzt 10:00 Orhan → savcılık"
    """, [SELIM, BURAK, ORHAN], kaynak="Olay yeri inceleme ekibi", konum="Çalışma odası"),

    K("foto_leyla_komodin", "foto", "14.03 08:30", "Olay yeri fotoğrafı #21", """
        Leyla Aydın'ın komodini. Zolpidem kutusu (20'lik, 2 tablet eksik), yarım
        bardak su, telefon (sessiz modda, 'Rahatsız Etmeyin' 22:30–08:00 arası
        otomatik açık), okuma gözlüğü, bir roman.
    """, [LEYLA], kaynak="Olay yeri inceleme ekibi", konum="Yatak odası"),

    K("eldiven_foto", "foto", "14.03 09:40", "Olay yeri fotoğrafı #27", """
        Misafir WC, çöp kovası. Kâğıt havluların altına bastırılmış, buruşturulmuş
        TEK bir mavi nitril eldiven (sağ el). Parmak uçlarında beyaz toz izi.

        Not: Köşkte bu tür eldiven kullanan kimse yok; mutfakta yalnızca sarı kauçuk
        bulaşık eldivenleri var. Eldiven laboratuvara gönderildi.
        Ön test (parmak ucu tozu): DİGOKSİN POZİTİF.
    """, [], kaynak="Olay yeri inceleme ekibi", konum="Misafir WC"),

    K("foto_mutfak_eldiven", "foto", "14.03 09:55", "Olay yeri fotoğrafı #33", """
        Mutfak lavabosu altı dolap: iki çift sarı kauçuk bulaşık eldiveni,
        deterjanlar, sünger. Başka eldiven yok.
    """, [NERMIN], kaynak="Olay yeri inceleme ekibi", konum="Mutfak"),

    # ------------------------------------------------------------------ ARAMA İZNİ PAKETLERİ
    # Burak Tan
    K("burak_sms", "mesaj", "13.03 21:49", "Burak Tan → Ece Yıldız (Burak'ın telefonundan)", """
        [13.03 12:35] Burak Tan: Akşam 21:50 gibi Selim Bey'i ara. Ege sözleşmesi 7. maddeyi sor. Uzun tut. Ben haber vereceğim.
        [13.03 21:49] Burak Tan: Şimdi ara.
        [13.03 22:31] Burak Tan: Teşekkürler Ece. Bu konuşmayı kimseye söylemene gerek yok, iç yazışma.
        [13.03 22:33] Ece Yıldız: Tamam Burak Bey, iyi geceler.
    """, [BURAK, ECE], kaynak="Burak Tan'ın telefonu (arama izni)", paket="burak"),

    K("burak_tarama", "belge", "11.03 23:15", "Tarayıcı geçmişi — Burak Tan", """
        TARAYICI GEÇMİŞİ — Burak Tan'ın kişisel telefonu (silinmiş kayıtlar kurtarıldı)

        09.03 22:40  "iç denetim zimmet ceza kaç yıl"
        09.03 22:52  "güveni kötüye kullanma nitelikli dolandırıcılık farkı"
        11.03 23:12  "digoksin zehirlenmesi belirtileri"
        11.03 23:15  "digoksin kaç tablet öldürür"
        11.03 23:21  "digoksin çayda tadı belli olur mu"
        11.03 23:34  "ıhlamur digoksin"
        11.03 23:40  "nitril eldiven parmak izi bırakır mı"
        12.03 08:10  "digoksin otopside çıkar mı kalp hastası"
    """, [BURAK], kaynak="Burak Tan'ın telefonu (arama izni)", paket="burak"),

    K("eldiven_dna", "belge", "15.03 11:00", "DNA karşılaştırma raporu — nitril eldiven", """
        KRİMİNAL LABORATUVAR — BİYOLOJİ ŞUBESİ

        Delil: Misafir WC çöp kovasından alınan mavi nitril eldiven (sağ el)
        İncelenen: Eldivenin iç yüzeyinden alınan epitel hücreleri

        Karşılaştırma (arama izni kapsamında alınan referans örnek):
          Burak Tan ............ UYUMLU (eşleşme olasılığı > 1 / 10 milyar)

        Eldiven dış yüzeyi parmak uçlarında digoksin kalıntısı doğrulandı.
    """, [BURAK], kaynak="Kriminal Laboratuvar (arama izni)", paket="burak"),

    K("burak_banka", "belge", "14.03 19:00", "Banka inceleme raporu — Burak Tan", """
        MASAK / BANKA İNCELEMESİ (arama izni kapsamında)

        Marmara Tedarik Ltd. — Ortak: Serkan Uysal (Burak Tan'ın eniştesi)
        Kıyı Danışmanlık — Ortak: Serkan Uysal

        Son 18 ayda Aydın Holding / Ege Lojistik'ten gelen: 4.212.000 TL
        Bu tutarın 3.680.000 TL'si, gelişinden 1–3 gün sonra Burak Tan'ın
        yurt dışındaki hesabına aktarılmış.
    """, [BURAK], kaynak="MASAK (arama izni)", paket="burak"),

    # Leyla Aydın
    K("leyla_kemal_msg", "mesaj", "13.03 22:58", "Leyla Aydın → Kemal Sarp (Leyla'nın telefonundan)", """
        [13.03 22:58] Leyla Aydın: Bu akşam kavga ettik. Birisi ona bizi anlatmış. Vasiyeti değiştirecekmiş.
        [13.03 22:59] Leyla Aydın: İlacımı aldım yatıyorum. Yarın konuşalım.
        [13.03 23:02] Kemal Sarp: Nöbetteyim, acil dolu. Lütfen sakin ol, bir şey yapma. Yarın konuşuruz.
        [13.03 23:05] Leyla Aydın: İyi geceler.
    """, [LEYLA, KEMAL], kaynak="Leyla Aydın'ın telefonu (arama izni)", paket="leyla"),

    K("leyla_tarama", "belge", "10.03 01:20", "Tarayıcı geçmişi — Leyla Aydın", """
        TARAYICI GEÇMİŞİ — Leyla Aydın

        08.03 00:45  "anlaşmalı boşanma kaç ayda biter"
        08.03 00:52  "evlilik sözleşmesi yoksa mal paylaşımı"
        10.03 01:20  "boşanma avukatı sarıyer"
        12.03 16:30  "zolpidem alkol ile alınır mı"
    """, [LEYLA], kaynak="Leyla Aydın'ın telefonu (arama izni)", paket="leyla"),

    K("leyla_konum", "belge", "14.03 07:14", "Telefon hareket verisi — Leyla Aydın", """
        TELEFON SENSÖR VE EKRAN KAYITLARI — Leyla Aydın

        22:58–23:05  Ekran açık (mesajlaşma)
        23:05–07:13  Ekran kapalı, cihaz hareketsiz (yatak odası Wi-Fi erişim noktası)
        07:14        Ekran açık, WhatsApp açıldı
    """, [LEYLA], kaynak="Leyla Aydın'ın telefonu (arama izni)", paket="leyla"),

    # Deniz Aydın
    K("deniz_tolga_msg", "mesaj", "12.03 23:30", "Tolga → Deniz Aydın (Deniz'in telefonundan)", """
        [12.03 23:30] Tolga: pazartesi son gün deniz. 300. yoksa arabanı alırız, sonra sen düşün
        [12.03 23:41] Deniz Aydın: abi hallediyorum babamla konuşcam
        [14.03 11:02] Tolga: başın sağolsun. borç yine borç ama
    """, [DENIZ, "Tolga"], kaynak="Deniz Aydın'ın telefonu (arama izni)", paket="deniz"),

    K("deniz_konum", "belge", "14.03 02:08", "Konum geçmişi — Deniz Aydın", """
        KONUM GEÇMİŞİ — Deniz Aydın

        20:53–21:05  Sarıyer → Bebek (araç)
        21:10–22:05  Bebek sahil yürüyüş yolu
        22:10–01:52  Kolonya Bar, Bebek
        01:55–02:08  Taksi, Bebek → Sarıyer
        02:09        Kuzgun Köşkü
        (Araç gece boyunca Bebek'te park halinde.)
    """, [DENIZ], kaynak="Deniz Aydın'ın telefonu (arama izni)", paket="deniz"),
]

# Arama izni: savcı, gerekçe listesindeki kanıtlardan en az 'esik' kadarını
# incelemiş olmanı bekler. Oyun boyunca en fazla IZIN_HAKKI kadar izin alınabilir.
IZIN_HAKKI = 2
IZINLER = {
    "burak": dict(
        gerekce=["burak_ifade", "kam_selim_koridor", "ece_ifade", "hts_selim", "orhan_eposta",
                 "orhan_ifade", "selim_burak_msg", "kam_burak_wc", "eldiven_foto",
                 "hoparlor_cay", "selim_not_foto", "selim_sesli_not"],
        esik=3,
        kabul="Savcı Burak Tan'ın telefonu, banka hesapları ve DNA referans örneği için izni onayladı.",
    ),
    "leyla": dict(
        gerekce=["tartisma_ses", "leyla_ifade", "eczane_leyla", "kam_leyla_giris", "selim_leyla_msg",
                 "foto_leyla_komodin"],
        esik=2,
        kabul="Savcı Leyla Aydın'ın telefonu için izni onayladı.",
    ),
    "deniz": dict(
        gerekce=["deniz_selim_msg", "deniz_emre_msg", "kam_deniz_kapi", "deniz_ifade", "kam_deniz_donus"],
        esik=2,
        kabul="Savcı Deniz Aydın'ın telefonu ve konum geçmişi için izni onayladı.",
    ),
    "nermin": dict(red="Nermin Kaya telefonunu zaten gönüllü olarak teslim etti; ilgili kayıtlar dosyada."),
    "kemal": dict(red="Dr. Kemal Sarp'ın hastane kayıtları zaten dosyada. Savcı ek izni gereksiz buldu."),
}

SUPHELI_SECENEKLERI = ["Leyla Aydın", "Deniz Aydın", "Burak Tan", "Nermin Kaya", "Dr. Kemal Sarp"]

SORULAR = [
    dict(soru="Bu olay nedir?",
         secenekler=["Doğal ölüm (kalp krizi)", "Kaza (Selim yanlışlıkla fazla ilaç aldı)", "İntihar", "Cinayet"],
         dogru=3,
         destek=["hap_sayimi", "foto_ilac_kutusu", "masa_toz", "lab_cay", "eldiven_foto", "bilet",
                 "kemal_ifade", "otopsi"]),
    dict(soru="Ölüm nedeni neydi?",
         secenekler=["Kalp krizi", "Digoksin (kalp ilacı) zehirlenmesi", "Uyku ilacı zehirlenmesi", "Boğulma"],
         dogru=1,
         destek=["otopsi", "saat_verisi", "selim_leyla_msg", "nermin_sesli", "lab_cay"]),
    dict(soru="Ölüm hangi saat aralığında gerçekleşti?",
         secenekler=["21:00 – 22:00", "22:00 – 23:00", "23:00 – 00:00", "00:30 – 01:30", "02:00 – 03:00"],
         dogru=3,
         destek=["otopsi", "saat_verisi"]),
    dict(soru="Zehir neye ve nerede katıldı?",
         secenekler=["Mutfakta, demlikteki çaya", "Çalışma odasında, termostaki çaya",
                     "İlaç kutusundaki haplar değiştirilerek", "Akşam yemeğine"],
         dogru=1,
         destek=["lab_cay", "kam_mutfak", "masa_toz", "eldiven_foto", "hoparlor_cay"]),
    dict(soru="Suçu kim işledi?",
         secenekler=SUPHELI_SECENEKLERI,
         dogru=2,
         destek=["kam_selim_koridor", "ece_ifade", "burak_ifade", "eldiven_dna", "burak_tarama",
                 "kam_burak_wc", "eldiven_foto", "burak_sms", "hoparlor_cay"]),
    dict(soru="Katil zehri katmak için odada nasıl yalnız kaldı?",
         secenekler=["Selim uyurken gece odaya girdi", "Selim'i bir telefonla koridora çıkarttırdı",
                     "Selim tuvaletteyken odaya girdi", "Yönetici koduyla oda boşken girdi"],
         dogru=1,
         destek=["kam_selim_koridor", "hts_selim", "ece_ifade", "burak_sms", "nermin_ifade",
                 "burak_ece_msg_acik", "saat_verisi"]),
    dict(soru="Oda sabah neden içeriden kilitliydi?",
         secenekler=["Katil çıkarken dışarıdan kilitledi", "Selim kapıyı kendisi içeriden kilitledi",
                     "Nermin gece kilitledi", "Kilit arızalıydı"],
         dogru=1,
         destek=["kilit_kaydi", "nermin_ifade", "kam_burak_wc", "selim_sesli_not"]),
    dict(soru="Katilin motifi neydi?",
         secenekler=["Mirastan pay almak", "Aldatma / aşk ilişkisi", "Zimmetinin savcılığa bildirilecek olması",
                     "Emekliye ayrılma öfkesi", "Kumar borcu"],
         dogru=2,
         destek=["orhan_eposta", "orhan_ifade", "selim_not_foto", "selim_burak_msg", "selim_sesli_not",
                 "muhasebe_eposta", "hoparlor_cay", "burak_banka"]),
]

IPUCLARI = [
    "Raporlarla başla: 'ara tur:belge rapor'. Otopsi neyin öldürdüğünü, toksikoloji zehrin "
    "nerede OLMADIĞINI söylüyor.",
    "Zehir mutfakta katılmadıysa, termos odaya girdikten sonra katıldı. Selim odadayken kimse bunu "
    "yapamazdı. Olay gecesini sırayla izle: 'zaman 13.03 21:00-22:30' ve özellikle Koridor-1 kayıtlarına bak.",
    "Selim neden koridora çıktı, onu kim aradı ve o kişiye bunu kim yaptırdı? Arama kayıtlarını ve "
    "ifadeleri karşılaştır. Sonra kimin yalan söylediğine bak.",
]

COZUM = """
NE OLDU?

9 Mart'ta Selim Aydın, Ege Lojistik'in 18 aylık ödeme dökümünü istedi. E-postanın
bilgi satırında Burak Tan vardı: Burak o gün oyunun bittiğini anladı. Aynı gece
"zimmet ceza kaç yıl" diye aradı; iki gün sonra "digoksin kaç tablet öldürür",
"digoksin çayda tadı belli olur mu", "nitril eldiven parmak izi bırakır mı".

12 Mart gecesi Selim avukatına yazdı: 4,2 milyon TL, iki paravan firma, ikisi de
Burak'ın eniştesinin. Pazartesi 10:00'da savcılığa gideceklerdi. "Soran olursa
vasiyet işi deriz." Ertesi akşam Leyla'yla tartışırken söylediği "vasiyet" de
buydu: bir kılıf.

13 Mart. Selim, avukatının uyarısına rağmen Burak'ı köşke çağırdı. Burak planını
kurdu: Selim'in çalışma odasında telefonun çekmediğini, Selim'in hep koridora
çıkıp konuştuğunu, ilaçlarının sağ çekmecede durduğunu, gece çayını 23:00'ten
sonra içtiğini biliyordu. Öğlen asistanı Ece'ye "21:50'de Selim Bey'i ara, uzun
tut" talimatını verdi.

21:05 — Nermin termosu odaya bıraktı. (Mutfak kamerası ve demlikteki negatif
sonuç: zehir mutfakta katılmadı. Nermin odaya girdiğinde Selim masasındaydı.)
21:38 — Burak odaya girdi.
21:49 — Burak, Ece'ye "Şimdi ara." yazdı.
21:52 – 21:58 — Selim telefonla koridora çıktı. Burak odada 6 dakika 40 saniye
yalnız kaldı. Tek nitril eldiveniyle çekmeceden 12 tablet aldı, pirinç kâğıt
ağırlığıyla sümenin kenarında ezdi, tozu termosa döktü, kâğıt ağırlığını sildi.
22:01 — "Çayın soğuyor, koyayım mı?" Selim: "Sonra içerim, gece çayım o."
Ege konuşuldu. Burak inkâr etti.
22:12 — Burak çıktı ve misafir WC'ye girip eldiveni çöpe, kâğıt havluların altına
bastırdı. 22:14 — Selim, her zamanki gibi kapısını içeriden kilitledi.
22:17 — Burak köşkten ayrıldı.

23:00'ten sonra Selim ıhlamurunu içti. 23:40'ta saati düzensiz ritim uyarısı
verdi. 23:47'de "her şey sarı sarı görünüyor" diye yazdı (digoksin zehirlenmesinin
klasik belirtisi: sarı görme). Leyla uyku ilacıyla uyuyordu, Nermin'in telefonu
sessizdeydi. 01:12'de kalbi durdu. Kapıyı içeriden kendisi kilitlediği için
"kilitli oda" kendiliğinden oluştu.

KIRMIZI RINGALAR
• Leyla: Tartışma ve "pişman olursun" sözü. Ama 22:36'dan sonra koridora hiç
  çıkmadı, telefonu 23:05'ten sabaha kadar hareketsizdi. Sırrı zehir değil,
  Dr. Kemal'le ilişkisi ve boşanma planıydı.
• Deniz: Borç, "babam ölse" şakası, "pişman olacaksın". Ama 20:52'de çıktı,
  01:52'ye kadar bardaydı; 02:14'te kapıyı denediğinde babası çoktan ölmüştü.
• Nermin: Termosu o hazırladı, emekliliğe kızgındı. Ama mutfak kamerası temiz,
  emeklilik aslında cömert bir ikramiyeydi, gece boyunca müştemilattan çıkmadı.
• Dr. Kemal: İlacı yazan oydu. Ama bütün gece hastanede, imzalı kayıtlarla.

KATİL: Burak Tan. YÖNTEM: Ezilmiş digoksin tabletleri, termostaki gece çayına.
FIRSAT: Ece'ye yaptırılan telefonla yaratılan 6 dakikalık yalnızlık.
MOTİF: Pazartesi savcılığa gidecek olan 4,2 milyonluk zimmet.
"""
