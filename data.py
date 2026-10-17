import json
with open("data/All_Beauty.jsonl", "r", encoding="utf-8") as f:
    ilk = json.loads(f.readline())

for anahtar in ilk:
    print(anahtar, type(ilk[anahtar]).__name__)