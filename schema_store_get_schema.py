import requests
import os
import time
from tqdm import tqdm

# 1. catalog.json URL
CATALOG_URL = "https://www.schemastore.org/api/json/catalog.json"

# 2. 저장할 폴더
SAVE_DIR = "schemas"
os.makedirs(SAVE_DIR, exist_ok=True)

# 3. catalog 가져오기
response = requests.get(CATALOG_URL)
catalog = response.json()
schemas = catalog["schemas"]

print(f"🔍 총 {len(schemas)}개의 스키마 발견")

# 4. 스키마 순회하며 다운로드
for schema in tqdm(schemas, desc="📥 스키마 다운로드"):
    name = schema["name"].replace("/", "_").replace(" ", "_")
    url = schema["url"]

    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            with open(os.path.join(SAVE_DIR, f"{name}.json"), "w", encoding="utf-8") as f:
                f.write(res.text)
        else:
            print(f"⚠️ {name}: 상태 코드 {res.status_code}")
    except Exception as e:
        print(f"❌ {name}: 다운로드 실패 ({e})")

    time.sleep(0.2)  # 요청 속도 제한
