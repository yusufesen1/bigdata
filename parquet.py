import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os

# Veri golu klasoru
KOK = "gol"
os.makedirs(KOK, exist_ok=True)
# Saklamak istenen sutunlar
SUTUNLAR = [
    "rating",
    "timestamp",
    "parent_asin",
    "user_id",
    "helpful_vote",
    "verified_purchase",
    "text"
]

for parca in pd.read_json(
    r"data/Baby_Products.jsonl",
    lines=True,chunksize=200_000
):
    # Sadece gerekli sutunlari al
    parca = parca[SUTUNLAR].copy()
    # Timestamp'i tarihe donustur
    parca["zaman"] = pd.to_datetime(
        parca["timestamp"],unit="ms"
    )
    # Yil bilgisini olsutur
    parca["yil"] = parca["zaman"].dt.year.astype("int32")
    # Pandas DataFrame -> PyArrow Table
    tablo = pa.Table.from_pandas(
        parca,preserve_index=False
    )
    # Yillara gore bolumlenmis Parquet olarak yaz
    pq.write_to_dataset(
 tablo,root_path=KOK,partition_cols=["yil"],compression="snappy"
    )
print("Veri golu olusturuldu.")
