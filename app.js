document.addEventListener('DOMContentLoaded', () => {
  renderCategoryButtons();
  fetchNews();
});

// keywords.js의 keywords 객체를 기반으로 출입처 버튼 생성
function renderCategoryButtons() {
  const container = document.getElementById('category-container');
  if (!container || typeof keywords === 'undefined') return;

  container.innerHTML = '';
  // '전체' 및 keywords 객체의 키값(자동차, 물류, 로봇 등) 배열 생성
  const categories = ['전체', ...Object.keys(keywords)];
  
  categories.forEach((cat, index) => {
    const btn = document.createElement('button');
    btn.className = `category-btn ${index === 0 ? 'active' : ''}`;
    btn.textContent = cat;
    btn.onclick = () => filterNews(cat, btn);
    container.appendChild(btn);
  });
}

let allNews = [];

// news.json 데이터 불러오기
async function fetchNews() {
  const container = document.getElementById('news-container');
  try {
    const response = await fetch('news.json');
    if (!response.ok) throw new Error('뉴스 데이터를 불러올 수 없습니다.');
    
    allNews = await response.json();
    renderNews(allNews);
  } catch (error) {
    console.error('Error:', error);
    container.innerHTML = `<p style="color:red;">뉴스를 불러오는 중 오류가 발생했습니다.</p>`;
  }
}

// 뉴스 카드 화면 출력
function renderNews(articles) {
  const container = document.getElementById('news-container');
  container.innerHTML = '';

  if (!articles || articles.length === 0) {
    container.innerHTML = '<p>등록된 뉴스가 없습니다.</p>';
    return;
  }

  articles.forEach(article => {
    const newsCard = document.createElement('div');
    newsCard.className = 'news-card';

    const mediaName = article.source || article.media || '언론사';

    newsCard.innerHTML = `
      <h3><a href="${article.url}" target="_blank" rel="noopener noreferrer">${article.title}</a></h3>
      <div class="meta">
        <span>${mediaName}</span> | <span>${article.date || '최신'}</span>
      </div>
    `;

    container.appendChild(newsCard);
  });
}

// 출입처 버튼 클릭 시 필터링
function filterNews(category, selectedBtn) {
  document.querySelectorAll('.category-btn').forEach(btn => btn.classList.remove('active'));
  selectedBtn.classList.add('active');

  if (category === '전체') {
    renderNews(allNews);
  } else {
    const filtered = allNews.filter(item => item.category === category);
    renderNews(filtered);
  }
}
