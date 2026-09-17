import urllib.request
import re
from bs4 import BeautifulSoup
import datetime

# korea.kr 보도자료 목록 페이지 주소
url = "https://www.korea.kr/briefing/pressReleaseList.do"

req = urllib.request.Request(
    url, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
)

articles = []

try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # 보도자료 게시글 요소 탐색
    items = soup.select('.article-list li, .list_type li, .news_list li')
    
    for item in items:
        title_tag = item.select_one('a, .title, strong')
        date_tag = item.select_one('.date, .time, span')
        
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag.get('href', '')
            if link and not link.startswith('http'):
                link = 'https://www.korea.kr' + link
            
            date = date_tag.get_text(strip=True) if date_tag else datetime.datetime.now().strftime("%Y-%m-%d")
            
            if title and len(title) > 2:
                articles.append({'title': title, 'link': link, 'date': date})
except Exception as e:
    print(f"크롤링 에러 발생: {e}")

# 만약 데이터 수집 실패 시 예시 알림 처리
now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>정부 보도자료 자동 수집</title>
    <style>
        body {{ font-family: 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif; margin: 30px; background-color: #f8f9fa; color: #333; }}
        h1 {{ border-bottom: 2px solid #0056b3; padding-bottom: 10px; color: #0056b3; }}
        .update-time {{ color: #6c757d; font-size: 0.9em; margin-bottom: 20px; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ background: #fff; margin-bottom: 10px; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        a {{ text-decoration: none; color: #1a0dab; font-weight: bold; font-size: 1.1em; }}
        a:hover {{ text-decoration: underline; }}
        .date {{ color: #28a745; font-size: 0.85em; margin-left: 10px; }}
    </style>
</head>
<body>
    <h1>🏛️ 대한민국 정부 최신 보도자료</h1>
    <div class="update-time">최종 업데이트 시간: {now_str} (KST)</div>
    <ul>
"""

if articles:
    for art in articles[:15]:  # 상위 15개 출력
        html_content += f"""        <li>
            <a href="{art['link']}" target="_blank">{art['title']}</a>
            <span class="date">[{art['date']}]</span>
        </li>\n"""
else:
    html_content += "        <li>현재 수집된 보도자료가 없거나 수집 중입니다. (잠시 후 다시 시도해 주세요)</li>\n"

html_content += """    </ul>
</body>
</html>"""

# index.html 파일 저장
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("index.html 업데이트 완료!")
