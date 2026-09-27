"""Gürültü kanıtları: gerçek bir soruşturma arşivini dolduran gündelik kayıtlar.

Tümü sabit bir tohumla üretilir, böylece kanıt kimlikleri her oyunda aynı kalır.
Olay gecesinin (13.03 akşamı – 14.03 sabahı) zaman çizelgesiyle çelişmemesi için
o saatlerde yalnızca dış kameralardan olaysız kayıtlar üretilir.
"""
import random
from datetime import datetime, timedelta

S, L, D, B, N, KM = "Selim Aydın", "Leyla Aydın", "Deniz Aydın", "Burak Tan", "Nermin Kaya", "Kemal Sarp"
E, O, H, Z, EM = "Ece Yıldız", "Orhan Demir", "Hakan Er", "Zeynep Kaya", "Emre Koç"

# Kilit kanıtlarda kullanılan olay yeri fotoğraf numaraları
KULLANILAN_FOTO_NO = {3, 4, 6, 9, 11, 14, 21, 27, 33}


def iyelik(ad: str) -> str:
    """'Selim Aydın' -> "Selim Aydın'ın", 'Nermin Kaya' -> "Nermin Kaya'nın"."""
    sesliler = "aıoueiöü"
    son_sesli = next((c for c in reversed(ad.lower()) if c in sesliler), "e")
    ek = {"a": "ın", "ı": "ın", "o": "un", "u": "un", "e": "in", "i": "in", "ö": "ün", "ü": "ün"}[son_sesli]
    return f"{ad}'{'n' if ad[-1].lower() in sesliler else ''}{ek}"


def _an(rng, gun_bas=2, gun_bit=12, saat_bas=8, saat_bit=22):
    gun = rng.randint(gun_bas, gun_bit)
    return datetime(2026, 3, gun, rng.randint(saat_bas, saat_bit), rng.randint(0, 59))


def _kanit(anahtar, tur, zaman, baslik, icerik, kisiler=(), kaynak="", konum=""):
    return dict(anahtar=anahtar, tur=tur, zaman=zaman, baslik=baslik, icerik=icerik,
                kisiler=tuple(kisiler), kaynak=kaynak, konum=konum, paket=None)


# ---------------------------------------------------------------- MESAJLAR
SOHBETLER = [
    (L, N, "Nermin Hanım, bu akşam misafir yok, sade bir şey yeterli.", "Tamam Leyla Hanım, zeytinyağlı yaparım."),
    (L, N, "Kuru temizlemeden lacivert paltomu alabilir misiniz?", "Öğleden sonra geçerim."),
    (L, N, "Çiçekçi 15:00'te gelecek, salona koysunlar lütfen.", "Tamam."),
    (L, N, "Bu akşam dışarıda yiyoruz, yemek yapmanıza gerek yok.", "Peki, iyi eğlenceler."),
    (L, N, "Misafir odasının perdeleri yıkanacak mıydı?", "Perşembe yıkıyorum."),
    (N, L, "Leyla Hanım, kombi servisi yarın 10:00'da gelecek.", "Tamam, ben evde olurum."),
    (N, S, "Selim Bey, zeytinyağı bitti, her zamankinden mi alayım?", "Evet, Ayvalık'tan olan."),
    (N, S, "Doğalgaz faturası geldi, masanıza bıraktım.", None),
    (S, N, "Nermin, yarın sabah kahvaltıyı erken hazırla, 07:00'de çıkacağım.", "Tamam Selim Bey."),
    (S, N, "Bu akşam Burak gelecek, iki kişilik bir şeyler hazırla.", "Tamam efendim."),
    (S, B, "Çeyrek raporunu Perşembe'ye yetiştirelim.", "Yetişir, merak etme."),
    (S, B, "Bankayla toplantı 11:00'e alındı.", "Tamam, orada olurum."),
    (B, S, "Yeni lojistik ihalesinin sunumunu mail attım.", "Akşam bakarım."),
    (B, S, "Vergi danışmanıyla konuştum, sorun yok.", "Güzel."),
    (S, B, "Pazartesi yönetim kurulu gündemini gönder.", "Gönderdim."),
    (B, E, "Yarınki Ankara uçuşunu iptal et.", "Ettim Burak Bey."),
    (B, E, "Sunumu PDF yapıp yönetim kuruluna gönder.", "Gönderildi."),
    (B, E, "Saat 14:00 toplantısını 15:00'e al.", "Aldım."),
    (E, B, "Burak Bey, İzmir'den aradılar, sizi arayacaklar.", "Tamam."),
    (E, B, "Eşiniz aradı, telefonunuza ulaşamamış.", "Tamam ararım."),
    (B, E, "Muhasebeden Şubat kapanışını iste.", "İstedim, yarın gelir."),
    (D, EM, "Maç akşam kaçta?", "21:45, bizde izleriz."),
    (D, EM, "Cumartesi Bodrum'a mı gidiyoruz sonunda?", "Bilmiyorum abi param yok."),
    (EM, D, "Dün akşam telefonun kapalıydı, iyi misin?", "Uyuyakalmışım."),
    (D, EM, "Yeni açılan yere gidelim mi Cuma?", "Olur."),
    (D, EM, "Tolga abi aradı mı seni?", "Aramadı."),
    (EM, D, "Abi 500 lira atabilir misin haftaya veririm", "Bende de yok ki."),
    (D, L, "Leyla abla arabamın anahtarı sende mi kaldı?", "Girişteki kaseye bıraktım."),
    (L, D, "Akşam yemeğe gelecek misin? Baban soruyor.", "Bilmiyorum."),
    (S, D, "Yarın 09:00'da ofiste ol.", "Tamam baba."),
    (S, D, "Toplantıya yine gelmedin.", None),
    (D, S, "Baba araba sigortası yenilenecekmiş.", "Ofise gönder faturasını."),
    (H, N, "Nermin abla gübre geldi, garaja koydum.", "Tamam Hakan."),
    (H, N, "Sulama sisteminin bir vanası arızalı, parça sipariş ettim.", "Selim Bey'e söylerim."),
    (H, N, "Yarın gelemiyorum, Perşembe telafi ederim.", "Tamam."),
    (N, H, "Hakan, gül bahçesine bu hafta bir bakar mısın?", "Cuma bakarım abla."),
    (Z, N, "Abla annemin ilaçlarını aldım.", "Allah razı olsun."),
    (Z, N, "Pazar bize gel, çocuklar seni özledi.", "İnşallah gelirim."),
    (N, Z, "Tansiyonum yine yükseldi.", "Doktora git abla, erteleme."),
    (Z, N, "Kızın doğum günü Salı, unutma.", "Unutmam."),
    (KM, S, "Selim Bey, kontrol randevunuz 24 Mart 10:30.", "Teşekkürler Kemal Bey."),
    (KM, S, "Tahlil sonuçlarınız normal, dozu aynı devam ediyoruz.", "Sağ olun."),
    (S, KM, "Son günlerde biraz yorgunum, normal mi?", "Yarın bir uğrayayım, bakarım."),
    (O, S, "Selim Bey, kira sözleşmesi taslağını ilettim.", "Gördüm, uygun."),
    (O, S, "Vakıf toplantısı Mart sonuna kaldı.", "Olur."),
    (S, L, "Akşam biraz geç kalacağım.", "Tamam."),
    (S, L, "Annenin doğum günü için çiçek gönderttim.", "Teşekkür ederim."),
    (L, S, "Galeriden Ayşe aradı, sergiye gelecek misin?", "Bu hafta çok yoğunum."),
    (L, S, "Kapadokya fotoğraflarını bastırdım, çok güzel olmuş.", "Salona asalım."),
    (L, S, "Nermin Hanım'ın tansiyonu yine yüksekmiş, bir doktora gitsin.", "Kemal Bey'e söyle."),
]

SERVIS_MESAJLARI = [
    ("KargoHızlı", "Kargonuz yola çıktı. Takip no: {n}"),
    ("KargoHızlı", "Kargonuz teslim edildi. Teslim alan: Nermin K."),
    ("Operatör", "Faturanız hazır: {t} TL. Son ödeme {g}.03."),
    ("Banka", "Kartınızla {t} TL harcama yapıldı."),
    ("Banka", "Tek kullanımlık şifreniz: {n}. Kimseyle paylaşmayın."),
    ("Eczane", "Reçeteli ilacınız hazırdır."),
    ("Otopark", "Aracınızın park süresi 30 dk içinde doluyor."),
    ("Kuaför", "Yarın 14:00 randevunuzu hatırlatırız."),
    ("Belediye", "Mahallenizde yarın 09:00–13:00 arası su kesintisi olacaktır."),
    ("Sigorta", "Poliçeniz {g}.04 tarihinde yenilenecektir."),
]


def _mesajlar(rng):
    sonuc = []
    for i, (kimden, kime, ilk, cevap) in enumerate(SOHBETLER):
        z = _an(rng)
        satirlar = [f"[{z:%d.%m %H:%M}] {kimden}: {ilk}"]
        if cevap:
            z2 = z + timedelta(minutes=rng.randint(1, 40))
            satirlar.append(f"[{z2:%d.%m %H:%M}] {kime}: {cevap}")
        sonuc.append(_kanit(f"g_msj_{i}", "mesaj", z, f"{kimden} → {kime}", "\n".join(satirlar),
                            [kimden, kime], kaynak=f"{iyelik(kimden)} telefonu"))
    alicilar = [S, L, D, N, B]
    for i in range(34):
        gonderen, sablon = rng.choice(SERVIS_MESAJLARI)
        alici = rng.choice(alicilar)
        z = _an(rng, saat_bas=9, saat_bit=20)
        metin = sablon.format(n=rng.randint(100000, 999999), t=f"{rng.randint(80, 4800)},{rng.randint(0, 99):02d}",
                              g=rng.randint(15, 28))
        sonuc.append(_kanit(f"g_srv_{i}", "mesaj", z, f"{gonderen} → {alici}",
                            f"[{z:%d.%m %H:%M}] {gonderen}: {metin}", [alici], kaynak=f"{iyelik(alici)} telefonu"))
    return sonuc


# ---------------------------------------------------------------- KAMERA
GUNDUZ_KAMERA = {
    "Ana kapı": [
        ("Kurye paket bıraktı, Nermin Kaya teslim aldı.", 10, 17, [N]),
        ("Leyla Aydın'ın beyaz Mini'si çıkış yaptı.", 9, 19, [L]),
        ("Leyla Aydın'ın aracı giriş yaptı.", 11, 21, [L]),
        ("Şoför, Selim Aydın'ın aracını kapı önüne getirdi; Selim Aydın bindi.", 7, 9, [S]),
        ("Selim Aydın'ın aracı giriş yaptı.", 18, 20, [S]),
        ("Deniz Aydın'ın siyah BMW'si çıkış yaptı.", 11, 22, [D]),
        ("Deniz Aydın'ın aracı giriş yaptı.", 13, 23, [D]),
        ("Market siparişi teslim edildi.", 10, 18, []),
        ("Postacı posta kutusuna zarf bıraktı.", 10, 14, []),
        ("Burak Tan'ın gri Volvo'su giriş yaptı; Burak Tan kendi kartıyla girdi. 45 dk sonra çıktı.", 18, 21, [B]),
        ("Dr. Kemal Sarp giriş yaptı (ev ziyareti), 35 dk sonra çıktı.", 17, 19, [KM]),
        ("Bahçıvan Hakan Er bisikletiyle giriş yaptı.", 8, 9, [H]),
    ],
    "Koridor-1": [
        ("Nermin Kaya çalışma odasını temizliyor, kapı açık.", 9, 11, [N]),
        ("Selim Aydın çalışma odasına giriyor.", 8, 22, [S]),
        ("Selim Aydın telefonla konuşarak odasından çıkıyor, koridor penceresinin önünde konuşuyor, "
         "birkaç dakika sonra odaya dönüyor.", 9, 22, [S]),
        ("Leyla Aydın yatak odaları kanadına geçiyor.", 9, 23, [L]),
        ("Deniz Aydın odasına gidiyor.", 12, 23, [D]),
        ("Nermin Kaya elinde termosla çalışma odasına giriyor, iki dakika sonra çıkıyor.", 20, 21, [N, S]),
        ("Hareket yok (periyodik kayıt).", 0, 23, []),
    ],
    "Mutfak": [
        ("Nermin Kaya yemek hazırlıyor.", 11, 19, [N]),
        ("Nermin Kaya bulaşık makinesini boşaltıyor.", 8, 10, [N]),
        ("Leyla Aydın kahve yapıyor.", 9, 16, [L]),
        ("Deniz Aydın buzdolabından bir şey alıp çıkıyor.", 12, 23, [D]),
        ("Nermin Kaya akşam ıhlamurunu demleyip termosa dolduruyor.", 20, 20, [N]),
    ],
    "Arka kapı": [
        ("Nermin Kaya müştemilattan ana binaya geçiyor.", 7, 7, [N]),
        ("Nermin Kaya müştemilata dönüyor.", 21, 21, [N]),
        ("Bahçıvan Hakan Er malzeme taşıyor.", 9, 16, [H]),
        ("Hareket yok (periyodik kayıt).", 0, 23, []),
    ],
    "Garaj": [
        ("Şoför Selim Aydın'ın aracını yıkıyor.", 10, 15, []),
        ("Deniz Aydın aracına biniyor.", 11, 22, [D]),
        ("Hareket yok (periyodik kayıt).", 0, 23, []),
    ],
    "Bahçe-1": [
        ("Bahçıvan Hakan Er çitleri buduyor.", 9, 16, [H]),
        ("Bir kedi çimenlerden geçiyor.", 0, 23, []),
        ("Hareket yok (periyodik kayıt).", 0, 23, []),
        ("Selim Aydın sabah yürüyüşünde.", 7, 7, [S]),
    ],
    "Bahçe-2": [
        ("Bahçıvan Hakan Er gül bahçesini suluyor.", 8, 17, [H]),
        ("Deniz Aydın telefonla konuşarak bahçede dolaşıyor.", 13, 22, [D]),
        ("Rüzgâr dalları sallıyor, sensör tetiklendi.", 0, 23, []),
    ],
    "Havuz": [
        ("Leyla Aydın havuz kenarında kitap okuyor.", 12, 17, [L]),
        ("Havuz bakım görevlisi filtreyi temizliyor.", 10, 13, []),
        ("Hareket yok (periyodik kayıt).", 0, 23, []),
    ],
    "Ön cephe": [
        ("Hareket yok (periyodik kayıt).", 0, 23, []),
        ("Bir köpek gezdiren komşu kapı önünden geçiyor.", 7, 21, []),
        ("Çöp kamyonu geçiyor.", 6, 7, []),
    ],
}

GECE_DIS_OLAYLAR = [
    "Hareket yok (periyodik kayıt).",
    "Hareket yok (periyodik kayıt).",
    "Bir kedi çimenlerden geçiyor.",
    "Rüzgâr dalları sallıyor, sensör tetiklendi.",
    "Bir gece kuşu kameranın önünden geçti.",
]


def _kameralar(rng):
    sonuc = []
    kameralar = list(GUNDUZ_KAMERA)
    for i in range(150):
        kamera = rng.choice(kameralar)
        olay, s_bas, s_bit, kisiler = rng.choice(GUNDUZ_KAMERA[kamera])
        z = _an(rng, 2, 12, s_bas, s_bit)
        z = z.replace(second=rng.randint(0, 59))
        bitis = z + timedelta(seconds=rng.randint(15, 240))
        sonuc.append(_kanit(f"g_kam_{i}", "kamera", z.replace(second=0), f"{kamera} kamerası",
                            f"▶ Kayıt {z:%H:%M:%S} – {bitis:%H:%M:%S}\n{olay}", kisiler,
                            kaynak="Köşk güvenlik sistemi", konum=kamera))
    # Olay gecesi: yalnızca bahçe/havuz kameralarından olaysız kayıtlar
    bas = datetime(2026, 3, 13, 19, 0)
    for i in range(26):
        z = bas + timedelta(minutes=rng.randint(0, 11 * 60 + 30), seconds=rng.randint(0, 59))
        kamera = rng.choice(["Bahçe-1", "Bahçe-2", "Havuz"])
        olay = rng.choice(GECE_DIS_OLAYLAR)
        bitis = z + timedelta(seconds=rng.randint(10, 60))
        sonuc.append(_kanit(f"g_kamg_{i}", "kamera", z.replace(second=0), f"{kamera} kamerası",
                            f"▶ Kayıt {z:%H:%M:%S} – {bitis:%H:%M:%S}\n{olay}", [],
                            kaynak="Köşk güvenlik sistemi", konum=kamera))
    return sonuc


# ---------------------------------------------------------------- FOTOĞRAFLAR
OLAY_YERI_FOTOLARI = [
    ("Salon, genel görünüm. Düzenli; koltuk üzerinde katlanmış bir şal, sehpada iki kahve fincanı.", "Salon"),
    ("Salon, şömine. Kül soğuk, son 24 saatte yakılmamış.", "Salon"),
    ("Kütüphane rafları. Kitaplar düzenli, eksik ya da devrilmiş kitap yok.", "Kütüphane"),
    ("Giriş holü. Anahtar kasesinde üç araç anahtarı.", "Giriş holü"),
    ("Giriş holü, portmanto. İki palto, bir şemsiye.", "Giriş holü"),
    ("Yemek odası. Masada iki kişilik akşam yemeğinden kalan örtü.", "Yemek odası"),
    ("Mutfak, genel görünüm. Ocak üstünde demlik; bulaşık sepetinde süzgeç ve iki tabak.", "Mutfak"),
    ("Mutfak, buzdolabı içi. Olağan gıdalar.", "Mutfak"),
    ("Kiler rafları. Kuru gıdalar, ıhlamur kavanozu (yarı dolu).", "Kiler"),
    ("Çalışma odası, kitaplık. Ciltli yıllık raporlar, aile fotoğrafları.", "Çalışma odası"),
    ("Çalışma odası, duvardaki yağlı boya tablo (Boğaz manzarası).", "Çalışma odası"),
    ("Çalışma odası, çöp kutusu. Buruşturulmuş toplantı notları, bir çikolata ambalajı.", "Çalışma odası"),
    ("Çalışma odası, masanın sol çekmecesi. Kalemler, kartvizitler, şarj kablosu.", "Çalışma odası"),
    ("Çalışma odası, duvar kasası. Kapalı; zorlama izi yok.", "Çalışma odası"),
    ("Çalışma odası, kapının iç yüzü ve akıllı kilidin döner topuzu.", "Çalışma odası"),
    ("Çalışma odası, halı. Leke ya da sürüklenme izi yok.", "Çalışma odası"),
    ("Misafir WC, lavabo. Sabunluk, katlanmış havlular.", "Misafir WC"),
    ("Koridor-1, pencere önü. Pencere pervazında bir saksı.", "Koridor-1"),
    ("Koridor-1, tavandaki güvenlik kamerası ve görüş açısı.", "Koridor-1"),
    ("Yatak odası kanadı, Deniz Aydın'ın odası. Dağınık; yerde kıyafetler, masada boş enerji içeceği kutuları.", "Deniz'in odası"),
    ("Deniz Aydın'ın odası, çalışma masası. Dizüstü bilgisayar, bahis sitesi reklamlı bir el ilanı.", "Deniz'in odası"),
    ("Yatak odası (Selim–Leyla), gardırop. Düzenli.", "Yatak odası"),
    ("Banyo dolabı. Ağrı kesici, vitamin, diş macunu. Reçeteli ilaç yok.", "Banyo"),
    ("Müştemilat, Nermin Kaya'nın odası. Sade, düzenli; komodinde tansiyon ilacı ve bir dua kitabı.", "Müştemilat"),
    ("Müştemilat, küçük mutfak. Çaydanlık soğuk.", "Müştemilat"),
    ("Garaj. Leyla Aydın'ın beyaz Mini'si ve Selim Aydın'ın siyah sedanı. Deniz Aydın'ın aracı yok.", "Garaj"),
    ("Arka bahçe kapısı. Kilitli; zorlama izi yok.", "Arka bahçe"),
    ("Havuz kenarı. Şezlonglar katlanmış.", "Havuz"),
    ("Ana kapı, dış görünüm. Kart okuyucu ve zil paneli.", "Ana kapı"),
    ("Çalışma odası penceresinin dışı, bahçe tarafı. Toprakta ayak izi yok.", "Bahçe"),
    ("Salon, bar dolabı. Açılmamış viski şişeleri, iki kadeh.", "Salon"),
    ("Giriş holü, çöp kutusu. Kargo kutuları, reklam broşürleri.", "Giriş holü"),
    ("Yemek odası, büfe. Gümüş takımlar eksiksiz.", "Yemek odası"),
    ("Merdiven sahanlığı. Aile portresi.", "Merdiven"),
    ("Çamaşır odası. Makine boş, kurutmada çarşaflar.", "Çamaşır odası"),
    ("Koridor-1, misafir WC kapısının dış yüzü.", "Koridor-1"),
]

GALERI_FOTOLARI = [
    (L, "Kapadokya gezisi, 2024. Selim ve Leyla balon önünde gülümsüyor."),
    (L, "Galeri açılışı. Leyla Aydın bir heykel önünde."),
    (L, "Köşkün bahçesi, bahar. Güller açmış."),
    (L, "Bir restoranda tatlı tabağı."),
    (D, "Bir gece kulübünde kalabalık grup; Deniz ortada."),
    (D, "Araba kaputunun üzerinde oturan Deniz."),
    (D, "Bir maç ekranının fotoğrafı, skor 2–1."),
    (D, "Yarım kalmış bir bahis kuponu ekran görüntüsü."),
    (N, "Nermin Kaya ve kız kardeşi Zeynep, bir düğünde."),
    (N, "Mutfakta kurabiye tepsisi."),
    (N, "Yeğeninin doğum günü pastası."),
    (S, "Holding'in 25. yıl kutlaması; Selim Aydın, Burak Tan ve yöneticiler kadeh kaldırıyor."),
    (S, "Boğaz'da tekne gezisi; Selim ve Deniz, yıllar önce."),
    (S, "Bir faturanın fotoğrafı (okunaksız)."),
    (B, "Burak Tan ve ailesi, bir tatil köyünde."),
]


def _fotolar(rng):
    sonuc = []
    numaralar = [n for n in range(1, 60) if n not in KULLANILAN_FOTO_NO]
    rng.shuffle(numaralar)
    for i, (aciklama, konum) in enumerate(OLAY_YERI_FOTOLARI):
        no = numaralar[i]
        z = datetime(2026, 3, 14, 7, 50) + timedelta(minutes=no * 4 + rng.randint(0, 3))
        sonuc.append(_kanit(f"g_foto_{i}", "foto", z, f"Olay yeri fotoğrafı #{no}", aciklama,
                            kaynak="Olay yeri inceleme ekibi", konum=konum))
    for i, (sahip, aciklama) in enumerate(GALERI_FOTOLARI):
        z = datetime(2026, 3, rng.randint(1, 12), rng.randint(9, 22), rng.randint(0, 59))
        sonuc.append(_kanit(f"g_gal_{i}", "foto", z, f"Telefon galerisi — {sahip}", aciklama, [sahip],
                            kaynak=f"{iyelik(sahip)} telefonu"))
    return sonuc


# ---------------------------------------------------------------- SES
HOPARLOR = [
    ("Salon", "Asistan, yarın hava nasıl?", "Yarın Sarıyer'de parçalı bulutlu, en yüksek 14 derece.", L),
    ("Salon", "Asistan, Sezen Aksu çal.", "Spotify'dan Sezen Aksu çalınıyor.", L),
    ("Mutfak", "Asistan, zamanlayıcı on beş dakika.", "On beş dakikalık zamanlayıcı başladı.", N),
    ("Mutfak", "Asistan, alışveriş listesine süt ekle.", "Süt listeye eklendi.", N),
    ("Mutfak", "Asistan, ıhlamur kaç dakika demlenir?", "Genellikle beş ila yedi dakika önerilir.", N),
    ("Çalışma odası", "Asistan, dolar kaç?", "Güncel kur bilgisi okunuyor.", S),
    ("Çalışma odası", "Asistan, yarın sabah altı buçukta uyandır.", "Alarm 06:30 için kuruldu.", S),
    ("Çalışma odası", "Asistan, klasik müzik çal.", "Chopin noktürnleri çalınıyor.", S),
    ("Salon", "Asistan, ışıkları kıs.", "Salon ışıkları yüzde otuza ayarlandı.", L),
    ("Salon", "Asistan, maç kaç kaç?", "Karşılaşma 1–1 devam ediyor.", D),
    ("Salon", "(anlaşılmayan konuşma, televizyon sesi)", "Üzgünüm, anlayamadım.", None),
]

SESLI_MESAJLAR = [
    (S, "Holding santrali: Selim Bey, yarınki banka toplantısı 11:00'e alınmıştır."),
    (L, "Galeriden Ayşe: Leyla'cım sergi için katalog provaları geldi, bir bakarsan sevinirim."),
    (L, "Diş kliniği: Randevunuzu hatırlatmak için aradık."),
    (D, "Emre: Abi neredesin, maç başladı, gel."),
    (D, "Bilinmeyen numara: Deniz Bey, kredi kartı borcunuz hakkında sizi arıyoruz."),
    (N, "Zeynep: Abla ara beni, annemle ilgili."),
    (N, "Kombi servisi: Yarın 10:00'da geleceğiz, evde olur musunuz?"),
    (S, "Av. Orhan Demir: Selim Bey, kira sözleşmesi hazır, uygun olduğunuzda imzalayalım."),
    (B, "Ece Yıldız: Burak Bey, İzmir ofisi sizi arıyor, dönüş yapabilir misiniz?"),
    (S, "Kardiyoloji polikliniği: Kontrol randevunuz 24 Mart 10:30 olarak ayarlanmıştır."),
    (L, "Kuaför: Yarınki randevunuz 14:00'te, hatırlatmak istedik."),
    (D, "Oto servis: Aracınızın bakımı tamamlandı."),
]


def _sesler(rng):
    sonuc = []
    for i in range(24):
        oda, komut, yanit, kisi = rng.choice(HOPARLOR)
        z = _an(rng, 2, 12, 8, 22)
        konusan = kisi.split()[0].upper() if kisi else "?"
        icerik = f"▶ Kayıt, {rng.randint(4, 12)} sn\n\n{konusan}: {komut}\nASİSTAN: {yanit}"
        sonuc.append(_kanit(f"g_hop_{i}", "ses", z, f"Akıllı hoparlör kaydı — {oda.lower()}", icerik,
                            [kisi] if kisi else [], kaynak="Akıllı hoparlör bulut kaydı", konum=oda))
    for i, (sahip, metin) in enumerate(SESLI_MESAJLAR):
        z = _an(rng, 2, 12, 9, 20)
        sonuc.append(_kanit(f"g_sesli_{i}", "ses", z, f"Sesli mesaj — {iyelik(sahip)} telefonu",
                            f"▶ Sesli mesaj, {rng.randint(8, 30)} sn\n\n{metin}", [sahip],
                            kaynak=f"{iyelik(sahip)} telefonu"))
    return sonuc


# ---------------------------------------------------------------- BELGELER
def _belgeler(rng):
    sonuc = []

    def ekle(baslik, icerik, z, kisiler=(), kaynak=""):
        sonuc.append(_kanit(f"g_blg_{len(sonuc)}", "belge", z, baslik, icerik, kisiler, kaynak=kaynak))

    for ad, kurum in [("Elektrik", "BEDAŞ"), ("Su", "İSKİ"), ("Doğalgaz", "İGDAŞ"), ("İnternet", "Operatör")]:
        z = _an(rng, 2, 9, 9, 17)
        ekle(f"{ad} faturası — Şubat 2026",
             f"{kurum}\nAbone: Selim Aydın — Kuzgun Köşkü\nDönem: Şubat 2026\n"
             f"Tutar: {rng.randint(900, 7800)},{rng.randint(0, 99):02d} TL\nSon ödeme: {rng.randint(15, 28)}.03.2026",
             z, [S], "Köşk evrak klasörü")

    for i in range(9):
        z = _an(rng, 2, 13, 9, 20)
        kalemler = rng.sample(["süt", "ekmek", "yumurta", "zeytin", "peynir", "domates", "ıhlamur",
                               "limon", "bal", "deterjan", "kâğıt havlu", "pirinç", "mercimek", "elma",
                               "kahve", "tereyağı", "maydanoz"], 5)
        ekle("Market fişi", "SARIYER GURME MARKET\n" + "\n".join(
            f"  {k:<14} {rng.randint(18, 240)},{rng.randint(0, 99):02d}" for k in kalemler)
             + f"\nToplam: {rng.randint(400, 1900)},{rng.randint(0, 99):02d} TL", z, [N], "Mutfak çekmecesi")

    tutanaklar = [
        ("Yönetim kurulu toplantı tutanağı", "Gündem: 2026 yatırım bütçesi, İzmir deposu kira yenilemesi, "
         "yeni lojistik ihalesi. Tüm kararlar oybirliğiyle alındı.", [S, B]),
        ("Aylık satış raporu — Şubat", "Toplam ciro bir önceki aya göre %4 arttı. Ege bölgesi hedefin "
         "%2 altında. Detaylı tablo ektedir.", [S, B]),
        ("İç yazışma — İzmir deposu kira sözleşmesi", "Kira artışı TÜFE oranında uygulanacak; "
         "sözleşme 3 yıl uzatılacak.", [S, O]),
        ("İnsan kaynakları duyurusu", "Holding genelinde yeni izin yönetim sistemine 1 Nisan itibarıyla "
         "geçilecektir.", []),
        ("Toplantı notu — Bankalar", "Kredi limitlerinin yenilenmesi için gerekli belgeler Mart sonuna "
         "kadar tamamlanacak. Sorumlu: Burak Tan.", [B]),
        ("Sunum özeti — Yeni lojistik ihalesi", "Üç teklif değerlendirildi. En uygun teklif teknik "
         "puanla birlikte ikinci sırada.", [B]),
        ("Yıllık bütçe taslağı 2026", "Genel giderlerde %6 azaltım hedefleniyor. Onay: Yönetim Kurulu.", [S, B]),
        ("Vakıf burs listesi", "2026 bahar dönemi için 42 öğrenciye burs verilecek.", [S]),
        ("Ofis tadilat teklifi", "Levent ofisi 4. kat toplantı salonu yenileme teklifi: 1.240.000 TL.", []),
        ("Bağımsız denetim ön raporu — 2025", "Önemli bir bulguya rastlanmamıştır. Grup şirketlerinin "
         "ayrıntılı incelemesi Nisan ayında yapılacaktır.", [B]),
    ]
    for baslik, icerik, kisiler in tutanaklar:
        ekle(baslik, icerik, _an(rng, 2, 11, 9, 18), kisiler, "Aydın Holding arşivi")

    kisisel = [
        ("Kredi kartı ekstresi — Leyla Aydın", "Butik alışverişleri, restoran, kuaför, galeri malzemeleri. "
         "Toplam: 64.120 TL.", [L]),
        ("Kredi kartı ekstresi — Deniz Aydın", "Gece kulüpleri, akaryakıt, online oyun siteleri. "
         "Limit aşımı uyarısı. Toplam: 118.400 TL.", [D]),
        ("Trafik cezası — Deniz Aydın", "Hız sınırı ihlali, Sahil Yolu, 142 km/s. 9.268 TL.", [D]),
        ("Otopark cezası — Deniz Aydın", "Hatalı park, Bebek. 1.100 TL.", [D]),
        ("Sigorta poliçesi yenileme", "Kuzgun Köşkü konut sigortası 15.04.2026 tarihinde yenilenecektir.", [S]),
        ("Site aidat bildirimi", "Mart 2026 aidatı: 12.500 TL.", [S]),
        ("Bahçe peyzaj teklifi", "Gül bahçesi yenileme ve damla sulama: 186.000 TL.", [H, S]),
        ("Havuz bakım raporu", "Klor ve pH değerleri normal. Filtre değiştirildi.", []),
        ("Kombi servis formu", "Yıllık bakım yapıldı, arıza yok. Teknisyen: M. Kara.", [N]),
        ("Veteriner faturası", "Kedi aşısı (bahçe kedisi 'Pamuk'). 850 TL.", [N]),
        ("Tapu fotokopisi — Kuzgun Köşkü", "Malik: Selim Aydın. Pafta ve parsel bilgileri.", [S]),
        ("Kuaför randevu kartı", "Leyla Aydın — 14.03 14:00.", [L]),
        ("Sinema bileti", "2 kişilik, 07.03 21:15.", [L]),
        ("Konser bileti", "Deniz Aydın — Harbiye, 20.06.", [D]),
        ("Özel ders faturası", "Nermin Kaya'nın yeğeni için matematik dersi, 4 saat.", [N, Z]),
        ("Kitap siparişi", "Selim Aydın — 'Osmanlı'da Ticaret Yolları', 'Stoacılar'.", [S]),
        ("Kulüp üyelik yenilemesi", "Selim Aydın — Tarabya Yat Kulübü, 2026.", [S]),
        ("Galeri kira sözleşmesi (eski)", "Leyla Aydın — Karaköy, 2018–2020.", [L]),
        ("Laboratuvar sonucu — Nermin Kaya", "Tansiyon takibi. Kolesterol hafif yüksek.", [N]),
        ("Kan tahlili — Selim Aydın (20.02.2026)", "Digoksin düzeyi: 1,6 ng/mL (tedavi aralığında). "
         "Potasyum ve böbrek değerleri normal.", [S, KM]),
        ("Diş kliniği faturası", "Leyla Aydın — dolgu, 3.200 TL.", [L]),
        ("Şoför mesai çizelgesi — Mart", "Selim Aydın'ın şoförü; 13.03 Cuma 18:30'da mesaiyi bitirmiş.", [S]),
        ("Hakan Er — puantaj", "Bahçıvan; 13.03 Cuma 08:00–16:30 çalıştı.", [H]),
        ("Kargo irsaliyesi", "Alıcı: Leyla Aydın — 2 koli, 'kırılabilir'.", [L]),
        ("Restoran rezervasyonu", "Selim Aydın — 2 kişi, 06.03 20:30, Arnavutköy.", [S, L]),
        ("Araç servis kaydı — Selim Aydın", "Periyodik bakım, 60.000 km.", [S]),
        ("Online sipariş özeti — Burak Tan", "Koşu ayakkabısı, kablosuz kulaklık.", [B]),
        ("Hastane randevu belgesi", "Selim Aydın — Kardiyoloji kontrol, 24.03.2026 10:30.", [S, KM]),
        ("Holding kartvizit listesi", "Yönetim ekibinin güncel iletişim bilgileri.", [S, B, E]),
        ("Giriş kartı yetki listesi — Kuzgun Köşkü", "Kartla giriş yetkisi: Selim Aydın, Leyla Aydın, "
         "Deniz Aydın, Nermin Kaya, Burak Tan, Hakan Er (yalnızca bahçe kapısı).", [S, L, D, N, B, H]),
    ]
    for baslik, icerik, kisiler in kisisel:
        ekle(baslik, icerik, _an(rng, 2, 12, 9, 19), kisiler, "Köşk evrak klasörü")

    for i in range(8):
        z = datetime(2026, 3, 14, rng.randint(8, 18), rng.randint(0, 59))
        tip = rng.choice([
            ("Delil teslim tutanağı", "Olay yerinden toplanan delillerin laboratuvara teslimi. Mühürler sağlam."),
            ("Olay yeri krokisi (taslak)", "Çalışma odası ölçüleri, mobilya yerleşimi, cesedin konumu."),
            ("Tutanak — köşk çevresinde komşu görüşmesi", "Komşular gece olağandışı bir ses ya da araç "
             "duymadıklarını beyan etti."),
            ("Tutanak — ambulans ekibi", "07:25'te ulaşıldı. Ölüm, ekip gelmeden önce gerçekleşmiş."),
            ("Tutanak — delil zinciri", "Termos, fincan ve ilaç şişesi ayrı ayrı mühürlendi."),
        ])
        ekle(tip[0], tip[1], z, [], "Sarıyer Emniyet")
    return sonuc


def uret(tohum: int) -> list[dict]:
    rng = random.Random(tohum * 7 + 1)
    return _mesajlar(rng) + _kameralar(rng) + _fotolar(rng) + _sesler(rng) + _belgeler(rng)
