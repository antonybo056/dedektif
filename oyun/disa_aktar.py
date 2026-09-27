"""Web sürümü için veri paketi.

Python burada kanıtları işler: mesajları konuşma akışlarına, ses kayıtlarını
konuşmacı satırlarına, kamera kayıtlarını klip süresi + görüntüdeki figürlere,
fotoğrafları sahnelere ayırır. Tarayıcı yalnızca bu yapılandırılmış veriyi çizer.

Çözüme dair her şey (arama izniyle açılan kanıtlar, doğru cevaplar, çözüm metni)
"gizli" alanında kodlanmış olarak durur ki sayfa kaynağına bakan biri bir bakışta
katili okumasın.
"""
import base64
import json
import re

from . import gurultu
from . import vaka_kuzgun as vaka
from .arsiv import Arsiv
from .metin import sade
from .modeller import Kanit

FOTO_SAHNE = {
    "foto_genel": "olay_genel", "foto_termos": "termos", "foto_pencere": "pencere",
    "masa_toz": "toz", "foto_ilac_kutusu": "ilac", "selim_not_foto": "not",
    "foto_leyla_komodin": "komodin", "eldiven_foto": "eldiven", "foto_mutfak_eldiven": "mutfak_eldiven",
}

KONUM_SAHNE = [
    ("çalışma", "calisma"), ("kütüphane", "calisma"), ("salon", "salon"), ("mutfak", "mutfak"),
    ("kiler", "kiler"), ("koridor", "koridor"), ("wc", "wc"), ("banyo", "wc"), ("çamaşır", "wc"),
    ("yatak", "yatak"), ("deniz'in odası", "yatak"), ("müştemilat", "mustemilat"), ("garaj", "garaj"),
    ("havuz", "havuz"), ("bahçe", "bahce"), ("giriş", "giris"), ("ana kapı", "giris"),
    ("merdiven", "giris"), ("yemek", "yemek"),
]

# Kilit kamera kayıtlarında görüntüde gerçekten kimin göründüğü
KAMERA_FIGUR = {
    "kam_nermin_termos": [("kisi", "Nermin Kaya")],
    "kam_selim_koridor": [("kisi", "Selim Aydın")],
    "kam_deniz_cikis": [("kisi", "Deniz Aydın"), ("arac", "")],
    "kam_burak_gelis": [("arac", ""), ("kisi", "Burak Tan")],
    "kam_burak_cikis": [("kisi", "Burak Tan"), ("arac", "")],
    "kam_deniz_donus": [("arac", ""), ("kisi", "Deniz Aydın")],
}

PORTRE = {
    "maktul": dict(sac="kisa", sacRenk="#d5d3cf", ten="#d8b596", giysi="#2a2c31", yaka="#e8e4da"),
    "leyla": dict(sac="uzun", sacRenk="#3a271c", ten="#dfbb9e", giysi="#7b3a48"),
    "deniz": dict(sac="dalgali", sacRenk="#231d19", ten="#cda386", giysi="#33445c", sakal=True),
    "burak": dict(sac="kisa", sacRenk="#58585a", ten="#d4ae90", giysi="#3a424e", yaka="#dfe3e8",
                  kravat="#6b2430", gozluk=True),
    "nermin": dict(sac="topuz", sacRenk="#7a7470", ten="#d6b093", giysi="#56644a"),
    "kemal": dict(sac="seyrek", sacRenk="#8d8680", ten="#d9b49a", giysi="#e9eaec", yaka="#9fb4c8",
                  gozluk=True),
}

_MESAJ = re.compile(r"^\[(\d\d\.\d\d \d\d:\d\d)\] ([^:]+): (.*)$")
_KONUSMA = re.compile(r"^([A-ZÇĞİÖŞÜ?]{2,}|\?):\s*(.*)$")
_KLIP = re.compile(r"Kayıt (\d\d:\d\d:\d\d) – (\d\d:\d\d:\d\d)")
_OLAY = re.compile(r"^(\d\d:\d\d(?::\d\d)?)\s+(.*)$")


def _saniye(s: str) -> int:
    p = [int(x) for x in s.split(":")] + [0]
    return p[0] * 3600 + p[1] * 60 + p[2]


def _mesajlar(icerik):
    akis, notlar = [], []
    for satir in icerik.splitlines():
        m = _MESAJ.match(satir.strip())
        if m:
            akis.append({"zaman": m.group(1), "kimden": m.group(2), "metin": m.group(3)})
        elif satir.strip():
            notlar.append(satir.strip())
    return akis, notlar


def _konusma(icerik):
    satirlar, baslik = [], ""
    for satir in icerik.splitlines():
        s = satir.strip()
        if not s:
            continue
        if s.startswith("▶"):
            baslik = s.lstrip("▶ ").strip()
            continue
        m = _KONUSMA.match(s)
        if m:
            satirlar.append({"konusan": m.group(1), "metin": m.group(2)})
        elif s.startswith("[") and s.endswith("]"):
            satirlar.append({"konusan": "", "metin": s})
        elif satirlar:
            satirlar[-1]["metin"] += " " + s
    return baslik, satirlar


def _kamera(k: Kanit):
    m = _KLIP.search(k.icerik)
    klip = {"bas": _saniye(m.group(1)), "bit": _saniye(m.group(2))} if m else None
    olaylar = []
    for satir in k.icerik.splitlines()[1:]:
        s = satir.strip()
        om = _OLAY.match(s)
        if om:
            olaylar.append({"saat": om.group(1), "metin": om.group(2)})
        elif s and olaylar and satir.startswith(" "):
            olaylar[-1]["metin"] += " " + s
        elif s:
            olaylar.append({"saat": "", "metin": s})

    if k.anahtar in KAMERA_FIGUR:
        figurler = [{"tip": t, "ad": a} for t, a in KAMERA_FIGUR[k.anahtar]]
    else:
        t = sade(k.icerik)
        figurler = []
        if "kedi" in t:
            figurler.append({"tip": "kedi", "ad": ""})
        if "kus" in t and "kuaf" not in t:
            figurler.append({"tip": "kus", "ad": ""})
        if any(w in t for w in ("arac", "volvo", "bmw", "mini'si", "taksi", "kamyon")):
            figurler.append({"tip": "arac", "ad": ""})
        figurler += [{"tip": "kisi", "ad": ad} for ad in k.kisiler]
        if not any(f["tip"] == "kisi" for f in figurler) and any(
                w in t for w in ("kurye", "postaci", "sofor", "gorevli", "komsu", "teslim")):
            figurler.append({"tip": "kisi", "ad": "?"})
        if "ruzgar" in t:
            figurler.append({"tip": "dal", "ad": ""})
    return klip, olaylar, figurler


def _belge_tipi(k: Kanit):
    b = sade(k.baslik)
    if "ifade" in b:
        return "ifade"
    if "e-posta" in b:
        return "eposta"
    if any(w in b for w in ("otopsi", "toksikoloji", "dna", "rapor", "tutanag")):
        return "rapor"
    if any(w in b for w in ("fatura", "fis", "ekstre", "bilet", "rezervasyon", "cezasi", "adisyon")):
        return "fis"
    return "genel"


def _damga(k: Kanit):
    if k.paket:
        return "ARAMA İZNİ"
    ks = sade(k.kaynak)
    for anahtar, damga in (("adli tip", "ADLİ TIP"), ("kriminal", "KRİMİNAL LAB."),
                           ("cinayet", "İFADE"), ("olay yeri", "DELİL"), ("emniyet", "EMNİYET"),
                           ("operator", "HTS"), ("noter", "NOTER")):
        if anahtar in ks:
            return damga
    return ""


def _kanit_json(k: Kanit) -> dict:
    d = {
        "id": k.id, "tur": k.tur, "baslik": k.baslik, "icerik": k.icerik,
        "zaman": k.zaman.strftime("%Y-%m-%dT%H:%M") if k.zaman else None,
        "kisiler": list(k.kisiler), "kaynak": k.kaynak, "konum": k.konum,
    }
    if k.paket:
        d["paket"] = k.paket
    if k.tur == "mesaj":
        d["akis"], d["notlar"] = _mesajlar(k.icerik)
    elif k.tur == "ses":
        d["kayit"], d["satirlar"] = _konusma(k.icerik)
    elif k.tur == "kamera":
        d["klip"], d["olaylar"], d["figurler"] = _kamera(k)
    elif k.tur == "foto":
        if k.anahtar in FOTO_SAHNE:
            d["sahne"] = FOTO_SAHNE[k.anahtar]
        elif k.baslik.startswith("Telefon galerisi"):
            d["sahne"] = "galeri"
        else:
            konum = k.konum.lower()
            d["sahne"] = next((s for anahtar, s in KONUM_SAHNE if anahtar in konum), "genel")
        m = re.search(r"#(\d+)", k.baslik)
        if m:
            d["numara"] = int(m.group(1))
        if d["sahne"] == "not":
            d["elYazisi"] = [s.strip().strip('"') for s in k.icerik.splitlines()[2:] if s.strip()]
    elif k.tur == "belge":
        d["tip"] = _belge_tipi(k)
        d["damga"] = _damga(k)
    return d


def _kodla(veri) -> str:
    ham = json.dumps(veri, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return base64.b64encode(ham).decode("ascii")[::-1]


def _web_brifing() -> str:
    """Kaynaktaki sabit satır sonlarını kaldırır (paragraflar korunur); terminal komutunu web diline çevirir."""
    metin = re.sub(r"(?<!\n)\n(?!\n)", " ", vaka.BRIFING.strip())
    return metin.replace("Hazır olduğunda 'sucla' yaz.", "Hazır olduğunda Suçlama bölümüne geç.")


def veri_paketi() -> dict:
    kanitlar = [Kanit(**d) for d in vaka.KANITLAR] + [Kanit(**d) for d in gurultu.uret(vaka.TOHUM)]
    arsiv = Arsiv(kanitlar, vaka.TOHUM)
    id_ = lambda anahtar: arsiv.anahtarla[anahtar].id

    acik = [_kanit_json(k) for k in arsiv.kanitlar if not k.paket]
    paketler = {}
    for k in arsiv.kanitlar:
        if k.paket:
            paketler.setdefault(k.paket, []).append(_kanit_json(k))

    izinler = {}
    for anahtar, kural in vaka.IZINLER.items():
        if "red" in kural:
            izinler[anahtar] = {"red": kural["red"]}
        else:
            izinler[anahtar] = {"gerekce": [id_(a) for a in kural["gerekce"]], "esik": kural["esik"],
                                "kabul": kural["kabul"]}

    gizli = {
        "paketler": paketler,
        "izinler": izinler,
        "cevaplar": [{"dogru": s["dogru"], "destek": [id_(a) for a in s["destek"]]} for s in vaka.SORULAR],
        "ipuclari": vaka.IPUCLARI,
        "cozum": vaka.COZUM.strip(),
    }
    return {
        "kimlik": vaka.KIMLIK,
        "baslik": vaka.BASLIK,
        "brifing": _web_brifing(),
        "maktul": {"ad": "Selim Aydın", "yas": 62, "metin": vaka.MAKTUL, "portre": PORTRE["maktul"]},
        "supheliler": [dict(anahtar=a, portre=PORTRE[a], **s) for a, s in vaka.SUPHELILER.items()],
        "sorular": [{"soru": s["soru"], "secenekler": s["secenekler"]} for s in vaka.SORULAR],
        "izinHakki": vaka.IZIN_HAKKI,
        "olayGecesi": [t.strftime("%Y-%m-%dT%H:%M") for t in vaka.OLAY_GECESI],
        "kanitlar": acik,
        "gizli": _kodla(gizli),
    }
