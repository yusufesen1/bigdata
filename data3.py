import os
import pyarrow.dataset as ds
import pyarrow.parquet as pq

# Yıllara göre bölünmüş Parquet veri gölünü aç
veri = ds.dataset(
    r"gol",
    format="parquet",
    partitioning="hive"
)

# Veri gölündeki yılları bul
yillar = sorted(
    set(
        veri.to_table(columns=["yil"])["yil"].to_pylist()
    )
)

print("Bulunan yıllar:")
print(yillar)

# Her yıl için küçük dosyaları birleştir
for yil in yillar:
    print(f"{yil} yılı birleştiriliyor...")

    # Sadece ilgili yılın verisini oku
    alt = veri.to_table(
        filter=ds.field("yil") == yil
    )

    # Yeni klasör
    hedef = fr"gol_temiz\yil={yil}"

    os.makedirs(
        hedef,
        exist_ok=True
    )

    # O yıla ait verileri tek Parquet dosyasına yaz
    pq.write_table(
        alt,
        fr"{hedef}\bolum.parquet",
        compression="snappy"
    )

print("Dosya birleştirme tamamlandı.")
