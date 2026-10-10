#!/usr/bin/env python3
"""Baseline evaluation of the base `english` checkpoint on demo/tickets_eval.csv.

Uses the exact same code path `finetune` uses for its "before training" scoring
(train.py:1117-1123): items_from_rows -> calibration_records -> evaluate_records,
so the numbers are directly comparable with the post-training report.
"""
import json

from laya.train import TrainConfig, load_checkpoint, read_data, items_from_rows, \
    calibration_records, evaluate_records, resolve_device

DATA = "/Users/johnson/WorkBuddy/laya-finetune/demo/tickets_eval.csv"
BASE = "english"

config = TrainConfig(text_column="body", label_column="department")
dev = resolve_device("mps")

model, tok, cfg = load_checkpoint(BASE)
model.to(dev)
max_len = cfg.get("max_len", 512)
head_max_len = cfg.get("head_max_len", 192)

rows = read_data(DATA, text_column="body", label_column="department",
                 question_id=config.question_id, instructions=config.instructions)
items, skipped = items_from_rows(tok, rows, max_len, head_max_len, label_smoothing=0.0)
print(f"eval rows read: {len(rows)}, valid items: {len(items)}, skipped: {skipped}")

records = calibration_records(model, tok, items, dev, max_len, head_max_len)
before_eval = evaluate_records(records, cfg.get("temperature"), cfg.get("temperature_by_options"))

print(json.dumps(before_eval, indent=2, ensure_ascii=False))
with open("/Users/johnson/WorkBuddy/laya-finetune/demo/baseline_eval.json", "w") as f:
    json.dump(before_eval, f, indent=2)
print("saved to demo/baseline_eval.json")
