"""Kanıt arşivi: kimlik atama, arama, filtreleme ve zaman çizelgesi."""
import random
import re
from collections import Counter
from datetime import datetime, time, timedelta

from .metin import sade
from .modeller import TUR_TAKMA_ADLARI, TURLER, Kanit

_ID_DESENI = re.compile(r"^([fmskb])\s*-?\s*(\d{1,4})$")
_SAAT_ARALIGI = re.compile(r"^(\d{1,2})(?::(\d{2}))?-(\d{1,2})(?::(\d{2}))?$")
_TARIH = re.compile(r"^(\d{1,2})\.(\d{1,2})$")


def id_normallestir(metin: str) -> str | None:
    """'k42', 'K-042', 'k 42' -> 'K-042'."""
    m = _ID_DESENI.match(sade(metin.strip()))
    if not m:
        return None
    return f"{m.group(1).upper()}-{int(m.group(2)):03d}"


def saat_araligi_coz(metin: str) -> tuple[time, time] | None:
    m = _SAAT_ARALIGI.match(metin)
    if not m:
        return None
    s1, d1, s2, d2 = m.groups()
    try:
        return time(int(s1) % 24, int(d1 or 0)), time(int(s2) % 24, int(d2 or 0))
    except ValueError:
        return None


def tarih_coz(metin: str, yil: int) -> datetime | None:
    m = _TARIH.match(metin)
    if not m:
        return None
    try:
        return datetime(yil, int(m.group(2)), int(m.group(1)))
    except ValueError:
        return None


class Arsiv:
    def __init__(self, kanitlar: list[Kanit], tohum: int):
        # Kimlikler karıştırılmış sırayla verilir: kritik kanıtlar listenin başında toplanmaz.
        # Tohum sabit olduğu için kimlikler her oyunda aynı kalır.
        rng = random.Random(tohum)
        karisik = list(kanitlar)
        rng.shuffle(karisik)
        sayac = Counter()
        for k in karisik:
            sayac[k.tur] += 1
            k.id = f"{TURLER[k.tur][0]}-{sayac[k.tur]:03d}"
        self.kanitlar = sorted(karisik, key=lambda k: ("FMSKB".index(k.id[0]), k.id))
        self.idle = {k.id: k for k in self.kanitlar}
        self.anahtarla = {k.anahtar: k for k in self.kanitlar}

    # --- erişim -----------------------------------------------------------
    def gorunur(self, acik_paketler) -> list[Kanit]:
        return [k for k in self.kanitlar if k.paket is None or k.paket in acik_paketler]

    def bul(self, metin: str, acik_paketler) -> Kanit | None:
        kid = id_normallestir(metin)
        k = self.idle.get(kid) if kid else None
        if k and (k.paket is None or k.paket in acik_paketler):
            return k
        return None

    # --- arama ------------------------------------------------------------
    def ara(self, sorgu: str, acik_paketler, yil: int) -> tuple[list[Kanit], list[str]]:
        """Sorgu dili:
            kelime kelime       -> hepsini içerenler
            "tam ifade"         -> ifadeyi içerenler
            tur:kamera          -> türe göre
            kisi:burak          -> kişi etiketine göre
            gun:13 / gun:13.03  -> güne göre
            saat:21-23 / saat:21:30-22:15 (gece yarısını aşabilir)
        """
        uyarilar = []
        kelimeler, turler, kisiler = [], set(), []
        gun = None
        aralik = None
        for tirnakli, tek in re.findall(r'"([^"]+)"|(\S+)', sorgu):
            parca = tirnakli or tek
            anahtar, _, deger = parca.partition(":")
            anahtar_s = sade(anahtar)
            if deger and anahtar_s in ("tur", "tip"):
                t = TUR_TAKMA_ADLARI.get(sade(deger))
                if t:
                    turler.add(t)
                else:
                    uyarilar.append(f"Bilinmeyen tür: {deger}")
            elif deger and anahtar_s in ("kisi", "kim"):
                kisiler.append(sade(deger))
            elif deger and anahtar_s in ("gun", "tarih"):
                d = deger if "." in deger else f"{deger}.03"
                gun = tarih_coz(d, yil)
                if not gun:
                    uyarilar.append(f"Tarih anlaşılamadı: {deger}")
            elif deger and anahtar_s == "saat":
                aralik = saat_araligi_coz(deger)
                if not aralik:
                    uyarilar.append(f"Saat aralığı anlaşılamadı: {deger} (örnek: saat:21-23)")
            else:
                kelimeler.append(sade(parca))

        sonuc = []
        for k in self.gorunur(acik_paketler):
            if turler and k.tur not in turler:
                continue
            if kisiler and not all(any(ks in sade(p) for p in k.kisiler) for ks in kisiler):
                continue
            if gun and (not k.zaman or k.zaman.date() != gun.date()):
                continue
            if aralik and (not k.zaman or not _saatte(k.zaman.time(), *aralik)):
                continue
            if not all(k.eslesir(w) for w in kelimeler):
                continue
            sonuc.append(k)
        return sonuc, uyarilar

    def zaman_araligi(self, bas: datetime, bit: datetime, acik_paketler) -> list[Kanit]:
        return sorted(
            (k for k in self.gorunur(acik_paketler) if k.zaman and bas <= k.zaman <= bit),
            key=lambda k: (k.zaman, k.id),
        )


def _saatte(t: time, bas: time, bit: time) -> bool:
    if bas <= bit:
        return bas <= t <= bit
    return t >= bas or t <= bit  # gece yarısını aşan aralık


def gun_sonu(gun: datetime) -> datetime:
    return gun + timedelta(days=1) - timedelta(minutes=1)
