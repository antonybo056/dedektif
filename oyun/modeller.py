"""Kanıt veri modeli."""
from dataclasses import dataclass, field
from datetime import datetime

from .metin import renkli, sade

# tür anahtarı -> (ID öneki, etiket, ANSI renk kodu)
TURLER = {
    "foto": ("F", "FOTO", "35"),
    "mesaj": ("M", "MESAJ", "36"),
    "ses": ("S", "SES", "33"),
    "kamera": ("K", "KAMERA", "34"),
    "belge": ("B", "BELGE", "32"),
}

TUR_TAKMA_ADLARI = {
    "foto": "foto", "fotograf": "foto", "resim": "foto", "f": "foto",
    "mesaj": "mesaj", "mesajlar": "mesaj", "sms": "mesaj", "m": "mesaj",
    "ses": "ses", "ses kaydi": "ses", "kayit": "ses", "s": "ses",
    "kamera": "kamera", "video": "kamera", "goruntu": "kamera", "k": "kamera",
    "belge": "belge", "dokuman": "belge", "rapor": "belge", "b": "belge",
}


@dataclass
class Kanit:
    anahtar: str                  # kalıcı iç anahtar (kayıt dosyası bunu kullanır)
    tur: str                      # foto | mesaj | ses | kamera | belge
    baslik: str
    icerik: str
    zaman: datetime | None = None
    kisiler: tuple = ()
    kaynak: str = ""
    konum: str = ""
    paket: str | None = None      # arama izniyle açılan kanıtlar için şüpheli anahtarı
    id: str = ""                  # oyuncunun gördüğü kimlik (ör. K-042)
    _arama: str = field(default="", repr=False)

    def __post_init__(self):
        parcalar = [self.baslik, self.icerik, self.kaynak, self.konum, " ".join(self.kisiler)]
        self._arama = sade(" ".join(parcalar))

    @property
    def etiket(self) -> str:
        _, ad, kod = TURLER[self.tur]
        return renkli(kod, f"[{ad}]")

    @property
    def zaman_kisa(self) -> str:
        return self.zaman.strftime("%d.%m %H:%M") if self.zaman else "--.-- --:--"

    def eslesir(self, kelime: str) -> bool:
        return kelime in self._arama
