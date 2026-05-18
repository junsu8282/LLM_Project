from datasets import load_dataset
import json
from pathlib import Path
import random

random.seed(42)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# KoAlpaca 다운로드
dataset = load_dataset("beomi/KoAlpaca-v1.1a")
koalpaca = dataset["train"]

def convert_koalpaca(row):
    instruction = row["instruction"].strip()
    output = row["output"].strip()

    text = f"질문: {instruction}\n답변: {output}"

    return {"text": text}

koalpaca_rows = [convert_koalpaca(row) for row in koalpaca]

with open(DATA_DIR / "phase1_koalpaca.jsonl", "w", encoding="utf-8") as f:
    for row in koalpaca_rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print("완료")
print(f"총 데이터 수: {len(koalpaca_rows)}")