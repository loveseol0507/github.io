document.addEventListener('DOMContentLoaded', () => {
    const newsContainer = document.getElementById('news-container');
    const categoryContainer = document.getElementById('category-container');
    const buttons = categoryContainer ? categoryContainer.querySelectorAll('button') : [];
    
    let allNewsData = [];

    // news.json 파일 로드 (캐시 방지 타임스탬프 추가)
    fetch('./news.json?t=' + new Date().getTime())
        .then(response => {
            if (!response.ok) throw new Error('news.json 파일을 읽을 수 없습니다.');
            return response.json();
        })
        .then(data => {
            console.log("불러온 뉴스 데이터:", data);
            allNewsData = data;
            
            if (!allNewsData || allNewsData.length === 0) {
                newsContainer.innerHTML = '<p style="padding:20px; color:#666;">수집된 기사가 없습니다.</p>';
                return;
            }

            renderNews(allNewsData);
            setupButtons();
        })
        .catch(error => {
            console.error('데이터 로드 오류:', error);
            newsContainer.innerHTML = `<p style="padding:20px; color:red;">뉴스 데이터를 불러오는 데 실패했습니다.<br>(${error.message})</p>`;
        });

    function renderNews(articles) {
        if (!articles || articles.length === 0) {
            newsContainer.innerHTML = '<p style="padding:20px; color:#666;">해당 카테고리의 기사가 없습니다.</p>';
            return;
        }

        newsContainer.innerHTML = articles.map(item => `
            <div style="background:#fff; border:1px solid #e1e4e8; border-radius:8px; padding:18px; margin-bottom:12px; text-align:left; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <h3 style="margin:0 0 8px 0; font-size:17px;">
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
        buttons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                // 파란색 버튼 스타일 즉시 적용
                buttons.forEach(b => {
                    b.style.backgroundColor = '#ffffff';
                    b.style.color = '#333333';
                    b.style.borderColor = '#e0e0e0';
                });

                e.target.style.backgroundColor = '#007bff';
                e.target.style.color = '#ffffff';
                e.target.style.borderColor = '#007bff';

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
