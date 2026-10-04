document.addEventListener('DOMContentLoaded', () => {
    const newsContainer = document.getElementById('news-container') || document.querySelector('.news-list');
    const categoryButtons = document.querySelectorAll('#category-container button, .category-group button, .category-btn');
    
    let allNewsData = [];

    // news.json 파일 읽기
    fetch('./news.json?t=' + new Date().getTime())
        .then(response => {
            if (!response.ok) throw new Error('news.json 로드 실패');
            return response.json();
        })
        .then(data => {
            allNewsData = data;
            
            if (!allNewsData || allNewsData.length === 0) {
                if (newsContainer) newsContainer.innerHTML = '<p style="padding:20px; color:#666;">수집된 기사가 없습니다.</p>';
                return;
            }

            renderNews(allNewsData);
            setupButtons();
        })
        .catch(error => {
            console.error('데이터 로드 실패:', error);
            if (newsContainer) {
                newsContainer.innerHTML = `<p style="padding:20px; color:red;">뉴스 데이터를 불러오는 데 실패했습니다.<br>(${error.message})</p>`;
            }
        });

    function renderNews(articles) {
        if (!newsContainer) return;

        if (!articles || articles.length === 0) {
            newsContainer.innerHTML = '<p style="padding:20px; color:#666;">해당 카테고리의 기사가 없습니다.</p>';
            return;
        }

        newsContainer.innerHTML = articles.map(item => `
            <div class="news-card" style="background:#fff; border:1px solid #e1e4e8; border-radius:8px; padding:18px; margin-bottom:12px; text-align:left;">
                <h3 style="margin:0 0 8px 0; font-size:17px; font-weight:bold;">
                    <a href="${item.url}" target="_blank" rel="noopener noreferrer" style="color:#1a0dab; text-decoration:none;">
                        ${item.title}
                    </a>
                </h3>
                <div style="font-size:13px; color:#666;">
                    <span>${item.source || '언론사'}</span> | <span>${item.date || '최신'}</span> | <span style="font-weight:bold; color:#0056b3;">[${item.category}]</span>
                </div>
            </div>
        `).join('');
    }

    function setupButtons() {
        categoryButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                // 기존 모든 버튼에서 active 제거 및 파란색 스타일 초기화
                categoryButtons.forEach(b => {
                    b.classList.remove('active');
                    b.style.backgroundColor = '';
                    b.style.color = '';
                });

                // 클릭한 버튼에 active 클래스 추가
                e.target.classList.add('active');

                const selectedCategory = e.target.innerText.trim();

                if (selectedCategory === '전체') {
                    renderNews(allNewsData);
                } else {
                    const filtered = allNewsData.filter(item => item.category === selectedCategory);
                    renderNews(filtered);
                }
            });
        });
    }
});
