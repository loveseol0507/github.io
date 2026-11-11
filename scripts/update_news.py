Python
import os
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

# 1. 파일 저장 경로 설정 (최상위 루트의 news.json)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'news.json'))

# 출입처 카테고리 및 키워드 설정
CATEGORIES = {
    '자동차': ['현대차', '기아', '완성차', '전기차'],
    '물류': ['해운', 'HMM', '물류', '항만'],
    '로봇': ['로보틱스', '휴머노이드', '산업용로봇'],
    '철강': ['포스코', '현대제철', '철강'],
    '비철금속': ['고려아연', '비철금속'],
    '전력기기': ['HD현대일렉트릭', '효성중공업', 'LS일렉트릭'],
    '에너지': ['수소', '신재생에너지', '원자력'],
    '화학소재': ['석유화학', '배터리소재', 'LG화학']
}

news_data = []

for category, keywords in CATEGORIES.items():
    cat_count = 0
    for keyword in keywords:
        if cat_count >= 10:
            break
        
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"
        
        try:
            # 외부 라이브러리(requests) 없이 파이썬 내장 기능으로만 접속
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()

            # BeautifulSoup 없이 내장 XML 파서 사용
            root = ET.fromstring(xml_data)
            
            for item in root.findall('./channel/item'):
                if cat_count >= 10:
                    break
                    
                title = item.findtext('title') or ''
                link = item.findtext('link') or ''
                pub_date = item.findtext('pubDate') or '최신'
                
                if not title or not link:
                    continue

                # 제목에서 " - 언론사명" 분리
                source = '언론사'
                if ' - ' in title:
                    parts = title.rsplit(' - ', 1)
                    title = parts[0]
                    source = parts[1]

                # 중복 데이터 거르기
                if not any(n['url'] == link for n in news_data):
                    news_data.append({
                        'title': title.strip(),
                        'url': link.strip(),
                        'source': source.strip(),
                        'date': pub_date[:16].strip(),
                        'category': category
                    })
                    cat_count += 1

        except Exception as e:
            print(f"[{keyword}] 수집 오류: {e}")

print(f"총 {len(news_data)}건 수집 완료.")

# 무조건 news.json 파일 덮어쓰기 (깃허브 액션이 변경점 인식하도록)
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)

print(f"파일 저장 성공: {JSON_PATH}")
