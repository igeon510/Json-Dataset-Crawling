import requests
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(BASE_DIR, "schemas")
OUTPUT_FILE = os.path.join(BASE_DIR, "fakedata.jsonl")

if not os.path.exists(SCHEMA_DIR):
    raise Exception(f"❌ 스키마 폴더가 존재하지 않음: {SCHEMA_DIR}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
    for filename in os.listdir(SCHEMA_DIR):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(SCHEMA_DIR, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    print(f"⚠️ {filename} → 비어있는 파일 (스킵)")
                    continue

                if "$ref" in content:
                    print(f"⚠️ {filename} → '$ref' 포함 (스킵)")
                    continue

                schema = json.loads(content)

        except json.JSONDecodeError as e:
            print(f"⚠️ {filename} → JSON 파싱 실패 (스킵): {e}")
            continue

        try:
            res = requests.post("http://localhost:3000/generate", json={
                "schema": schema,
                "count": 10
            }, timeout=10)
            res.raise_for_status()
            samples = res.json()

            output_file.write(json.dumps({
                "source": filename,
                "samples": samples
            }) + "\n")

            print(f"✅ {filename} → 생성 완료")
        except Exception as e:
            print(f"❌ {filename} → 생성 실패: {e}")
