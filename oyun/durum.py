"""Oyuncunun ilerlemesi: incelenen kanıtlar, işaretler, notlar, izinler. JSON'a kaydedilir."""
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class Durum:
    vaka: str
    gorulen: list[str] = field(default_factory=list)      # kanıt anahtarları
    isaretli: list[str] = field(default_factory=list)
    notlar: list[dict] = field(default_factory=list)      # {"zaman": ..., "metin": ...}
    izinler: list[str] = field(default_factory=list)      # açılan şüpheli paketleri
    ipucu: int = 0
    bitti: bool = False
    sonuc: dict | None = None

    def gordu(self, anahtar: str) -> bool:
        return anahtar in self._gorulen_kume

    def gor(self, anahtar: str):
        if anahtar not in self._gorulen_kume:
            self.gorulen.append(anahtar)
            self._gorulen_kume.add(anahtar)

    def __post_init__(self):
        self._gorulen_kume = set(self.gorulen)

    def not_ekle(self, metin: str):
        self.notlar.append({"zaman": datetime.now().strftime("%d.%m %H:%M"), "metin": metin})

    # --- kalıcılık ---------------------------------------------------------
    def kaydet(self, yol: Path):
        veri = asdict(self)
        veri.pop("_gorulen_kume", None)
        gecici = yol.with_suffix(".tmp")
        gecici.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
        gecici.replace(yol)

    @classmethod
    def yukle(cls, yol: Path, vaka: str) -> "Durum":
        if yol.exists():
            try:
                veri = json.loads(yol.read_text(encoding="utf-8"))
                if veri.get("vaka") == vaka:
                    return cls(**veri)
            except (json.JSONDecodeError, TypeError):
                pass
        return cls(vaka=vaka)
