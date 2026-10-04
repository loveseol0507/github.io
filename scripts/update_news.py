import os
import json
import datetime
import requests
from bs4 import BeautifulSoup

# 1. 저장할 경로 지정 (프로젝트 최상위 루트의 news.json)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'news.json'))

# 2. 카테고리별 다중 키워드/기업명 설정
CATEGORIES = {
    "자동차": ["현대차", "기아", "제네시스", "KG모빌리티", "현대모비스", "HL만도", "한국타이어"],
    "물류": ["CJ대한통운", "HMM", "현대글로비스", "한진", "롯데글로벌로지스", "팬스타"],
    "로봇": ["보스턴다이내믹스", "로보티즈", "뉴로메카", "유니트리", "에프알티로보틱스", "뉴빌리티"],
    "철강": ["포스코", "현대제철", "동국제강"],
    "비철금속": ["고려아연", "풍산"],
    "전력기기": ["LS일렉트릭", "대한전선", "HD현대일렉트릭"],
    "에너지": ["한화솔루션", "OCI홀딩스", "HD현대케미칼"],
    "화학소재": ["LG화학", "롯데케미칼", "금호석유화학"]
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

news_data = []
seen_urls = set() # 중복 기사 제거용 세트

print("뉴스 크롤링 시작...")

for category, keywords in CATEGORIES.items():
    cat_count = 0
    for keyword in keywords:
        if cat_count >= 10: # 카테고리당 최대 10개 채워지면 다음 카테고리로
            break
            
        url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # 네이버 뉴스 리스트 아이템 선택자
            articles = soup.select('ul.list_news > li')
            
            for article in articles:
                if cat_count >= 10:
                    break
                    
                title_tag = article.select_one('a.news_tit')
                if title_tag:
                    title = title_tag.get('title') or title_tag.text.strip()
                    link = title_tag['href']
                    
                    # 중복 기사 URL 방지
                    if link in seen_urls:
                        continue
                        
                    info_press = article.select_one('a.info.press')
                    source = info_press.text.replace('언론사 선정', '').strip() if info_press else '네이버뉴스'
                    
                    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    
                    news_data.append({
                        "category": category,
                        "title": title,
                        "source": source,
                        "date": now_str,
                        "url": link
                    })
                    seen_urls.add(link)
                    cat_count += 1
                    
        except Exception as e:
            print(f"[{category} - {keyword}] 수집 중 에러 발생: {e}")

print(f"총 {len(news_data)}건의 뉴스 수집 완료.")

# 3. news.json 파일 저장
if len(news_data) > 0:
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    print(f"파일 저장 완료: {JSON_PATH}")
else:
    print("수집된 뉴스가 없어 파일 저장을 건너뜁니다.")
