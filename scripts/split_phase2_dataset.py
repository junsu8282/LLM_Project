import json
import random

input_path = "data/phase2_mixed.jsonl"
train_path = "data/phase2_train.jsonl"
valid_path = "data/phase2_valid.jsonl"

random.seed(42)

with open(input_path, "r", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f]

random.shuffle(rows)

split_idx = int(len(rows) * 0.9)
train_rows = rows[:split_idx]
valid_rows = rows[split_idx:]

with open(train_path, "w", encoding="utf-8") as f:
    for row in train_rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

with open(valid_path, "w", encoding="utf-8") as f:
    for row in valid_rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print("train:", len(train_rows))
print("valid:", len(valid_rows))