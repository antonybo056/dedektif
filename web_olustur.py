"""Görsel (tarayıcı) sürümünü üretir.

    python web_olustur.py              -> web/kuzgun_kosku.html  (çift tıklayıp açılabilir)
    python web_olustur.py --govde X    -> yalnızca sayfa gövdesi (barındırma ortamları için)

Python vakayı ve yüzlerce kanıtı işler (oyun/disa_aktar.py), şablonun içine gömer;
ortaya sunucu gerektirmeyen tek bir HTML dosyası çıkar.
"""
import argparse
import json
from pathlib import Path

from oyun.disa_aktar import veri_paketi

KOK = Path(__file__).parent
SABLON = KOK / "web" / "sablon.html"
CIKTI = KOK / "web" / "kuzgun_kosku.html"


def govde_uret() -> str:
    veri = json.dumps(veri_paketi(), ensure_ascii=False, separators=(",", ":"))
    veri = veri.replace("</", "<\\/")  # </script> kaçışı
    return SABLON.read_text(encoding="utf-8").replace("__VERI__", veri)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--govde", type=Path, help="yalnızca sayfa gövdesini bu dosyaya yaz")
    args = ap.parse_args()
    govde = govde_uret()
    if args.govde:
        args.govde.write_text(govde, encoding="utf-8")
        print(f"Gövde yazıldı: {args.govde}  ({len(govde) // 1024} KB)")
        return
    tam = ('<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           "</head>\n<body>\n" + govde + "\n</body>\n</html>\n")
    CIKTI.write_text(tam, encoding="utf-8")
    print(f"Oluşturuldu: {CIKTI}  ({len(tam) // 1024} KB)")


if __name__ == "__main__":
    main()
