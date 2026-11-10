Python
import os
import json
import urllib.parse
import xml.etree.ElementTree as ET
import requests

# 1. 저장할 경로 지정 (최상위 루트의 news.json)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'news.json'))

# 출입처 카테고리 및 키워드 설정
CATEGORIES = {
    '자동차': ['현대차', '기아', '완성차', '전기차'],
    '물류': ['해운', 'HMM', '물류', '항만'],
    '로봇': ['로보틱스', '휴머노이드', '산업용로봇'],
    '철강': ['포스코', '현대제철', '철강'],
    '비철금속': ['고려아연', '비철금속'],
    '전력기기': ['HD현대일렉트릭', '효성중공업', 'LS일렉트릭', '변압기'],
    '에너지': ['수소', '신재생에너지', '원자력'],
    '화학소재': ['석유화학', '배터리소재', 'LG화학']
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

news_data = []

for category, keywords in CATEGORIES.items():
    cat_count = 0
    for keyword in keywords:
        if cat_count >= 10:
            break
        
        # 네이버 뉴스 RSS 검색 API 사용 (해외 IP 차단 없음)
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"
        
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code != 200:
                continue

            # XML 파싱
            root = ET.fromstring(res.text)
            items = root.findall('.//item')

            for item in items:
                if cat_count >= 10:
                    break

                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else '최신'
                
                # 언론사명 분리 (보통 제목 끝에 '- 언론사명' 형태로 붙음)
                source = '언론사'
                if ' - ' in title:
                    parts = title.rsplit(' - ', 1)
                    title = parts[0]
                    source = parts[1]

                # 중복 방지
                if not any(n['url'] == link for n in news_data):
                    news_data.append({
                        'title': title,
                        'url': link,
                        'source': source,
                        'date': pub_date[:16], # 날짜 포맷 깔끔하게 자르기
                        'category': category
                    })
                    cat_count += 1

        except Exception as e:
            print(f"Error fetching {keyword}: {e}")

print(f"총 {len(news_data)}건의 뉴스 수집 완료.")

# 무조건 파일 저장
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)

print(f"파일 저장 완료: {JSON_PATH}")
