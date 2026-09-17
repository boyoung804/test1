import urllib.request
import re
import datetime

url = "https://www.korea.kr/briefing/pressReleaseList.do"

# 헤더 설정으로 접속 차단 방지
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
articles = []

try:
    html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
    
    # <a> 태그 내 링크 및 제목 패턴
    pattern = r'<a href="(/briefing/pressReleaseView\.do\?newsId=[^"]+)"[^>]*>(.*?)</a>'
    matches = re.findall(pattern, html, re.DOTALL)
    
    for link, title in matches:
        # HTML 태그 제거 및 공백 정리
        clean_title = re.sub(r'<[^>]+>', '', title).strip()
        full_link = "https://www.korea.kr" + link
        if clean_title and len(clean_title) > 2:
            articles.append((clean_title, full_link))
            
    # 중복 제거 (순서 유지)
    seen = set()
    articles = [x for x in articles if not (x[0] in seen or seen.add(x[0]))][:15]

except Exception as e:
    print(f"크롤링 중 에러 발생: {e}")

now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>정부 보도자료 수집</title>
</head>
<body>
    <h1>대한민국 정부 최신 보도자료</h1>
    <p>최종 업데이트: {now_str}</p>
    <ul>
"""

if articles:
    for title, link in articles:
        html_content += f'        <li><a href="{link}" target="_blank">{title}</a></li>\n'
else:
    html_content += "        <li>현재 수집된 보도자료가 없거나 접속이 지연되고 있습니다.</li>\n"

html_content += """    </ul>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("작업 완료")
