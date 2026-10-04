document.addEventListener('DOMContentLoaded', () => {
  fetchNews();
});

async function fetchNews() {
  const container = document.getElementById('news-container');
  
  try {
    // GitHub에 저장된 news.json 데이터 요청
    const response = await fetch('news.json');
    if (!response.ok) throw new Error('뉴스 데이터를 불러올 수 없습니다.');
    
    const newsData = await response.json();
    renderNews(newsData);
  } catch (error) {
    console.error('Error:', error);
    container.innerHTML = `<p style="color:red;">뉴스를 불러오는 중 오류가 발생했습니다.</p>`;
  }
}

function renderNews(articles) {
  const container = document.getElementById('news-container');
  container.innerHTML = ''; // 기존 '불러오는 중' 문구 제거

  if (!articles || articles.length === 0) {
    container.innerHTML = '<p>등록된 뉴스가 없습니다.</p>';
    return;
  }

  // 뉴스 목록 생성
  articles.forEach(article => {
    const newsCard = document.createElement('div');
    newsCard.className = 'news-card';

    newsCard.innerHTML = `
      <h3><a href="${article.url}" target="_blank" rel="noopener noreferrer">${article.title}</a></h3>
      <div class="meta">
        <span>${article.media || '언론사'}</span> | <span>${article.date || '최신'}</span>
      </div>
    `;

    container.appendChild(newsCard);
  });
}
