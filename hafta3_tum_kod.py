# Hücre 0: hazırlık. Not defterini her açtığınızda ilk bunu çalıştırın.
import os, glob, json, hashlib, shutil
from pathlib import Path

# Not defteri gol klasörünün yanındaysa bu satıra dokunmayın.
CALISMA = Path.cwd()
# Değilse gol klasörünün İÇİNDE durduğu klasörü yazın, örneğin:
# CALISMA = Path(r"D:\bvders")

os.chdir(CALISMA)
print("Calisma klasoru :", os.getcwd())
if not os.path.isdir("gol"):
    raise FileNotFoundError(f"{CALISMA} icinde gol klasoru yok")

# Hücre 1: gölde en büyük dosyayı bul
adaylar = glob.glob("gol/yil=*/*.parquet")
if not adaylar:
    raise FileNotFoundError("gol/yil=*/ altinda parquet dosyasi yok")

KAYNAK = max(adaylar, key=os.path.getsize)
BOYUT = os.path.getsize(KAYNAK)

print("Dosya :", KAYNAK)
print(f"Boyut : {BOYUT / 1024**2:.2f} MB")

# Hücre 2: dosyayı parçalara kes (KAYNAK Hücre 1'den gelir)
PARCA_BOYUTU = 4 * 1024 * 1024        # 4 MB

parcalar = []
with open(KAYNAK, "rb") as f:
    i = 0
    while True:
        veri = f.read(PARCA_BOYUTU)
        if not veri:
            break
        parcalar.append((f"parca_{i:04d}", veri))
        i += 1

print(f"Parca sayisi : {len(parcalar)}")
print(f"Son parca    : {len(parcalar[-1][1]) / 1024**2:.2f} MB")

# Hücre 3: parçaları üç makineye dağıt, kataloğu yaz
# (parcalar Hücre 2'den, KAYNAK Hücre 1'den gelir)
MAKINELER = ["makine1", "makine2", "makine3"]
KOPYA = 2

for m in MAKINELER:
    shutil.rmtree(m, ignore_errors=True)
    os.makedirs(m)

katalog = {}
for sira, (ad, veri) in enumerate(parcalar):
    yerler = []
    for k in range(KOPYA):
        hedef = MAKINELER[(sira + k) % len(MAKINELER)]
        with open(f"{hedef}/{ad}", "wb") as f:
            f.write(veri)
        yerler.append(hedef)
    katalog[ad] = {"yerler": yerler, "boyut": len(veri)}

with open("katalog.json", "w") as f:
    json.dump({"kaynak": KAYNAK, "parca_boyutu": PARCA_BOYUTU,
               "kopya": KOPYA, "parcalar": katalog}, f, indent=2)
print("Dagitim tamam, katalog.json yazildi")

# Hücre 4: hangi makinede ne var, ne kadar yer tuttu
for m in MAKINELER:
    dosyalar = sorted(os.listdir(m))
    numaralar = [int(x.split("_")[1]) for x in dosyalar]
    yer = sum(os.path.getsize(f"{m}/{x}") for x in dosyalar)
    print(f"{m}: {numaralar}  ({yer / 1024**2:.1f} MB)")

toplam = sum(sum(os.path.getsize(f"{m}/{x}") for x in os.listdir(m))
             for m in MAKINELER)
print(f"Diskte toplam : {toplam / 1024**2:.1f} MB")
print(f"Kac kat yer   : {toplam / BOYUT:.2f}")

# Hücre 5: birleştirme ve parmak izi fonksiyonları
# (sadece tanımlar, çalıştırınca ekrana bir şey yazmaz)
def birlestir(hedef_dosya="geri_gelen.parquet"):
    with open("katalog.json") as f:
        kat = json.load(f)
    kayip = []
    with open(hedef_dosya, "wb") as cikti:
        for ad, bilgi in kat["parcalar"].items():
            bulundu = None
            for yer in bilgi["yerler"]:
                yol = f"{yer}/{ad}"
                if os.path.exists(yol):
                    bulundu = yol
                    break
            if bulundu is None:
                kayip.append(ad)
                continue
            with open(bulundu, "rb") as f:
                cikti.write(f.read())
    return kayip

def parmak_izi(yol):
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for p in iter(lambda: f.read(1024 * 1024), b""):
            h.update(p)
    return h.hexdigest()

# Hücre 6: hiçbir şey silmeden birleştir
asil = parmak_izi(KAYNAK)
kayip = birlestir()
print("Kayip parca :", len(kayip))
print("Ayni mi     :", parmak_izi("geri_gelen.parquet") == asil)

# Hücre 7: makine2 bozuldu
shutil.rmtree("makine2", ignore_errors=True)

kayip = birlestir()
print("Kayip parca :", len(kayip))
print("Ayni mi     :", parmak_izi("geri_gelen.parquet") == asil)

# Hücre 8: makine3 de bozuldu (makine2 hâlâ yok)
shutil.rmtree("makine3", ignore_errors=True)

kayip = birlestir()
print("Kayip parca sayisi :", len(kayip))
print("Kayip parcalar     :", kayip)
print("Ayni mi            :", parmak_izi("geri_gelen.parquet") == asil)

# Hücre 3 tekrar: makineleri geri kur
# (not defterinde Hücre 3’e dönülür, düz dosyada kod tekrar yazılır)
MAKINELER = ["makine1", "makine2", "makine3"]
KOPYA = 2

for m in MAKINELER:
    shutil.rmtree(m, ignore_errors=True)
    os.makedirs(m)

katalog = {}
for sira, (ad, veri) in enumerate(parcalar):
    yerler = []
    for k in range(KOPYA):
        hedef = MAKINELER[(sira + k) % len(MAKINELER)]
        with open(f"{hedef}/{ad}", "wb") as f:
            f.write(veri)
        yerler.append(hedef)
    katalog[ad] = {"yerler": yerler, "boyut": len(veri)}

with open("katalog.json", "w") as f:
    json.dump({"kaynak": KAYNAK, "parca_boyutu": PARCA_BOYUTU,
               "kopya": KOPYA, "parcalar": katalog}, f, indent=2)
print("Dagitim tamam, katalog.json yazildi")

# Hücre 9: Hücre 3'ü yeniden çalıştırdıktan sonra kontrol
kayip = birlestir()
print("Kayip parca :", len(kayip))
print("Ayni mi     :", parmak_izi("geri_gelen.parquet") == asil)

# Hücre 10: hesabı nerede yapacaksınız
import pandas as pd

bolumler = sorted(glob.glob("gol/yil=*/*.parquet"))

# Yol A: butun dosyalari merkeze getir, sonra hesapla
tasinan_a = sum(os.path.getsize(b) for b in bolumler)
parcalar_df = [pd.read_parquet(b, columns=["rating"]) for b in bolumler]
hepsi = pd.concat(parcalar_df)
sonuc_a = hepsi["rating"].mean()

# Yol B: hesabi her makinede yap, sadece sonucu tasi
tasinan_b = 0
toplam_puan, adet = 0.0, 0
for b in bolumler:
    d = pd.read_parquet(b, columns=["rating"])
    toplam_puan += float(d["rating"].sum())
    adet += len(d)
    tasinan_b += 16          # iki sayi, sekizer bayt
sonuc_b = toplam_puan / adet

print(f"A yolu tasinan : {tasinan_a / 1024**2:10.1f} MB   sonuc {sonuc_a:.4f}")
print(f"B yolu tasinan : {tasinan_b / 1024**2:10.6f} MB   sonuc {sonuc_b:.4f}")
print(f"Aradaki fark   : {tasinan_a / tasinan_b:,.0f} kat")

# Hücre 11: kontrol 1, parmak izi
# Önce dosyayı temiz halden yeniden birleştir
kayip = birlestir()
print("Kayip parca :", len(kayip))
print("Orijinal    :", parmak_izi(KAYNAK)[:16])
print("Geri gelen  :", parmak_izi("geri_gelen.parquet")[:16])
print("SONUC       :", "AYNI" if parmak_izi(KAYNAK) == parmak_izi("geri_gelen.parquet") else "FARKLI")

# Hücre 12: kontrol 2, dosya hâlâ açılıyor mu
import pandas as pd

orijinal = pd.read_parquet(KAYNAK)
geri = pd.read_parquet("geri_gelen.parquet")
print("Orijinal satir :", len(orijinal))
print("Geri gelen     :", len(geri))
print("Sutunlar ayni  :", list(orijinal.columns) == list(geri.columns))

# Hücre 13: kontrol 4, diskte kaç kat yer
toplam = sum(sum(os.path.getsize(f"{m}/{x}") for x in os.listdir(m))
             for m in MAKINELER if os.path.exists(m))
print(f"Dosya       : {BOYUT / 1024**2:.1f} MB")
print(f"Klasorlerde : {toplam / 1024**2:.1f} MB")
print(f"Kac kat     : {toplam / BOYUT:.2f}  (beklenen {KOPYA})")
