import os
import pyarrow.dataset as ds
import pyarrow.parquet as pq

# Yillara gore bolumlenmis Parquet veri golu
veri = ds.dataset(
    r"gol",
    format="parquet",
    partitioning="hive"
)

# Veri golundeki yillari bul
yillar = sorted(
    set(
        veri.to_table(columns=["yil"])["yil"].to_pylist()
    )
)

print("Bulunan yillar:")
print(yillar)

# Her yil icin kucuk Parquet dosyalarini birlestir
for yil in yillar:
    print(f"{yil} yili birlestiriliyor...")

    # Sadece ilgili yilin verisini oku
    alt = veri.to_table(
        filter=ds.field("yil") == yil
    )

    # Yeni klasor
    hedef = fr"gol_temiz\yil={yil}"

    os.makedirs(
        hedef,
        exist_ok=True
    )

    # O yila ait verileri tek Parquet dosyasina yaz
    pq.write_table(
        alt,
        fr"{hedef}\bolum.parquet",
        compression="snappy"
    )

print("Dosya birlestirme tamamlandi.")
