#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建 消防刷题 index.html：读取 questions.json 内嵌进单文件 HTML"""
import json, os

BASE = r"E:\JUST_DO_IT\消防刷题"
with open(os.path.join(BASE, "questions.json"), encoding="utf-8") as f:
    data = json.load(f)

JS_DATA = json.dumps(data, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>消防安全公共知识 · 刷题</title>
<style>
  :root {
    --primary: #d32f2f; --primary-dark: #b71c1c;
    --bg: #f5f6fa; --card: #fff; --text: #2c2c2c; --muted: #888;
    --ok: #2e7d32; --ok-bg: #e8f5e9; --err: #c62828; --err-bg: #fdecea;
  }
  * { margin:0; padding:0; box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
  body { font-family: "Microsoft YaHei", "PingFang SC", sans-serif; background:var(--bg); color:var(--text); padding-bottom: 80px; }
  header { background:var(--primary); color:#fff; padding:14px 16px; position:sticky; top:0; z-index:10; box-shadow:0 2px 8px rgba(0,0,0,.15); }
  header h1 { font-size:18px; font-weight:600; }
  header .sub { font-size:12px; opacity:.85; margin-top:2px; }

  .toolbar { display:flex; gap:8px; padding:10px 12px; background:#fff; border-bottom:1px solid #eee; flex-wrap:wrap; }
  .toolbar select, .toolbar button { padding:8px 12px; border:1px solid #ddd; border-radius:8px; font-size:14px; background:#fff; }
  .toolbar button.active { background:var(--primary); color:#fff; border-color:var(--primary); }
  .toolbar .spacer { flex:1; }

  .progress { padding:8px 16px; font-size:13px; color:var(--muted); display:flex; justify-content:space-between; }
  .progress .bar-wrap { flex:1; margin:0 12px; background:#e0e0e0; border-radius:6px; height:8px; overflow:hidden; align-self:center; }
  .progress .bar { height:100%; width:0; background:var(--primary); border-radius:6px; transition:width .3s; }

  #quiz-area { padding:14px 12px; }
  .card { background:var(--card); border-radius:14px; padding:18px 16px; box-shadow:0 1px 6px rgba(0,0,0,.07); }
  .q-head { font-size:12px; color:var(--muted); margin-bottom:8px; display:flex; justify-content:space-between; }
  .q-head .tag { background:var(--primary); color:#fff; padding:2px 8px; border-radius:10px; font-size:11px; }
  .q-stem { font-size:16px; line-height:1.7; margin-bottom:14px; }
  .q-stem .blank { display:inline-block; min-width:60px; border-bottom:2px solid var(--primary); margin:0 4px; }

  .opt-list { display:flex; flex-direction:column; gap:10px; }
  .opt { border:2px solid #e0e0e0; border-radius:10px; padding:12px 14px; font-size:15px; line-height:1.5; cursor:pointer; transition:all .15s; }
  .opt:active { transform:scale(.98); }
  .opt.correct { border-color:var(--ok); background:var(--ok-bg); }
  .opt.wrong { border-color:var(--err); background:var(--err-bg); }

  .judge-row { display:flex; gap:14px; }
  .judge-btn { flex:1; padding:18px; font-size:20px; font-weight:700; border:2px solid #e0e0e0; border-radius:12px; cursor:pointer; text-align:center; background:#fff; }
  .judge-btn.correct { border-color:var(--ok); background:var(--ok-bg); }
  .judge-btn.wrong { border-color:var(--err); background:var(--err-bg); }

  .fill-input { width:100%; padding:12px 14px; font-size:16px; border:2px solid #e0e0e0; border-radius:10px; }
  .fill-input:focus { outline:none; border-color:var(--primary); }
  .fill-submit { margin-top:12px; width:100%; padding:12px; background:var(--primary); color:#fff; border:none; border-radius:10px; font-size:16px; cursor:pointer; }

  .short-ans { margin-top:14px; border-top:1px dashed #ddd; padding-top:12px; }
  .short-ans summary { cursor:pointer; color:var(--primary); font-size:14px; font-weight:600; }
  .short-ans .ans-body { margin-top:8px; font-size:14px; line-height:1.8; color:#444; background:#fafafa; padding:10px; border-radius:8px; }

  .self-row { display:flex; gap:10px; margin-top:14px; }
  .self-btn { flex:1; padding:13px; font-size:15px; border:none; border-radius:10px; cursor:pointer; color:#fff; font-weight:600; }
  .self-ok { background:var(--ok); }
  .self-no { background:var(--err); }
  .self-btn:active { transform:scale(.98); }

  .feedback { margin-top:14px; padding:12px 14px; border-radius:10px; font-size:15px; display:none; line-height:1.6; }
  .feedback.show { display:block; }
  .feedback.ok { background:var(--ok-bg); color:var(--ok); }
  .feedback.err { background:var(--err-bg); color:var(--err); }

  .nav-row { display:flex; gap:10px; margin-top:16px; }
  .nav-row button { flex:1; padding:13px; font-size:15px; border:none; border-radius:10px; cursor:pointer; }
  #btn-prev { background:#eee; color:#333; }
  #btn-next { background:var(--primary); color:#fff; }

  .stats { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-top:14px; }
  .stat { background:var(--card); border-radius:10px; padding:10px; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,.05); }
  .stat .num { font-size:20px; font-weight:700; color:var(--primary); }
  .stat .lbl { font-size:11px; color:var(--muted); margin-top:2px; }

  #empty { text-align:center; padding:60px 20px; color:var(--muted); font-size:15px; line-height:2; }
  #empty button { margin-top:16px; padding:10px 24px; background:var(--primary); color:#fff; border:none; border-radius:8px; font-size:15px; cursor:pointer; }

  footer { position:fixed; bottom:0; left:0; right:0; background:#fff; border-top:1px solid #eee; padding:10px 12px; display:flex; gap:8px; }
  footer button { flex:1; padding:10px; border:none; border-radius:8px; font-size:14px; cursor:pointer; background:#f0f0f0; color:#333; }
  footer button.primary { background:var(--primary); color:#fff; }
</style>
</head>
<body>

<header>
  <h1>🔥 消防安全公共知识 · 刷题</h1>
  <div class="sub">卷A~E · 210题 · 本地离线使用</div>
</header>

<div class="toolbar">
  <select id="paper-select">
    <option value="ALL">全部卷</option>
    <option value="A">卷A</option>
    <option value="B">卷B</option>
    <option value="C">卷C</option>
    <option value="D">卷D</option>
    <option value="E">卷E</option>
  </select>
  <select id="type-select">
    <option value="ALL">全部题型</option>
    <option value="choice">选择题</option>
    <option value="judge">判断题</option>
    <option value="fill">填空题</option>
    <option value="short">简答题</option>
  </select>
  <button id="btn-random">🎲 随机</button>
  <button id="btn-wrong">📕 错题</button>
</div>

<div class="progress" id="progress-bar">
  <span id="p-pos">0/0</span>
  <div class="bar-wrap"><div class="bar" id="p-bar"></div></div>
  <span id="p-pct">0%</span>
</div>

<div id="quiz-area"></div>
<div id="empty" style="display:none;">
  🎉 没有题了！<br>
  <button onclick="resetProgress()">重置进度 / 清空错题</button>
</div>

<div class="stats" id="stats-row">
  <div class="stat"><div class="num" id="s-total">0</div><div class="lbl">已刷</div></div>
  <div class="stat"><div class="num" id="s-ok">0</div><div class="lbl">答对</div></div>
  <div class="stat"><div class="num" id="s-rate">0%</div><div class="lbl">正确率</div></div>
</div>

<footer>
  <button id="btn-prev">◀ 上一题</button>
  <button class="primary" id="btn-next">下一题 ▶</button>
</footer>

<script>
// ===== 数据（内嵌） =====
const QUESTIONS = __DATA__;

// ===== 状态管理（localStorage 持久化） =====
const LS_KEY = "fire_quiz_v1";
let state = {
  mode: "paper",        // paper | wrong
  paper: "ALL",
  type: "ALL",
  order: [],            // 当前题序（索引数组）
  idx: 0,
  answered: {},         // qid -> {ok: bool, my: ...}
  wrongIds: [],         // 错题 qid 列表
  totalAnswered: 0,
  totalOk: 0,
};
function loadState() {
  try { const s = localStorage.getItem(LS_KEY); if (s) state = Object.assign(state, JSON.parse(s)); } catch(e) {}
}
function saveState() { localStorage.setItem(LS_KEY, JSON.stringify(state)); }
function qidOf(q, i) { return q.paper + "-" + q.type + "-" + q.no + "-" + i; }

// ===== 题序生成 =====
function filterQuestions() {
  let list = QUESTIONS.map((q, i) => ({q, i}));
  if (state.paper !== "ALL") list = list.filter(x => x.q.paper === state.paper);
  if (state.type !== "ALL") list = list.filter(x => x.q.type === state.type);
  if (state.mode === "wrong") {
    const w = new Set(state.wrongIds);
    list = list.filter(x => w.has(qidOf(x.q, x.i)));
  }
  return list.map(x => x.i);
}

// ===== 渲染 =====
function render() {
  const area = document.getElementById("quiz-area");
  const empty = document.getElementById("empty");
  if (!state.order.length) {
    area.innerHTML = "";
    empty.style.display = "block";
    document.getElementById("stats-row").style.display = "none";
    return;
  }
  empty.style.display = "none";
  document.getElementById("stats-row").style.display = "grid";

  const i = state.order[state.idx];
  const q = QUESTIONS[i];
  const qid = qidOf(q, i);
  const answered = state.answered[qid];

  // 进度条
  const done = Object.keys(state.answered).length;
  document.getElementById("p-pos").textContent = (state.idx+1) + "/" + state.order.length;
  document.getElementById("p-bar").style.width = ((state.idx+1)/state.order.length*100) + "%";
  document.getElementById("p-pct").textContent = Math.round(done/QUESTIONS.length*100) + "%";

  const typeName = {choice:"选择题", judge:"判断题", fill:"填空题", short:"简答题"}[q.type];
  let html = '<div class="card">';
  html += `<div class="q-head"><span>卷${q.paper} · ${typeName} · 第${q.no}题</span><span class="tag">${state.idx+1}/${state.order.length}</span></div>`;
  html += `<div class="q-stem">${escapeHtml(q.stem)}</div>`;

  if (q.type === "choice") {
    html += '<div class="opt-list">';
    q.options.forEach((opt, oi) => {
      const letter = opt.match(/^([A-E])[.、]/);
      const cls = answered ? (letter && letter[1] === q.answer ? "correct" : (answered.my === letter[1] ? "wrong" : "")) : "";
      html += `<div class="opt ${cls}" onclick="answer('${qid}','${letter ? letter[1] : ""}')">${escapeHtml(opt)}</div>`;
    });
    html += '</div>';
  } else if (q.type === "judge") {
    html += '<div class="judge-row">';
    ["√","×"].forEach(v => {
      const cls = answered ? (v === q.answer ? "correct" : (answered.my === v ? "wrong" : "")) : "";
      html += `<div class="judge-btn ${cls}" onclick="answer('${qid}','${v}')">${v}</div>`;
    });
    html += '</div>';
  } else if (q.type === "fill") {
    html += `<input class="fill-input" id="fill-input" type="text" placeholder="请输入答案" value="${answered && answered.my ? escapeHtml(String(answered.my)) : ""}">`;
    html += `<button class="fill-submit" onclick="submitFill('${qid}')">提交答案</button>`;
  } else { // short
    html += '<div class="short-ans"><details><summary>查看参考答案</summary><div class="ans-body">' + escapeHtml(q.answer) + '</div></details></div>';
    if (!answered) {
      html += '<div class="self-row">';
      html += `<button class="self-btn self-ok" onclick="answer('${qid}','self-ok')">✅ 我答对了</button>`;
      html += `<button class="self-btn self-no" onclick="answer('${qid}','self-no')">❌ 我没答对</button>`;
      html += '</div>';
    }
  }

  if (answered && q.type !== "short") {
    const ok = answered.ok;
    html += `<div class="feedback show ${ok ? "ok" : "err"}">${ok ? "✅ 回答正确！" : "❌ 回答错误"}`;
    if (!ok) html += `<br>正确答案：<b>${escapeHtml(String(q.answer))}</b>`;
    html += '</div>';
  } else if (answered && q.type === "short" && answered.my) {
    const ok = answered.ok;
    html += `<div class="feedback show ${ok ? "ok" : "err"}">${ok ? "✅ 自评：答对了！" : "❌ 自评：没答对（已加入错题本）"}</div>`;
  }
  html += '</div>';
  area.innerHTML = html;
  if (q.type === "fill" && !answered) {
    const inp = document.getElementById("fill-input");
    if (inp) inp.focus();
  }

  // 统计（放在最后，确保 short 自动记录已计入）
  document.getElementById("s-total").textContent = state.totalAnswered;
  document.getElementById("s-ok").textContent = state.totalOk;
  document.getElementById("s-rate").textContent = state.totalAnswered ? Math.round(state.totalOk/state.totalAnswered*100) + "%" : "0%";
}

function escapeHtml(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

// ===== 答题 =====
function answer(qid, val) {
  if (state.answered[qid]) return;
  const i = state.order[state.idx];
  const q = QUESTIONS[i];
  // 简答题：自评模式（self-ok=self-ok 判对，self-no 判错）；其他题型：严格匹配
  let ok;
  if (q.type === "short") ok = val === "self-ok";
  else ok = val === q.answer;
  record(qid, ok, val);
  render();
}
function submitFill(qid) {
  if (state.answered[qid]) return;
  const val = document.getElementById("fill-input").value;
  const i = state.order[state.idx];
  const q = QUESTIONS[i];
  // 严格匹配：trim 后完全一致
  const ok = val.trim() === q.answer.trim();
  record(qid, ok, val.trim());
  render();
}
function record(qid, ok, my) {
  state.answered[qid] = {ok, my};
  state.totalAnswered++;
  if (ok) state.totalOk++;
  else if (!state.wrongIds.includes(qid)) state.wrongIds.push(qid);
  saveState();
}

// ===== 导航 =====
function next() {
  if (state.idx < state.order.length - 1) { state.idx++; saveState(); render(); }
}
function prev() {
  if (state.idx > 0) { state.idx--; saveState(); render(); }
}

// ===== 工具栏 =====
document.getElementById("paper-select").value = state.paper;
document.getElementById("type-select").value = state.type;
document.getElementById("paper-select").onchange = e => { state.paper = e.target.value; state.mode="paper"; state.idx=0; state.order=filterQuestions(); saveState(); render(); };
document.getElementById("type-select").onchange = e => { state.type = e.target.value; state.mode="paper"; state.idx=0; state.order=filterQuestions(); saveState(); render(); };
document.getElementById("btn-random").onclick = () => {
  const list = filterQuestions().slice();
  for (let i=list.length-1; i>0; i--) { const j=Math.floor(Math.random()*(i+1)); [list[i],list[j]]=[list[j],list[i]]; }
  state.order = list; state.idx = 0; saveState(); render();
};
document.getElementById("btn-wrong").onclick = () => {
  state.mode = state.mode === "wrong" ? "paper" : "wrong";
  document.getElementById("btn-wrong").classList.toggle("active", state.mode === "wrong");
  state.idx = 0; state.order = filterQuestions(); saveState(); render();
};
document.getElementById("btn-next").onclick = next;
document.getElementById("btn-prev").onclick = prev;
document.addEventListener("keydown", e => {
  if (e.key === "ArrowRight" || e.key === "Enter") next();
  if (e.key === "ArrowLeft") prev();
});

function resetProgress() {
  if (!confirm("确定清除全部进度和错题记录？")) return;
  state = { mode:"paper", paper:"ALL", type:"ALL", order:[], idx:0, answered:{}, wrongIds:[], totalAnswered:0, totalOk:0 };
  state.order = filterQuestions();
  saveState(); render();
}
window.resetProgress = resetProgress;

// ===== 启动 =====
loadState();
state.order = filterQuestions();
render();
</script>
</body>
</html>
"""

html = html.replace("__DATA__", JS_DATA)
out = os.path.join(BASE, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"index.html written: {out}, {os.path.getsize(out)/1024:.1f} KB")
