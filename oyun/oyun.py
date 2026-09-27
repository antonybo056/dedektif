"""Komut döngüsü ve oyun kuralları."""
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

from . import gurultu
from . import vaka_kuzgun as vaka
from .arsiv import Arsiv, gun_sonu, id_normallestir, saat_araligi_coz, tarih_coz
from .durum import Durum
from .metin import (baslik, camgobegi, cizgi, kalin, kirmizi, mavi, sade, sar, sari,
                    soluk, yesil)
from .modeller import TUR_TAKMA_ADLARI, TURLER, Kanit

SAYFA = 25
AZAMI_SONUC = 80

PLAN = r"""
                    KUZGUN KÖŞKÜ — ZEMİN KAT

  ┌────────────────┬────────────┬───────────────────┐
  │ ÇALIŞMA ODASI  │ MİSAFİR WC │ YATAK ODALARI     │
  │ akıllı kilit   │            │ (Leyla, Deniz)    │
  │ kamera yok     │ kamera yok │                   │
  ├───── ▯ ────────┴──── ▯ ─────┴──────── ▯ ────────┤
  ◄ pencere          KORİDOR-1             ◉ kamera │
  ├──────────────────┬──────── ▯ ───────┬───────────┤
  │ SALON            │  GİRİŞ HOLÜ      │  MUTFAK   │
  │                  │                  │  ◉ kamera │
  └──────────────────┴──── ▯ ───────────┴──── ▯ ────┘
                        ◉ ANA KAPI          ◉ ARKA KAPI
                                                 │
   BAHÇE:  ◉ Bahçe-1  ◉ Bahçe-2  ◉ Havuz          │
           ◉ Garaj    ◉ Ön cephe                 ▼
                              MÜŞTEMİLAT (Nermin Kaya'nın evi)

   • Koridor-1 kamerası çalışma odası kapısını, misafir WC kapısını ve
     yatak odaları kanadına geçişi kesintisiz görür.
   • Çalışma odasında cep telefonu çekmez.
"""

YARDIM = f"""
{kalin('İNCELEME')}
  vaka                     Brifingi yeniden oku
  plan                     Köşkün krokisi ve kamera yerleri
  supheliler               Şüpheli listesi       supheli <ad>   Tek şüphelinin profili
  liste [tür] [sayfa]      Arşivi listele        tür: foto, mesaj, ses, kamera, belge
  liste yeni | isaretli    Görmediğin / işaretlediğin kanıtlar
  incele <ID> [ID ...]     Kanıtı aç (kısaca yalnızca ID yazmak da olur: K-042)
  ara <sorgu>              Arşivde ara. Örnekler:
                             ara burak eldiven
                             ara "gece çayı"
                             ara tur:kamera gun:13 saat:21-23
                             ara kisi:nermin tur:mesaj
  zaman [GG.AA] [SS:DD-SS:DD]  Kronolojik görünüm (parametresiz: olay gecesi)
  zaman isaretli           İşaretlediğin kanıtlarla kendi zaman çizelgen

{kalin('DEFTER')}
  isaretle <ID> [ID ...]   Kanıtı işaretle        kaldir <ID>   İşareti kaldır
  not <metin>              Deftere not yaz        notlar        Notları göster
  durum                    İlerleme özeti

{kalin('SORUŞTURMA')}
  izin <şüpheli>           Savcıdan telefon/hesap/DNA için arama izni iste
                           (en fazla {vaka.IZIN_HAKKI} kez; gerekçe kanıtlarını önceden incelemiş olmalısın)
  ipucu                    Komiserden ipucu al (her biri -5 puan)
  sucla                    Suçlamayı yap ve vakayı kapat
  cozum                    (Vaka kapandıktan sonra) tüm hikâye

{kalin('DİĞER')}
  temizle   ekranı temizle      yeni   baştan başla      cikis   kaydet ve çık
  İlerleme her komuttan sonra otomatik kaydedilir.
"""


class Oyun:
    def __init__(self, kayit_yolu: Path):
        kanitlar = [Kanit(**d) for d in vaka.KANITLAR] + [Kanit(**d) for d in gurultu.uret(vaka.TOHUM)]
        self.arsiv = Arsiv(kanitlar, vaka.TOHUM)
        self.kayit_yolu = kayit_yolu
        self.durum = Durum.yukle(kayit_yolu, vaka.KIMLIK)
        self.komutlar = {
            "yardim": self.k_yardim, "help": self.k_yardim, "?": self.k_yardim, "komutlar": self.k_yardim,
            "vaka": self.k_vaka, "brifing": self.k_vaka,
            "plan": self.k_plan, "kroki": self.k_plan, "harita": self.k_plan,
            "supheliler": self.k_supheliler, "supheli": self.k_supheli, "kisi": self.k_supheli,
            "liste": self.k_liste, "ls": self.k_liste, "arsiv": self.k_liste,
            "incele": self.k_incele, "oku": self.k_incele, "ac": self.k_incele, "bak": self.k_incele,
            "ara": self.k_ara, "bul": self.k_ara,
            "zaman": self.k_zaman, "kronoloji": self.k_zaman,
            "isaretle": self.k_isaretle, "pin": self.k_isaretle,
            "kaldir": self.k_kaldir,
            "isaretler": lambda a: self.k_liste("isaretli"),
            "not": self.k_not, "notlar": self.k_notlar,
            "durum": self.k_durum,
            "izin": self.k_izin,
            "ipucu": self.k_ipucu,
            "sucla": self.k_sucla, "suclama": self.k_sucla,
            "cozum": self.k_cozum,
            "yeni": self.k_yeni,
            "temizle": self.k_temizle, "cls": self.k_temizle, "clear": self.k_temizle,
        }

    # ------------------------------------------------------------ yardımcılar
    @property
    def acik(self):
        return set(self.durum.izinler)

    def gorunur(self):
        return self.arsiv.gorunur(self.acik)

    def satir(self, k: Kanit, zaman_once=False) -> str:
        isaret = sari("★") if k.anahtar in self.durum.isaretli else " "
        yeni = not self.durum.gordu(k.anahtar)
        kid = kalin(k.id) if yeni else soluk(k.id)
        bas = soluk(k.baslik) if not yeni else k.baslik
        if zaman_once:
            return f" {isaret} {camgobegi(k.zaman_kisa)}  {kid}  {k.etiket:<8} {bas}"
        return f" {isaret} {kid}  {soluk(k.zaman_kisa)}  {k.etiket:<8} {bas}"

    def listele(self, kanitlar, zaman_once=False, sinir=AZAMI_SONUC):
        for k in kanitlar[:sinir]:
            print(self.satir(k, zaman_once))
        if len(kanitlar) > sinir:
            print(soluk(f"   … ve {len(kanitlar) - sinir} kanıt daha. Aramayı daraltmayı dene."))

    def kanit_coz(self, metin: str) -> Kanit | None:
        k = self.arsiv.bul(metin, self.acik)
        if not k:
            print(kirmizi(f"  '{metin}' diye bir kanıt yok. Kimlikler F-001, M-012, K-104 gibi yazılır."))
        return k

    def kaydet(self):
        try:
            self.durum.kaydet(self.kayit_yolu)
        except OSError as e:
            print(kirmizi(f"  Kayıt yapılamadı: {e}"))

    # ------------------------------------------------------------ döngü
    def calistir(self):
        self.acilis()
        while True:
            try:
                satir = input(f"\n{mavi('dedektif')}> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not satir:
                continue
            ilk, _, arguman = satir.partition(" ")
            komut = sade(ilk)
            if komut in ("cikis", "q", "quit", "exit"):
                break
            if id_normallestir(ilk) or re.fullmatch(r"[fmskb]-?\s+\d{1,4}.*", sade(satir)):
                self.k_incele(satir)
            elif komut in self.komutlar:
                self.komutlar[komut](arguman.strip())
            else:
                print(kirmizi(f"  Anlaşılmadı: '{ilk}'. Komutlar için 'yardim' yaz."))
            self.kaydet()
        self.kaydet()
        print(soluk("  İlerleme kaydedildi. Dosya seni bekliyor, dedektif."))

    def acilis(self):
        print(kalin(f"\n  ═══  D E D E K T İ F  ═══   Vaka: {vaka.BASLIK}"))
        if self.durum.gorulen or self.durum.bitti:
            print(soluk(f"  Kayıtlı ilerleme yüklendi — {len(self.durum.gorulen)} kanıt incelenmiş."))
            print("  'durum' ile özet, 'vaka' ile brifing, 'yardim' ile komutlar.")
        else:
            self.k_vaka("")
            print(f"\n  İlk kez mi? {kalin('yardim')} yaz ya da doğrudan {kalin('liste belge')} ile başla.")

    # ------------------------------------------------------------ komutlar
    def k_yardim(self, _):
        print(YARDIM)

    def k_vaka(self, _):
        print(baslik(f"VAKA DOSYASI — {vaka.BASLIK}"))
        print(sar(vaka.BRIFING.strip()))
        sayim = {t: 0 for t in TURLER}
        for k in self.gorunur():
            sayim[k.tur] += 1
        ozet = ", ".join(f"{n} {TURLER[t][1].lower()}" for t, n in sayim.items())
        print(f"\n  Arşivde {kalin(str(sum(sayim.values())))} kanıt var: {ozet}.")

    def k_plan(self, _):
        print(PLAN)

    def k_supheliler(self, _):
        print(baslik("MAKTUL"))
        print(sar(vaka.MAKTUL))
        print(baslik("ŞÜPHELİLER"))
        for anahtar, s in vaka.SUPHELILER.items():
            print(f"  {kalin(s['ad'])} ({s['yas']}) — {s['rol']}   {soluk('[supheli ' + anahtar + ']')}")

    def supheli_bul(self, metin: str):
        m = sade(metin)
        for anahtar, s in vaka.SUPHELILER.items():
            if m and (anahtar.startswith(m) or any(p.startswith(m) for p in sade(s["ad"]).split())):
                return anahtar, s
        return None, None

    def k_supheli(self, arguman):
        anahtar, s = self.supheli_bul(arguman)
        if not s:
            print(kirmizi("  Kim? Örnek: supheli burak"))
            return
        print(baslik(f"{s['ad']} ({s['yas']}) — {s['rol']}"))
        print(sar(s["profil"]))
        ilgili = [k for k in self.gorunur() if any(sade(s["ad"]).split()[-1] in sade(p) for p in k.kisiler)]
        gorulen = sum(self.durum.gordu(k.anahtar) for k in ilgili)
        print(f"\n  Arşivde bu kişiyle etiketli {len(ilgili)} kanıt var ({gorulen} tanesini inceledin).")
        print(soluk(f"  Listelemek için: ara kisi:{anahtar}"))
        if anahtar in self.durum.izinler:
            print(yesil("  Bu kişi için arama izni alındı."))

    def k_liste(self, arguman):
        parcalar = sade(arguman).split()
        sayfa = 1
        tur = None
        ozel = None
        for p in parcalar:
            if p.isdigit():
                sayfa = max(1, int(p))
            elif p in TUR_TAKMA_ADLARI:
                tur = TUR_TAKMA_ADLARI[p]
            elif p in ("yeni", "gorulmemis"):
                ozel = "yeni"
            elif p in ("isaretli", "isaretler", "pin"):
                ozel = "isaretli"
            elif p in ("gorulen", "incelenen"):
                ozel = "gorulen"
            else:
                print(kirmizi(f"  '{p}' anlaşılmadı. Örnek: liste kamera 2"))
                return
        kanitlar = self.gorunur()
        if tur:
            kanitlar = [k for k in kanitlar if k.tur == tur]
        if ozel == "yeni":
            kanitlar = [k for k in kanitlar if not self.durum.gordu(k.anahtar)]
        elif ozel == "gorulen":
            kanitlar = [k for k in kanitlar if self.durum.gordu(k.anahtar)]
        elif ozel == "isaretli":
            sira = {a: i for i, a in enumerate(self.durum.isaretli)}
            kanitlar = sorted((k for k in kanitlar if k.anahtar in sira), key=lambda k: sira[k.anahtar])
            if not kanitlar:
                print("  Henüz işaretlediğin kanıt yok. 'isaretle K-042' gibi.")
                return
        toplam_sayfa = max(1, -(-len(kanitlar) // SAYFA))
        sayfa = min(sayfa, toplam_sayfa)
        etiket = TURLER[tur][1] if tur else "TÜM ARŞİV"
        if ozel:
            etiket += f" · {ozel}"
        print(baslik(f"{etiket} — {len(kanitlar)} kanıt — sayfa {sayfa}/{toplam_sayfa}"))
        self.listele(kanitlar[(sayfa - 1) * SAYFA: sayfa * SAYFA])
        if sayfa < toplam_sayfa:
            devam = " ".join([p for p in arguman.split() if not p.isdigit()] + [str(sayfa + 1)])
            print(soluk(f"\n  Sonraki sayfa: liste {devam}"))

    def k_incele(self, arguman):
        kimlikler = arguman.replace(",", " ").split()
        if not kimlikler:
            print(kirmizi("  Hangi kanıt? Örnek: incele B-012"))
            return
        # "k 42" gibi ayrık yazımları birleştir
        birlesik, i = [], 0
        while i < len(kimlikler):
            if i + 1 < len(kimlikler) and re.fullmatch(r"[fmskbFMSKB]-?", kimlikler[i]) and kimlikler[i + 1].isdigit():
                birlesik.append(kimlikler[i] + kimlikler[i + 1])
                i += 2
            else:
                birlesik.append(kimlikler[i])
                i += 1
        for kid in birlesik:
            k = self.kanit_coz(kid)
            if k:
                self.goster(k)

    def goster(self, k: Kanit):
        ilk = not self.durum.gordu(k.anahtar)
        self.durum.gor(k.anahtar)
        isaret = sari(" ★ işaretli") if k.anahtar in self.durum.isaretli else ""
        print(baslik(f"{k.id}  {k.etiket}  {k.baslik}{isaret}"))
        bilgiler = []
        if k.zaman:
            bilgiler.append(f"Zaman: {k.zaman:%d.%m.%Y %H:%M}")
        if k.konum:
            bilgiler.append(f"Konum: {k.konum}")
        if k.kaynak:
            bilgiler.append(f"Kaynak: {k.kaynak}")
        if bilgiler:
            print(soluk("  " + "   ·   ".join(bilgiler)))
        if k.kisiler:
            print(soluk("  Etiketli kişiler: " + ", ".join(k.kisiler)))
        print()
        print(sar(k.icerik, "    "))
        if ilk and k.paket:
            print(yesil("\n  (Arama izniyle elde edildi.)"))

    def k_ara(self, arguman):
        if not arguman:
            print(kirmizi('  Ne arıyorsun? Örnek: ara termos   |   ara tur:kamera saat:21-23'))
            return
        sonuc, uyarilar = self.arsiv.ara(arguman, self.acik, vaka.YIL)
        for u in uyarilar:
            print(sari(f"  ! {u}"))
        print(baslik(f"ARAMA: {arguman} — {len(sonuc)} sonuç"))
        if not sonuc:
            print("  Eşleşen kanıt yok.")
            return
        zamanli = sorted(sonuc, key=lambda k: (k.zaman or datetime.max, k.id))
        self.listele(zamanli, zaman_once=True)

    def k_zaman(self, arguman):
        parcalar = arguman.split()
        if parcalar and sade(parcalar[0]) in ("isaretli", "pin", "isaretler"):
            kanitlar = sorted((self.arsiv.anahtarla[a] for a in self.durum.isaretli
                               if a in self.arsiv.anahtarla),
                              key=lambda k: (k.zaman or datetime.max, k.id))
            print(baslik(f"SENİN ZAMAN ÇİZELGEN — {len(kanitlar)} işaretli kanıt"))
            if not kanitlar:
                print("  Henüz işaretli kanıt yok. Önemli bulduklarını 'isaretle <ID>' ile ekle.")
            self.listele(kanitlar, zaman_once=True, sinir=500)
            return

        gun, aralik = None, None
        for p in parcalar:
            gun = gun or tarih_coz(p, vaka.YIL)
            aralik = aralik or saat_araligi_coz(p)
            if not tarih_coz(p, vaka.YIL) and not saat_araligi_coz(p):
                print(kirmizi(f"  '{p}' anlaşılmadı. Örnek: zaman 13.03 21:00-23:00"))
                return
        if not parcalar:
            bas, bit = vaka.OLAY_GECESI
        elif aralik:
            gun = gun or vaka.OLAY_GECESI[0].replace(hour=0, minute=0)
            bas = datetime.combine(gun.date(), aralik[0])
            bit = datetime.combine(gun.date(), aralik[1])
            if bit < bas:
                bit += timedelta(days=1)
        else:
            bas, bit = gun, gun_sonu(gun)
        kanitlar = self.arsiv.zaman_araligi(bas, bit, self.acik)
        print(baslik(f"KRONOLOJİ  {bas:%d.%m %H:%M} → {bit:%d.%m %H:%M} — {len(kanitlar)} kayıt"))
        if not parcalar:
            print(soluk("  (Olay gecesi. Başka aralık için: zaman 13.03 21:00-22:30)\n"))
        self.listele(kanitlar, zaman_once=True, sinir=150)

    def k_isaretle(self, arguman):
        if not arguman:
            self.k_liste("isaretli")
            return
        for kid in arguman.replace(",", " ").split():
            k = self.kanit_coz(kid)
            if not k:
                continue
            if k.anahtar in self.durum.isaretli:
                print(f"  {k.id} zaten işaretli.")
            else:
                self.durum.isaretli.append(k.anahtar)
                print(sari(f"  ★ {k.id} işaretlendi: {k.baslik}"))

    def k_kaldir(self, arguman):
        for kid in arguman.replace(",", " ").split():
            k = self.kanit_coz(kid)
            if k and k.anahtar in self.durum.isaretli:
                self.durum.isaretli.remove(k.anahtar)
                print(f"  {k.id} işareti kaldırıldı.")

    def k_not(self, arguman):
        if not arguman:
            self.k_notlar("")
            return
        self.durum.not_ekle(arguman)
        print(soluk("  Not deftere yazıldı."))

    def k_notlar(self, _):
        print(baslik(f"DEFTER — {len(self.durum.notlar)} not"))
        if not self.durum.notlar:
            print("  Defter boş. 'not Burak 22:00 dedi ama kamera 22:12 gösteriyor' gibi yaz.")
        for i, n in enumerate(self.durum.notlar, 1):
            print(f"  {soluk(str(i) + '.')} {soluk(n['zaman'])}  {n['metin']}")

    def k_durum(self, _):
        gorunur = self.gorunur()
        gorulen = sum(self.durum.gordu(k.anahtar) for k in gorunur)
        print(baslik("SORUŞTURMA DURUMU"))
        print(f"  İncelenen kanıt : {gorulen} / {len(gorunur)}")
        for t, (_, ad, _) in TURLER.items():
            ts = [k for k in gorunur if k.tur == t]
            g = sum(self.durum.gordu(k.anahtar) for k in ts)
            print(soluk(f"      {ad:<7} {g:>3} / {len(ts)}"))
        print(f"  İşaretli        : {len(self.durum.isaretli)}")
        print(f"  Notlar          : {len(self.durum.notlar)}")
        izinler = ", ".join(vaka.SUPHELILER[a]["ad"] for a in self.durum.izinler) or "yok"
        print(f"  Arama izinleri  : {izinler} (kalan hak: {vaka.IZIN_HAKKI - len(self.durum.izinler)})")
        print(f"  Alınan ipucu    : {self.durum.ipucu}")
        if self.durum.bitti:
            print(yesil(f"  Vaka kapandı. Puan: {self.durum.sonuc['puan']} — {self.durum.sonuc['rutbe']}"))

    def k_izin(self, arguman):
        anahtar, s = self.supheli_bul(arguman)
        if not s:
            print(kirmizi("  Kim için? Örnek: izin deniz"))
            return
        kural = vaka.IZINLER.get(anahtar, {})
        if "red" in kural:
            print(f"  Savcılık: {kural['red']}")
            return
        if anahtar in self.durum.izinler:
            print("  Bu kişi için izin zaten alındı.")
            return
        kalan = vaka.IZIN_HAKKI - len(self.durum.izinler)
        if kalan <= 0:
            print(kirmizi("  Savcı daha fazla izin vermeyecek: 'Elindekiyle çalış, dedektif.'"))
            return
        incelenen = sum(self.durum.gordu(a) for a in kural["gerekce"])
        if incelenen < kural["esik"]:
            print(sari(f"  Savcı: \"{s['ad']} hakkında bu kadar ağır bir tedbir için elimde yeterli "
                       f"gerekçe yok. Dosyada ona işaret eden daha somut şeyler bul, sonra gel.\""))
            print(soluk("  (Talep reddedildi; hakkın düşmedi.)"))
            return
        print(sari(f"  Kalan izin hakkın: {kalan}. {s['ad']} için kullanılsın mı? (e/h) "), end="")
        try:
            if sade(input().strip()) not in ("e", "evet", "y"):
                print("  Vazgeçildi.")
                return
        except EOFError:
            return
        self.durum.izinler.append(anahtar)
        yeni = [k for k in self.arsiv.kanitlar if k.paket == anahtar]
        print(yesil(f"  {kural['kabul']}"))
        print(f"  Arşive {len(yeni)} yeni kanıt eklendi:")
        self.listele(yeni)

    def k_ipucu(self, _):
        if self.durum.ipucu >= len(vaka.IPUCLARI):
            print("  Komiser Güneş: \"Sana verebileceğim her şeyi verdim. Gerisi senin işin.\"")
            return
        print(sari(f"  Bu ipucu 5 puana mal olacak. Emin misin? (e/h) "), end="")
        try:
            if sade(input().strip()) not in ("e", "evet", "y"):
                return
        except EOFError:
            return
        metin = vaka.IPUCLARI[self.durum.ipucu]
        self.durum.ipucu += 1
        print(baslik(f"KOMİSER GÜNEŞ — ipucu {self.durum.ipucu}/{len(vaka.IPUCLARI)}"))
        print(sar(metin))

    # ------------------------------------------------------------ suçlama
    def k_sucla(self, _):
        if self.durum.bitti:
            print("  Vaka zaten kapandı. 'cozum' ile hikâyenin tamamını okuyabilir, 'yeni' ile baştan "
                  "başlayabilirsin.")
            return
        print(baslik("SUÇLAMA"))
        print(sar("Komiser Güneş karşında. Sekiz soru soracak. Her cevaba istersen destekleyen "
                  "kanıtların kimliklerini ekleyebilirsin (ör. B-012 K-044). Doğru cevap 10 puan, "
                  "doğru cevabı destekleyen ve senin incelemiş olduğun en az bir kanıt +5 puan. "
                  "Bu işlem vakayı kapatır."))
        print(sari("\n  Hazır mısın? (e/h) "), end="")
        try:
            if sade(input().strip()) not in ("e", "evet", "y"):
                print("  Dosyaya geri dönüyorsun.")
                return
            cevaplar = [self.soru_sor(i, s) for i, s in enumerate(vaka.SORULAR, 1)]
        except (EOFError, KeyboardInterrupt):
            print("\n  Suçlama yarıda kaldı; vaka açık.")
            return

        puan = 0
        print(baslik("KOMİSER GÜNEŞ'İN DEĞERLENDİRMESİ"))
        for (secim, kanitlar), s in zip(cevaplar, vaka.SORULAR):
            dogru = secim == s["dogru"]
            # Yalnızca gerçekten incelenmiş kanıtlar sayılır: kimlik tahmin etmek işe yaramaz
            destek = dogru and any(k.anahtar in s["destek"] and self.durum.gordu(k.anahtar)
                                   for k in kanitlar)
            puan += (10 if dogru else 0) + (5 if destek else 0)
            isaret = yesil("✔") if dogru else kirmizi("✘")
            ek = yesil(" +kanıt") if destek else (soluk(" (kanıt desteği yok)") if dogru else "")
            print(f"  {isaret} {s['soru']}{ek}")
        ceza = self.durum.ipucu * 5
        puan = max(0, puan - ceza)
        azami = len(vaka.SORULAR) * 15
        rutbe = self.rutbe(puan, azami)
        gorulen = len(self.durum.gorulen)
        print(cizgi())
        if ceza:
            print(soluk(f"  İpucu cezası: -{ceza}"))
        print(kalin(f"  PUAN: {puan} / {azami}   RÜTBE: {rutbe}"))
        print(soluk(f"  {gorulen} kanıt inceledin (arşivde {len(self.gorunur())} kanıt vardı)."))
        katil_dogru = cevaplar[4][0] == vaka.SORULAR[4]["dogru"]
        if katil_dogru and puan >= azami * 0.75:
            print(sar("\nKomiser Güneş dosyayı kapatıyor: \"Bu bir isim değil, bir dava. Savcılık bunu "
                      "mahkemeye taşıyabilir. İyi iş, dedektif.\""))
        elif katil_dogru:
            print(sar("\nKomiser Güneş: \"Doğru kişiyi buldun ama hikâyede delikler var. İyi bir avukat "
                      "bu delikleri bulur.\""))
        else:
            print(sar("\nKomiser Güneş sessizce dosyayı geri itiyor: \"Yanlış kişiyi mahkemeye "
                      "gönderirsek gerçek katil kapıdan çıkıp gider.\""))
        self.durum.bitti = True
        self.durum.sonuc = {"puan": puan, "rutbe": rutbe}
        print(soluk("\n  Gerçekte ne olduğunu okumak için: cozum"))

    def soru_sor(self, no, s):
        soru = s["soru"]
        print("\n" + kalin(f"{no}. {soru}"))
        for i, secenek in enumerate(s["secenekler"], 1):
            print(f"   {i}) {secenek}")
        while True:
            cevap = input("  Cevabın (numara): ").strip()
            if cevap.isdigit() and 1 <= int(cevap) <= len(s["secenekler"]):
                break
            print(kirmizi(f"  1 ile {len(s['secenekler'])} arasında bir numara gir."))
        kanitlar = []
        ham = input(soluk("  Destekleyen kanıtlar (boşlukla ayır, Enter = geç): ")).replace(",", " ").split()
        for kid in ham:
            k = self.arsiv.bul(kid, self.acik)
            if k:
                kanitlar.append(k)
            else:
                print(soluk(f"    ({kid} tanınmadı, yok sayıldı)"))
        return int(cevap) - 1, kanitlar

    @staticmethod
    def rutbe(puan, azami):
        oran = puan / azami
        if oran >= 0.95:
            return "Efsanevi Başkomiser"
        if oran >= 0.8:
            return "Başkomiser"
        if oran >= 0.6:
            return "Dedektif"
        if oran >= 0.4:
            return "Komiser Yardımcısı"
        return "Çaylak"

    def k_cozum(self, _):
        if not self.durum.bitti:
            print("  Önce suçlamanı yapmalısın ('sucla'). Çözüm, vaka kapandıktan sonra açılır.")
            return
        print(baslik("ÇÖZÜM"))
        print(sar(vaka.COZUM.strip()))

    def k_yeni(self, _):
        print(sari("  Tüm ilerleme silinecek. Emin misin? (e/h) "), end="")
        try:
            if sade(input().strip()) not in ("e", "evet", "y"):
                return
        except EOFError:
            return
        self.durum = Durum(vaka=vaka.KIMLIK)
        self.kaydet()
        self.k_temizle("")
        self.acilis()

    def k_temizle(self, _):
        os.system("cls" if os.name == "nt" else "clear")
