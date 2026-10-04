import json
import re
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup


def load_keywords():
  """keywords.js 파일에서 출입처별 키워드 디크셔너리를 추출합니다."""
  try:
    with open('keywords.js', 'r', encoding='utf-8') as f:
      content = f.read()
    # const keywords = { ... }; 부분에서 { ... } 객체 텍스트만 추출
    match = re.search(r'keywords\s*=\s*(\{.*?\});', content, re.DOTALL)
    if match:
      json_str = match.group(1)
      # JS 객체 포맷을 파이썬 json 파싱이 가능하도록 정리
      return json.loads(json_str)
  except Exception as e:
    print(f'keywords.js 로드 중 오류 발생: {e}')

  # 기본 예시 키워드 fallback
  return {
      '자동차': ['현대차', '기아', '현대모비스'],
      '물류': ['대한통운', 'HMM', '현대글로비스'],
      '로봇': ['뉴로메카', '레인보우로보틱스'],
  }


def fetch_naver_news(category, keyword_list):
  """네이버 뉴스 검색을 통해 관련 기사를 수집합니다."""
  articles = []
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

  for kw in keyword_list[:3]:  # 속도를 위해 주요 키워드 상위 3개 검색
    encoded_kw = urllib.parse.quote(kw)
    url = f'https://search.naver.com/search.naver?where=news&query={encoded_kw}'

    req = urllib.request.Request(url, headers=headers)
    try:
      html = urllib.request.urlopen(req).read().decode('utf-8')
      soup = BeautifulSoup(html, 'html.parser')

      # 네이버 뉴스 검색 결과 리스트 파싱
      news_items = soup.select('div.news_wrap.api_ani_send') or soup.select(
          'ul.list_news > li'
      )

      for item in news_items[:2]:  # 키워드당 최대 2건 추출
        title_tag = item.select_one('a.news_tit')
        media_tag = item.select_one('a.info.press') or item.select_one('a.info')

        if title_tag:
          title = title_tag.get('title') or title_tag.get_text()
          link = title_tag.get('href')
          media = media_tag.get_text() if media_tag else '언론사'

          articles.append({
              'category': category,
              'title': title.strip(),
              'source': media.strip().replace('언론사 언론사 선정', ''),
              'date': '최신',
              'url': link,
          })
    except Exception as e:
      print(f"'{kw}' 검색 중 오류: {e}")
      continue

  return articles


def main():
  keywords_dict = load_keywords()
  all_news = []

  for category, kw_list in keywords_dict.items():
    print(f'[{category}] 카테고리 뉴스 수집 중...')
    fetched = fetch_naver_news(category, kw_list)
    all_news.extend(fetched)

  if all_news:
    with open('news.json', 'w', encoding='utf-8') as f:
      json.dump(all_news, f, ensure_ascii=False, indent=2)
    print(f'총 {len(all_news)}건의 뉴스를 news.json에 저장했습니다.')
  else:
    print('수집된 뉴스가 없습니다.')


if __name__ == '__main__':
  main()
