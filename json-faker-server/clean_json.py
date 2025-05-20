import json

valid_data = []
input_file = "fakedata.jsonl"
output_file = "fakedata_cleaned.json"

with open(input_file, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        try:
            obj = json.loads(line)
            valid_data.append(obj)
        except json.JSONDecodeError as e:
            print(f"❌ Line {i} skipped due to error: {e}")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(valid_data, f, indent=2)

print(f"✅ {len(valid_data)}개 항목 저장 완료 → {output_file}")
