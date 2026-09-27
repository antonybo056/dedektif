# Dedektif — Kuzgun Köşkü

Terminalde oynanan bir soruşturma oyunu. Önünde yüzlerce **fotoğraf, mesaj, ses kaydı,
kamera görüntüsü ve belge** var. Çoğu gündelik gürültü, bazıları her şeyi değiştiriyor.

**Görevin:** Suçun nasıl gerçekleştiğini bulmak. Kim, nasıl, ne zaman, neden, kanıtıyla.

## Çalıştırma

```
python main.py
```

Python 3.10+ yeterli, dış kütüphane gerekmiyor. İlerleme `kayit.json` dosyasına otomatik kaydedilir.

## Görsel sürüm (tarayıcı)

```
python web_olustur.py
```

`web/kuzgun_kosku.html` oluşur; çift tıklayıp tarayıcıda aç. İnternet yalnızca yazı tipleri için
gerekir, oyun sunucusuz çalışır ve ilerlemeyi tarayıcıya kaydeder. İçinde:

- **Arşiv:** Kanıtlar küçük resimleriyle ızgarada; tür, gün, kişi filtresi ve aynı arama dili
- **Kanıt görüntüleyici:** Çizilmiş olay yeri fotoğrafları (delil işaretçisi ve cetvelle),
  oynatılabilir CCTV kayıtları, tarayıcının sesiyle okunan ses kayıtları, telefon ekranında mesajlar,
  kâğıt üzerinde belgeler
- **Zaman şeridi:** Olay gecesi, konumlara göre ayrı şeritlerde
- **Kroki:** Tıklanabilir oda ve kameralar, olay gecesinde gezinmek için saat kaydırıcısı
- **Pano:** Sürüklenebilen kanıt kartları, kırmızı ip, yapışkan notlar
- **Suçlama:** 8 soru, puan, rütbe ve çözüm raporu

Python tarafı (`oyun/disa_aktar.py`) kanıtları işler: mesajları konuşma akışlarına, ses kayıtlarını
konuşmacı satırlarına, kamera kayıtlarını klip süresi ve görüntüdeki figürlere ayırır.
Arayüz `web/sablon.html` içinde. Çözüm verisi sayfa kaynağında kodlanmış durur.

## Terminal sürümü: nasıl oynanır

| Komut | Ne yapar |
|---|---|
| `vaka`, `plan`, `supheliler` | Brifing, köşk krokisi, şüpheliler |
| `liste [tür] [sayfa]` | Arşivi gez (`liste kamera 3`, `liste yeni`) |
| `incele K-042` ya da sadece `K-042` | Kanıtı aç |
| `ara <sorgu>` | `ara termos`, `ara "gece çayı"`, `ara tur:kamera gun:13 saat:21-23`, `ara kisi:burak` |
| `zaman [GG.AA] [SS:DD-SS:DD]` | Kronolojik görünüm; parametresiz hâli olay gecesini gösterir |
| `isaretle <ID>`, `zaman isaretli` | Önemli kanıtları işaretle, kendi zaman çizelgeni kur |
| `not <metin>`, `notlar` | Dedektif defteri |
| `izin <şüpheli>` | Savcıdan telefon, hesap ya da DNA izni iste (en fazla 2 hak; önce gerekçe bulmalısın) |
| `ipucu` | Komiserden ipucu al (-5 puan) |
| `sucla` | 8 soruluk suçlama: doğru cevap 10 puan, incelediğin destekleyici kanıt +5 puan |
| `cozum` | Vaka kapandıktan sonra hikâyenin tamamı |

## Yapı

```
main.py              giriş noktası
oyun/
  oyun.py            komut döngüsü, izin, ipucu, suçlama ve puanlama
  arsiv.py           kanıt arşivi: kimlik atama, arama dili, zaman aralığı
  modeller.py        Kanit veri sınıfı ve kanıt türleri
  durum.py           oyuncu ilerlemesi (JSON kaydı)
  vaka_kuzgun.py     vakanın kendisi: hikâye, şüpheliler, kilit kanıtlar, sorular, çözüm
  gurultu.py         arşivi dolduran yüzlerce gündelik kaydı sabit tohumla üretir
  metin.py           Türkçe karakter katlama (ş→s ...), renkler, satır sarma
```

Yeni vaka yazmak için `vaka_kuzgun.py` ile aynı alanları (`KANITLAR`, `SORULAR`, `IZINLER`,
`COZUM` …) içeren bir modül oluşturup `oyun.py` içindeki içe aktarmayı değiştirmen yeterli.
Gürültü kanıtları, olay gecesinin zaman çizelgesiyle çelişmeyecek şekilde üretilir.
Olay saatlerinde yalnızca dış kameralardan olaysız kayıtlar gelir.

> Spoiler uyarısı: `vaka_kuzgun.py` dosyasını açmak, dosyadaki katilin adını okumak demek.
