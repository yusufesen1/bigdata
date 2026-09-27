import json

with open("data/All_Beauty.jsonl", "r", encoding="utf-8") as f:
    ilk = json.loads(f.readline())

for anahtar in ilk:
    print(anahtar, type(ilk[anahtar]).__name__)

import psutil
surec = psutil.Process()
print(f"Başlangıç:{surec.memory_info().rss / 1024**2:.0f} MB")
sayac = 0
with open("data/All_Beauty.jsonl", "r", encoding="utf-8") as f:
      for satir in f:
        sayac += 1
print(f"Satır sayısı: {sayac:,}")
print(f"Bitiş:{surec.memory_info().rss / 1024**2:.0f} MB")

# %%
