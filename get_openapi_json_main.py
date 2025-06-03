import requests
import yaml
import json
import csv
import time
import os

# 마지막 주소 https://api.orthanc-server.com/orthanc-openapi.json

def get_list_json():
    response = requests.get("https://api.apis.guru/v2/list.json")
    response.raise_for_status()
    return response.json()

def fetch_schema(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        if url.endswith(".json"):
            return response.json()
        elif url.endswith(".yaml") or url.endswith(".yml"):
            result = yaml.safe_load(response.text)
            if not isinstance(result, dict):
                raise ValueError("YAML is not a dict")
            return result
    except Exception as e:
        print(f"[!] 실패: {url} → {e}")
        return None

def extract_schema_paths(schema):
    if not isinstance(schema, dict):
        print("[!] ⚠️ 스키마가 dict가 아님 → 건너뜀")
        return []

    paths = []
    components = schema.get("components", {})
    schemas = components.get("schemas", {})
    for schema_name, schema_def in schemas.items():
        base = f"{schema_name}"
        paths.append(base)
        if "properties" in schema_def:
            for prop in schema_def["properties"]:
                paths.append(f"{base}.properties.{prop}")
    return paths

def main():
    list_json = get_list_json()
    output_file = "openapi_schema_paths.csv"
    max_apis = 2000
    processed = 0

    # 🔁 이어서 시작할 기준 URL
    start_url = "https://api.orthanc-server.com/orthanc-openapi.json"
    started = False

    # 헤더는 파일 없을 때만 작성
    if not os.path.exists(output_file):
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["json_path"])

    for api_name, api_info in list_json.items():
        if processed >= max_apis:
            break

        preferred = api_info.get("preferred")
        version_data = api_info.get("versions", {}).get(preferred, {})
        x_origin = version_data.get("info", {}).get("x-origin", [])
        if x_origin and "url" in x_origin[0]:
            url = x_origin[0]["url"]
            if not started:
                if url == start_url:
                    started = True
                else:
                    continue  

            if url.endswith((".json", ".yaml", ".yml")):
                print(f" [{processed+1}] {url}")
                schema = fetch_schema(url)
                if schema:
                    paths = extract_schema_paths(schema)
                    with open(output_file, "a", newline="") as f:
                        writer = csv.writer(f)
                        for path in paths:
                            writer.writerow([path])
                processed += 1
                time.sleep(0.2)

    print(f"\n✅ 완료: 총 {processed}개 API 처리 완료, 결과는 '{output_file}'에 저장됨.")

if __name__ == "__main__":
    main()
