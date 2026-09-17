import urllib.request
import re
import datetime

url = "https://www.korea.kr/briefing/pressReleaseList.do"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)

try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    # 게시글 제목과 링크 추출 (정규표현식 사용)
    pattern = r'<a href="(/briefing/pressReleaseView.do\?newsId=[^"]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html)
    
    articles = []
    for link, title in matches[:15]:
        clean_title = title.strip()
        full_link = "https://www.korea.kr" + link
        if clean_title:
            articles.append((clean_title, full_link))
            
except Exception as e:
    print(f"Error: {e}")
    articles = []

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
    html_content += "        <li>수집된 보도자료가 없습니다.</li>\n"

html_content += """    </ul>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("완료")
