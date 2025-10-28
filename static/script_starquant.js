const $ = (id)=>document.getElementById(id);

function pick(arr, alt){ return Array.isArray(arr) ? arr : (alt||[]); }
function field(s, a, b){ return (s && (s[a] ?? s[b])) ?? []; } // 兼容老字段/新字段

async function loadAll() {
  try {
    const r = await fetch('/api/data');
    const s = await r.json();

    // 顶部状态
    const status = (s.status && (s.status.status || s.status.phase)) || "--";
    $('mstatus').innerText = status;
    $('mtime').innerText = s.update_time || "--";

    // 打板
    const boards = field(s, 'board', 'board_suggestions');
    let b = `<tr><th>代码</th><th>名称</th><th>分数</th></tr>`;
    pick(boards).forEach(x => b += `<tr><td>${x.code||''}</td><td>${x.name||''}</td><td>${x.score??''}</td></tr>`);
    $('board').innerHTML = b;

    // 预测
    const preds = s.predictions || [];
    let p = `<tr><th>代码</th><th>名称</th><th>T+1</th><th>T+3</th><th>置信%</th></tr>`;
    preds.forEach(x => p += `<tr><td>${x.code||''}</td><td>${x.name||''}</td><td>${x.t1||x.T1||''}</td><td>${x.t3||x.T3||''}</td><td>${(x.confidence??'')}</td></tr>`);
    $('pred').innerHTML = p;

    // 文案 & 学习
    $('copy').innerText = s.copy_text || '暂无文案';
    const acc = (s.learning && s.learning.accuracy!=null) ? s.learning.accuracy : null;
    $('acc').innerText = acc==null ? '--' : `${(+acc).toFixed(2)}%`;

    // 新闻
    const news = field(s, 'news', 'news_data');
    $('news').innerHTML = pick(news).slice(0,12).map(n => `<li>📢 ${n.title||''}</li>`).join('');

    // 自选
    renderWatchlist(s.watchlist || []);
  } catch(e) {
    console.error('加载失败', e);
  }
}

function renderWatchlist(list){
  if(!Array.isArray(list) || !list.length){ $('watchlist').innerHTML = '<div>（空）</div>'; return; }
  let html = `<table class="table"><tr><th>代码</th><th>名称</th></tr>`;
  list.forEach(x => html += `<tr><td>${x.code||''}</td><td>${x.name||''}</td></tr>`);
  html += `</table>`;
  $('watchlist').innerHTML = html;
}

// --- 搜索 / 添加 / 删除 ---
async function doSearch(){
  const q = $('q').value.trim();
  if(!q){ $('search').innerHTML = ''; return; }
  const r = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
  const data = await r.json();
  const list = data.results || [];
  if(!list.length){ $('search').innerHTML = '<div>未找到结果</div>'; return; }
  let html = `<table class="table"><tr><th>代码</th><th>名称</th><th>价格</th><th>涨跌%</th></tr>`;
  list.forEach(x => html += `<tr><td>${x.code||''}</td><td>${x.name||''}</td><td>${x.price??''}</td><td>${x.pct??''}</td></tr>`);
  html += `</table>`;
  $('search').innerHTML = html;
}

async function addWatch(){
  const txt = $('q').value.trim();
  if(!txt) return;
  // 从搜索结果里挑第一条
  const r = await fetch(`/api/search?q=${encodeURIComponent(txt)}`);
  const d = await r.json();
  const first = (d.results||[])[0];
  if(!first){ alert('没找到股票'); return; }
  await fetch('/api/add',{method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({code:first.code, name:first.name})});
  loadAll();
}

async function delWatch(){
  const code = $('q').value.trim();
  if(!code) return;
  await fetch('/api/delete',{method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({code})});
  loadAll();
}

// 定时刷新
loadAll();
setInterval(loadAll, 10000);
