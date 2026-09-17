@@ -0,0 +1,68 @@
import datetime
import json
import re
import requests
from bs4 import BeautifulSoup

# Korea.kr 보도자료 데이터 수집
url = "https://www.korea.kr/briefing/pressReleaseList.do"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

releases = []
items = soup.select(".article-list li")

for item in items:
    title_el = item.select_one(".title a")
    dept_el = item.select_one(".dept")
    summary_el = item.select_one(".text")

    if title_el and dept_el:
        title = title_el.get_text(strip=True)
        ministry = dept_el.get_text(strip=True)
        summary = summary_el.get_text(strip=True) if summary_el else ""
        link_path = title_el.get("href", "")
        link = (
            f"https://www.korea.kr{link_path}"
            if link_path.startswith("/")
            else url
        )

        releases.append(
            {
                "ministry": ministry,
                "title": title,
                "summary": summary,
                "link": link,
            }
        )

# index.html 파일 읽기 및 데이터 교체
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

now = datetime.datetime.now()
today_dot = now.strftime("%Y.%m.%d")
today_kor = now.strftime("%Y년 %m월 %d일")

html_content = re.sub(r"\d{4}\.\d{2}\.\d{2}", today_dot, html_content)
html_content = re.sub(r"\d{4}년 \d{1,2}월 \d{1,2}일", today_kor, html_content)

json_data = json.dumps(releases, ensure_ascii=False, indent=2)
html_content = re.sub(
    r"const releases = \[.*?\];",
    f"const releases = {json_data};",
    html_content,
    flags=re.DOTALL,
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("업데이트 완료")
