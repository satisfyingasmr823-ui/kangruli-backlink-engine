# scripts/check_backlinks.py
import csv
import sys
import requests
from bs4 import BeautifulSoup

TARGET_DOMAIN = "kangruli.web.id"
HEADERS = {"User-Agent": "Mozilla/5.0 (backlink-monitor)"}

def check(source_url: str) -> dict:
    result = {"source": source_url, "status": "", "found": False,
              "rel": "", "anchor": "", "error": ""}
    try:
        r = requests.get(source_url, headers=HEADERS, timeout=15)
        result["status"] = r.status_code
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            if TARGET_DOMAIN in a["href"]:
                result["found"] = True
                result["rel"] = " ".join(a.get("rel", [])) or "dofollow"
                result["anchor"] = a.get_text(strip=True)[:120]
                break
    except requests.RequestException as e:
        result["error"] = str(e)[:200]
    return result

def main(path: str) -> None:
    with open(path, newline="", encoding="utf-8") as f:
        sources = [row["source_url"] for row in csv.DictReader(f)]

    fields = ["source", "status", "found", "rel", "anchor", "error"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    for url in sources:
        writer.writerow(check(url))

if __name__ == "__main__":
    main(sys.argv[1])
