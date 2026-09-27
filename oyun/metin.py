"""Metin yardımcıları: Türkçe karakter katlama, renkler, satır sarma."""
import os
import shutil
import sys
import textwrap

if os.name == "nt":
    os.system("")  # Windows konsolunda ANSI renklerini etkinleştirir

RENK_ACIK = sys.stdout.isatty() and "NO_COLOR" not in os.environ

_KATLAMA = str.maketrans({
    "İ": "i", "I": "i", "ı": "i", "ş": "s", "Ş": "s", "ç": "c", "Ç": "c",
    "ğ": "g", "Ğ": "g", "ü": "u", "Ü": "u", "ö": "o", "Ö": "o",
    "â": "a", "Â": "a", "î": "i", "û": "u",
})


def sade(metin: str) -> str:
    """Aramada 'sehir' ile 'Şehir'in eşleşmesi için metni ASCII küçük harfe katlar."""
    return metin.translate(_KATLAMA).lower()


def _renk(kod):
    def uygula(s):
        return f"\033[{kod}m{s}\033[0m" if RENK_ACIK else str(s)
    return uygula


kalin = _renk("1")
soluk = _renk("2")
kirmizi = _renk("31")
yesil = _renk("32")
sari = _renk("33")
mavi = _renk("34")
mor = _renk("35")
camgobegi = _renk("36")


def renkli(kod, s):
    return _renk(kod)(s)


def genislik() -> int:
    return max(60, min(shutil.get_terminal_size((96, 24)).columns, 100)) - 2


def sar(metin: str, girinti: str = "  ") -> str:
    """Paragrafları terminal genişliğine göre sarar; boşluklu satır düzenini korur."""
    g = genislik()
    satirlar = []
    for satir in metin.splitlines():
        if not satir.strip():
            satirlar.append("")
            continue
        # Tablo/çizim satırlarını ve girintili satırları olduğu gibi bırak
        bas_bosluk = len(satir) - len(satir.lstrip(" "))
        if any(c in satir for c in "│┌└├─") or len(satir) <= g - len(girinti):
            satirlar.append(girinti + satir)
            continue
        satirlar.extend(textwrap.wrap(
            satir.strip(), width=g,
            initial_indent=girinti + " " * bas_bosluk,
            subsequent_indent=girinti + " " * bas_bosluk,
        ))
    return "\n".join(satirlar)


def cizgi(karakter="─") -> str:
    return soluk(karakter * genislik())


def baslik(metin: str) -> str:
    return "\n" + kalin(metin) + "\n" + cizgi()
