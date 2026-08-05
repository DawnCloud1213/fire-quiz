#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建 消防刷题 v0.2 index.html：液态玻璃 + 毛玻璃 + Anthropic 配色 + Apple 动效"""
import json, os

BASE = r"E:\JUST_DO_IT\消防刷题"
with open(os.path.join(BASE, "questions.json"), encoding="utf-8") as f:
    data = json.load(f)

JS_DATA = json.dumps(data, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>消防安全公共知识 · 刷题</title>
<style>
  /* ============ Design Tokens (Anthropic 路线) ============ */
  :root {
    /* 基础色 */
    --bg: #F5F1EA;            /* 暖米白背景 */
    --bg-deep: #EDE8DF;       /* 背景深一档（内容层/分隔） */
    --ink: #281F15;           /* 深棕黑文字 */
    --ink-2: #5A5144;         /* 次级文字 */
    --ink-3: #8A8178;         /* 弱化文字 */
    --paper: #FBF9F4;         /* 实体卡片色 */
    --paper-2: #F1EDE4;       /* 卡片hover/嵌入色 */

    /* 强调色（消防红降饱和 → 陶土砖红） */
    --accent: #B4553D;        /* 陶土红（主强调） */
    --accent-strong: #8E3D2A; /* 深陶土（按压/标题） */
    --accent-soft: #E8D5CC;   /* 浅陶土（选中底/反馈底） */
    --ok: #5B7A54;            /* 对—— 苔绿（Anthropic 系低饱和） */
    --ok-bg: #E4EBE1;
    --err: #A63D2F;           /* 错—— 暗红 */
    --err-bg: #F3E3DF;

    /* 毛玻璃（题目卡） */
    /* 毛玻璃材质（题目卡）：半透明 + 强 blur，背景色块透出模糊 */
    --glass-frost-bg: rgba(251, 249, 244, 0.52);
    --glass-frost-blur: 26px;
    --glass-frost-border: rgba(255, 255, 255, 0.55);

    /* 液态玻璃（浮动控件） */
    --glass-liq-bg: rgba(251, 249, 244, 0.42);
    --glass-liq-border: rgba(255, 255, 255, 0.65);

    /* 圆角（Apple squircle 系，Windows 观感 ×1.2） */
    --r-panel: 26px;
    --r-card: 22px;
    --r-btn: 14px;
    --r-row: 12px;
    --r-pill: 999px;

    /* 阴影 */
    --shadow-1: 0 1px 3px rgba(40, 31, 21, 0.06), 0 4px 16px rgba(40, 31, 21, 0.07);
    --shadow-2: 0 2px 6px rgba(40, 31, 21, 0.08), 0 12px 32px rgba(40, 31, 21, 0.12);
    --shadow-glass: 0 2px 6px rgba(40, 31, 21, 0.08), 0 10px 30px rgba(40, 31, 21, 0.12), 0 20px 50px rgba(40, 31, 21, 0.08);

    /* 字体（英文衬线标题 + 中文无衬线正文） */
    --font-display: "Georgia", "Times New Roman", "Songti SC", "SimSun", serif;
    --font-body: -apple-system, "PingFang SC", "Microsoft YaHei UI", "Segoe UI", sans-serif;

    /* 弹簧动效参数（Apple：damping 1.0 默认，0.8 带弹性） */
    --spring-standard: cubic-bezier(0.34, 1.6, 0.64, 1);  /* 弹簧：明显过冲回弹（iOS 手感） */
    --spring-settle: cubic-bezier(0.22, 1, 0.36, 1);        /* 收敛：缓出 */
    --ease-inout: cubic-bezier(0.65, 0, 0.35, 1);
  }

  * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

  body {
    font-family: var(--font-body);
    background: var(--bg);
    color: var(--ink);
    min-height: 100vh;
    padding-bottom: 96px;
    overflow-x: hidden;
  }

  /* ============ 背景装饰色块层（毛玻璃的"素材"：blur 有内容可模糊） ============ */
  .bg-deco {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
    contain: strict;  /* 防止子元素撑开滚动区域 */
  }
  .bg-deco .blob {
    position: absolute;
    border-radius: 38% 62% 55% 45% / 45% 40% 60% 55%;  /* 不规则柔和形状 */
    filter: blur(2px);
    max-width: 100%;
  }
  .bg-deco .b1 { width: 340px; height: 300px; top: -60px; left: -80px; background: rgba(222, 190, 170, 0.38); transform: rotate(12deg); }
  .bg-deco .b2 { width: 280px; height: 260px; top: 30%; right: -90px; background: rgba(210, 190, 165, 0.30); transform: rotate(-18deg); }
  .bg-deco .b3 { width: 220px; height: 200px; bottom: 8%; left: 12%; background: rgba(225, 200, 178, 0.25); transform: rotate(28deg); }
  .bg-deco .b4 { width: 180px; height: 170px; bottom: -40px; right: 25%; background: rgba(215, 195, 175, 0.28); transform: rotate(-8deg); }
  .bg-deco .b5 { width: 150px; height: 140px; top: 18%; left: 45%; background: rgba(228, 208, 188, 0.18); transform: rotate(40deg); }

  /* 消防元素装饰 SVG（Anthropic 式低饱和线条风，不抢内容） */
  .bg-deco .fire-svg {
    position: absolute;
    opacity: 0.22;
    filter: blur(0.5px);
  }
  .bg-deco .fire-svg svg { width: 100%; height: 100%; }
  /* 灭火器：右上角 */
  .fire-svg.extinguisher { width: 110px; height: 150px; top: 14%; right: 5%; transform: rotate(8deg); }
  /* 消防员（头盔+身体）：左侧中间偏上 */
  .fire-svg.firefighter { width: 150px; height: 200px; top: 22%; left: 3%; transform: rotate(-4deg); }
  /* 水流弧线（消防员 → 火焰）：跨页面连接 */
  .fire-svg.stream { width: 420px; height: 260px; top: 30%; left: 12%; opacity: 0.20; transform: rotate(-6deg); }
  /* 火焰：右下被水浇 */
  .fire-svg.flame1 { width: 80px; height: 100px; bottom: 14%; right: 10%; transform: rotate(-6deg); }
  /* 小火焰：左下 */
  .fire-svg.flame2 { width: 48px; height: 62px; bottom: 4%; left: 30%; transform: rotate(12deg); }
  /* 水珠：沿水流散布 */
  .fire-svg.drop1 { width: 36px; height: 46px; top: 36%; left: 26%; transform: rotate(-18deg); }
  .fire-svg.drop2 { width: 28px; height: 36px; top: 42%; left: 38%; transform: rotate(8deg); }
  .fire-svg.drop3 { width: 32px; height: 40px; bottom: 24%; left: 52%; transform: rotate(-10deg); }
  /* 消防栓：左下角 */
  .fire-svg.hydrant { width: 70px; height: 100px; bottom: 6%; left: 6%; transform: rotate(-5deg); }

  /* 内容层 z-index（bg-deco 之上），但不影响 fixed 定位的浮层 */
  body > header,
  body > .toolbar,
  body > .progress,
  body > #quiz-area,
  body > .stats,
  body > footer { position: relative; z-index: 1; }

  /* ============ 液态玻璃材质（工具栏/统计/导航——已定稿，保持） ============ */
  .glass-liquid {
    background: var(--glass-liq-bg);
    -webkit-backdrop-filter: blur(10px) saturate(160%);
    backdrop-filter: blur(10px) saturate(160%);
    border: 1px solid var(--glass-liq-border);
    box-shadow: var(--shadow-glass), inset 0 1px 0 rgba(255,255,255,0.7);
    position: relative;
  }
  /* 顶部亮边：光打进来的感觉（克制，不抢内容） */
  .glass-liquid::before {
    content: "";
    position: absolute; top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent);
    pointer-events: none;
  }
  .glass-liquid > * { position: relative; z-index: 1; }

  /* ============ 毛玻璃材质（题目卡） ============ */
  .glass-frost {
    background: var(--glass-frost-bg);
    -webkit-backdrop-filter: blur(var(--glass-frost-blur)) saturate(180%);
    backdrop-filter: blur(var(--glass-frost-blur)) saturate(180%);
    border: 1px solid var(--glass-frost-border);
    box-shadow: var(--shadow-2), inset 0 1px 0 rgba(255,255,255,0.8);
    position: relative;
  }  .glass-frost::after {  /* 顶部亮边（光打进来的感觉） */
    content: "";
    position: absolute; top: 0; left: 8%; right: 8%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.9), transparent);
    pointer-events: none;
  }

  /* ============ 布局 ============ */
  header {
    padding: 18px 20px 14px;
    position: sticky; top: 0; z-index: 20;
  }
  header .brand { display: flex; align-items: baseline; gap: 12px; }
  header h1 {
    font-family: var(--font-display);
    font-size: 24px; font-weight: 700;
    letter-spacing: -0.01em;
    color: var(--ink);
  }
  header .brand-en {
    font-family: var(--font-display);
    font-size: 13px; font-style: italic; color: var(--ink-3);
  }
  header .sub { font-size: 12.5px; color: var(--ink-3); margin-top: 3px; }

  .toolbar {
    display: flex; gap: 10px; padding: 12px 14px;
    margin: 4px 16px 12px;
    border-radius: var(--r-card);
    flex-wrap: wrap;
    animation: glassIn 0.5s var(--spring-standard) both;
    z-index: 40;
  }
  .toolbar select {
    flex: 1 1 130px;
    padding: 9px 12px;
    font-family: var(--font-body); font-size: 14px;
    color: var(--ink);
    background: rgba(255,255,255,0.45);
    border: 1px solid rgba(40,31,21,0.12);
    border-radius: var(--r-btn);
    outline: none;
    transition: border-color 0.2s;
  }
  .toolbar select:focus { border-color: var(--accent); }

  /* ===== 自研液态玻璃下拉 ===== */
  .drop { position: relative; flex: 1 1 130px; }
  .drop-btn {
    width: 100%;
    display: flex; align-items: center; justify-content: space-between; gap: 8px;
    padding: 9px 14px;
    font-family: var(--font-body); font-size: 14px;
    color: var(--ink);
    background: rgba(255,255,255,0.45);
    border: 1px solid rgba(40,31,21,0.12);
    border-radius: var(--r-btn);
    cursor: pointer;
    transition: border-color 0.2s, transform 0.15s var(--spring-standard), box-shadow 0.2s;
    -webkit-user-select: none; user-select: none;
  }
  .drop-btn:hover { border-color: rgba(40,31,21,0.25); }
  .drop-btn.open {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(180, 85, 61, 0.10);
  }
  .drop-btn .chevron {
    width: 0; height: 0;
    border-left: 5px solid transparent; border-right: 5px solid transparent;
    border-top: 6px solid var(--ink-3);
    transition: transform 0.3s var(--spring-standard);
  }
  .drop-btn.open .chevron { transform: rotate(180deg); }

  .drop-panel {
    position: fixed;
    border-radius: var(--r-row);
    /* 毛玻璃浮层：半透明 + 强 blur，背后内容透出模糊（Apple menu 毛玻璃感） */
    background: rgba(251, 249, 244, 0.55);
    -webkit-backdrop-filter: blur(32px) saturate(180%);
    backdrop-filter: blur(32px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.70);
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,0.9),    /* 顶部柔光 */
      inset 0 -1px 1px rgba(255,255,255,0.35),
      0 12px 36px -8px rgba(120, 60, 30, 0.18), /* 暖色投影 */
      0 4px 12px rgba(120, 60, 30, 0.08);
    padding: 6px;
    z-index: 100;
    opacity: 0; visibility: hidden;
    transform: translateY(-8px) scale(0.96);
    transform-origin: top center;
    /* 收起：transform 用弹簧（回弹可见），opacity 用慢速淡出（比回弹更晚结束） */
    transition: opacity 0.5s ease-out 0.05s, transform 0.38s var(--spring-standard), visibility 0s 0.55s;
  }
  .drop-panel.show {
    opacity: 1; visibility: visible;
    transform: none;
    /* 展开：opacity 快速淡入，transform 弹簧（轻微过冲） */
    transition: opacity 0.22s ease-out, transform 0.38s var(--spring-standard), visibility 0s;
  }
  .drop-opt {
    position: relative; z-index: 5;
    padding: 8px 14px;
    font-size: 14px; color: var(--ink-2);
    border-radius: calc(var(--r-row) - 4px);
    cursor: pointer;
    transition: background 0.15s, color 0.15s, transform 0.12s var(--spring-standard);
  }
  .drop-opt:hover { background: rgba(180, 85, 61, 0.10); color: var(--accent-strong); }
  .drop-opt.selected {
    background: var(--accent); color: #FFF8F2; font-weight: 600;
    box-shadow: 0 2px 8px rgba(180, 85, 61, 0.25);
  }
  .drop-opt:active { transform: scale(0.98); }
  .toolbar button {
    padding: 9px 16px;
    font-family: var(--font-body); font-size: 14px;
    color: var(--ink);
    background: rgba(255,255,255,0.45);
    border: 1px solid rgba(40,31,21,0.12);
    border-radius: var(--r-btn);
    box-shadow: 0 1px 3px rgba(40, 31, 21, 0.06);
    cursor: pointer;
    transition: transform 0.15s var(--spring-standard), background 0.2s, box-shadow 0.2s;
  }
  .toolbar button:active { transform: scale(0.94); }
  .toolbar button.active {
    background: var(--accent); color: #FFF8F2;
    border-color: var(--accent);
    box-shadow: 0 3px 10px rgba(180, 85, 61, 0.35);
  }

  .progress {
    margin: 0 16px 14px;
    padding: 10px 16px;
    border-radius: var(--r-row);
    display: flex; align-items: center; gap: 12px;
    font-size: 12.5px; color: var(--ink-3);
  }
  .progress .bar-wrap {
    flex: 1; height: 5px;
    background: rgba(40,31,21,0.08);
    border-radius: 4px; overflow: hidden;
  }
  .progress .bar {
    height: 100%; width: 0;
    background: var(--accent);
    border-radius: 4px;
    transition: width 0.5s var(--spring-settle);
  }

  #quiz-area { padding: 2px 16px 10px; }
  .card {
    border-radius: var(--r-panel);
    padding: 22px 20px;
    position: relative;
  }
  /* ===== 切题动画：View Transitions 交叉过渡（大厂 fade-through 模式，无空窗） ===== */
  .q-body { view-transition-name: quiz-body; }
  /* 旧快照：轻微上移淡出 */
  ::view-transition-old(quiz-body) {
    animation: vtOld 140ms ease-in both;
  }
  @keyframes vtOld {
    from { opacity: 1; transform: translateY(0); }
    to   { opacity: 0; transform: translateY(-6px); }
  }
  /* 新快照：从下方淡入（与旧内容交叉重叠） */
  ::view-transition-new(quiz-body) {
    animation: vtNew 240ms var(--spring-standard) both;
  }
  @keyframes vtNew {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: none; }
  }
  /* 非 API 环境降级：旧内容快速淡出（无空窗感知的兜底） */
  .q-body.leaving {
    opacity: 0;
    transform: translateY(-6px);
    transition: opacity 140ms ease-in, transform 140ms ease-in;
  }

  /* ===== 模式切换动画：整卡 quick fade（M3 top-level 模式） ===== */
  .card { view-transition-name: quiz-card; }
  ::view-transition-old(quiz-card) {
    animation: vtCardOld 140ms ease-in both;
  }
  @keyframes vtCardOld {
    from { opacity: 1; }
    to   { opacity: 0; }
  }
  ::view-transition-new(quiz-card) {
    animation: vtCardNew 240ms var(--spring-standard) both;
  }
  @keyframes vtCardNew {
    from { opacity: 0; }
    to   { opacity: 1; }
  }
  .card-leave {
    opacity: 0;
    transition: opacity 140ms ease-in;
  }
  .empty-leave {
    opacity: 0;
    transition: opacity 140ms ease-in;
  }
  .empty-enter {
    animation: vtNew 240ms var(--spring-standard) both;
  }

  .q-head {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 10px;
  }
  .q-head .crumb { font-size: 12.5px; color: var(--ink-3); }
  .q-head .crumb b { color: var(--ink-2); font-weight: 600; }
  .q-head .tag {
    font-family: var(--font-display);
    font-size: 13px; color: var(--accent-strong);
    background: rgba(180, 85, 61, 0.10);
    padding: 3px 12px; border-radius: var(--r-pill);
  }
  .q-stem {
    font-size: 16.5px; line-height: 1.85;
    margin-bottom: 18px;
    color: var(--ink);
  }
  .q-stem .blank {
    display: inline-block; min-width: 64px;
    border-bottom: 2px solid var(--accent);
    margin: 0 4px;
  }

  /* 选项（毛玻璃上更偏实体，保证可读） */
  .opt-list { display: flex; flex-direction: column; gap: 10px; }
  .opt {
    border: 1.5px solid rgba(40,31,21,0.10);
    border-radius: var(--r-row);
    padding: 13px 16px;
    font-size: 15px; line-height: 1.55;
    background: rgba(255,255,255,0.42);
    box-shadow: 0 1px 3px rgba(40, 31, 21, 0.05);
    cursor: pointer;
    transition: transform 0.15s var(--spring-standard), background 0.2s, border-color 0.2s, box-shadow 0.2s;
  }
  .opt:hover { box-shadow: 0 3px 10px rgba(40, 31, 21, 0.10); }
  .opt:active { transform: scale(0.975); }
  .opt.correct {
    border-color: var(--ok); background: var(--ok-bg);
    box-shadow: 0 2px 10px rgba(91,122,84,0.20);
  }
  .opt.wrong {
    border-color: var(--err); background: var(--err-bg);
    box-shadow: 0 2px 10px rgba(166,61,47,0.18);
  }

  .judge-row { display: flex; gap: 14px; }
  .judge-btn {
    flex: 1; padding: 20px;
    font-size: 24px; font-weight: 700;
    border: 1.5px solid rgba(40,31,21,0.10);
    border-radius: var(--r-card);
    background: rgba(255,255,255,0.42);
    cursor: pointer;
    transition: transform 0.15s var(--spring-standard), background 0.2s, border-color 0.2s;
  }
  .judge-btn:active { transform: scale(0.96); }
  .judge-btn.correct { border-color: var(--ok); background: var(--ok-bg); }
  .judge-btn.wrong { border-color: var(--err); background: var(--err-bg); }

  .fill-input {
    width: 100%; padding: 14px 16px;
    font-family: var(--font-body); font-size: 16px;
    color: var(--ink);
    background: rgba(255,255,255,0.55);
    border: 1.5px solid rgba(40,31,21,0.12);
    border-radius: var(--r-btn);
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .fill-input:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(180, 85, 61, 0.12);
  }
  .fill-submit {
    margin-top: 12px; width: 100%; padding: 14px;
    font-family: var(--font-body); font-size: 16px; font-weight: 600;
    color: #FFF8F2;
    background: var(--accent);
    border: none; border-radius: var(--r-btn);
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(180, 85, 61, 0.25), 0 6px 18px rgba(180, 85, 61, 0.30);
    transition: transform 0.15s var(--spring-standard), box-shadow 0.2s;
  }
  .fill-submit:active { transform: scale(0.97); box-shadow: 0 2px 8px rgba(180,85,61,0.25); }

  .short-ans { margin-top: 16px; border-top: 1px dashed rgba(40,31,21,0.15); padding-top: 14px; }
  .ans-toggle {
    cursor: pointer; color: var(--accent-strong);
    font-size: 14px; font-weight: 600;
    font-family: var(--font-body);
    background: none; border: none; padding: 0;
    display: flex; align-items: center; gap: 6px;
    -webkit-user-select: none; user-select: none;
  }
  .ans-toggle .chev {
    display: inline-block;
    transition: transform 300ms var(--spring-standard);
    font-size: 10px;
  }
  .ans-toggle.open .chev { transform: rotate(180deg); }
  /* 手风琴展开：grid 0fr→1fr 可动画高度（容器始终 display:block，transition 才能生效） */
  .ans-wrap {
    display: grid;
    grid-template-rows: 0fr;
    transition: grid-template-rows 350ms var(--spring-standard);
  }
  .ans-wrap.open { grid-template-rows: 1fr; }
  .ans-wrap > div { overflow: hidden; }
  .ans-wrap .ans-body {
    margin-top: 10px; font-size: 14.5px; line-height: 1.9;
    color: var(--ink-2);
    background: rgba(255,255,255,0.45);
    padding: 14px; border-radius: var(--r-row);
    opacity: 0;
    transform: translateY(-6px);
    transition: opacity 250ms ease 80ms, transform 250ms var(--spring-standard) 80ms;
  }
  .ans-wrap.open .ans-body {
    opacity: 1;
    transform: none;
  }

  .self-row { display: flex; gap: 10px; margin-top: 16px; }
  .self-btn {
    flex: 1; padding: 14px;
    font-size: 15px; font-weight: 600;
    border: none; border-radius: var(--r-btn);
    cursor: pointer; color: #fff;
    transition: transform 0.15s var(--spring-standard), box-shadow 0.2s;
  }
  .self-ok { background: var(--ok); box-shadow: 0 3px 12px rgba(91,122,84,0.30); }
  .self-no { background: var(--err); box-shadow: 0 3px 12px rgba(166,61,47,0.28); }
  .self-btn:active { transform: scale(0.96); }
  /* 当前自评选中态（upsert 可改判） */
  .self-btn.chosen { outline: 2px solid var(--ink-2); outline-offset: 2px; }
  .self-btn:not(.chosen) { opacity: 0.85; }

  .feedback {
    margin-top: 16px; padding: 14px 16px;
    border-radius: var(--r-row);
    font-size: 15px; line-height: 1.7;
    display: none;
    animation: glassIn 0.3s var(--spring-standard) both;
  }
  .feedback.show { display: block; }
  .feedback.ok { background: var(--ok-bg); color: var(--ok); }
  .feedback.err { background: var(--err-bg); color: var(--err); }

  .nav-row { display: flex; gap: 12px; margin-top: 18px; }
  .nav-row button {
    flex: 1; padding: 15px;
    font-size: 15px; font-weight: 600;
    border: none; border-radius: var(--r-btn);
    cursor: pointer;
    transition: transform 0.15s var(--spring-standard), box-shadow 0.2s;
  }
  .nav-row button:active { transform: scale(0.97); }
  #btn-prev { background: rgba(40,31,21,0.07); color: var(--ink-2); }
  #btn-next {
    background: var(--ok); color: #FFF8F2;
    box-shadow: 0 4px 14px rgba(91,122,84,0.30);
  }

  /* 统计区：液态玻璃（紧凑高度，避免把切题按钮挤出屏外） */
  .stats {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;
    margin: 4px 16px 10px;
    padding: 8px 10px;
    border-radius: var(--r-card);
    animation: glassIn 0.5s var(--spring-standard) both;
  }
  .stat { text-align: center; padding: 4px 4px; }
  .stat .num {
    font-family: var(--font-display);
    font-size: 20px; font-weight: 700;
    line-height: 1.15;
    color: var(--accent-strong);
  }
  .stat .lbl { font-size: 11px; color: var(--ink-3); margin-top: 2px; line-height: 1.2; }

  #empty { text-align: center; padding: 70px 24px; color: var(--ink-3); font-size: 15px; line-height: 2; view-transition-name: quiz-empty; }
  ::view-transition-old(quiz-empty) { animation: vtCardOld 140ms ease-in both; }
  ::view-transition-new(quiz-empty) { animation: vtCardNew 240ms var(--spring-standard) both; }
  #empty button {
    margin-top: 18px; padding: 12px 28px;
    background: var(--accent); color: #FFF8F2;
    border: none; border-radius: var(--r-btn);
    font-size: 15px; cursor: pointer;
  }

  /* 收藏按钮（题目卡头部，题目标签右侧） */
  .fav-btn {
    display: inline-flex; align-items: center; justify-content: center;
    width: 28px; height: 28px;
    margin-left: 8px;
    vertical-align: middle;
    background: rgba(255,255,255,0.5);
    border: 1px solid rgba(40,31,21,0.10);
    border-radius: 50%;
    cursor: pointer;
    font-size: 15px;
    transition: transform 0.15s var(--spring-standard), background 0.2s, box-shadow 0.2s;
  }
  .fav-btn:hover { background: rgba(255,255,255,0.8); box-shadow: 0 2px 8px rgba(40,31,21,0.10); }
  .fav-btn:active { transform: scale(0.9); }
  .fav-btn.on { background: rgba(255, 236, 200, 0.7); box-shadow: 0 0 0 1px rgba(200, 150, 60, 0.3); }

  /* 清除记录按钮（工具栏最右侧） */
  .btn-clear {
    padding: 9px 16px;
    font-family: var(--font-body); font-size: 14px;
    color: var(--err);
    background: rgba(255,255,255,0.45);
    border: 1px solid rgba(166, 61, 47, 0.25);
    border-radius: var(--r-btn);
    box-shadow: 0 1px 3px rgba(40, 31, 21, 0.06);
    cursor: pointer;
    transition: transform 0.15s var(--spring-standard), background 0.2s;
  }
  .btn-clear:hover { background: var(--err-bg); }
  .btn-clear:active { transform: scale(0.94); }

  /* 底部导航：液态玻璃悬浮 */
  footer {
    position: fixed; bottom: 0; left: 0; right: 0;
    padding: 12px 16px calc(12px + env(safe-area-inset-bottom));
    z-index: 30;
  }
  footer .dock {
    display: flex; gap: 12px;
    border-radius: var(--r-panel);
    padding: 12px;
    animation: glassIn 0.5s var(--spring-standard) both;
  }
  footer button {
    flex: 1; padding: 13px;
    font-size: 15px; font-weight: 600;
    border: none; border-radius: var(--r-btn);
    cursor: pointer;
    transition: transform 0.15s var(--spring-standard), box-shadow 0.2s;
  }
  footer button:active { transform: scale(0.97); }
  footer .btn-prev { background: rgba(255,255,255,0.35); color: var(--ink-2); border: 1px solid rgba(40,31,21,0.08); box-shadow: 0 1px 3px rgba(40,31,21,0.06); }
  footer .btn-next {
    background: var(--ok); color: #FFF8F2;
    box-shadow: 0 2px 4px rgba(91,122,84,0.25), 0 6px 18px rgba(91,122,84,0.30);
  }

  /* 键盘焦点可见性 */
  :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

  /* 减少动效偏好 */
  @media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
    .q-body.leaving, .card-leave, .empty-leave { opacity: 1; transform: none; }
    ::view-transition-old(quiz-body), ::view-transition-new(quiz-body),
    ::view-transition-old(quiz-card), ::view-transition-new(quiz-card),
    ::view-transition-old(quiz-empty), ::view-transition-new(quiz-empty) { animation: none !important; }
    .glass-liquid::after, .glass-frost::after { display: none; }
  }
  /* 减弱透明度偏好 */
  @media (prefers-reduced-transparency: reduce) {
    .glass-liquid { background: var(--paper); -webkit-backdrop-filter: none; backdrop-filter: none; }
    .glass-frost { background: var(--paper); -webkit-backdrop-filter: none; backdrop-filter: none; }
  }

  /* 手机窄屏 */
  @media (max-width: 480px) {
    header h1 { font-size: 20px; }
    header { padding: 14px 16px 10px; }
    .toolbar { margin: 4px 10px 10px; gap: 8px; padding: 10px 10px; }
    /* 工具栏按钮小屏时两行排列，保证可点 */
    .toolbar .drop { flex: 1 1 46%; }
    .toolbar button { flex: 1 1 30%; padding: 12px 10px; font-size: 13.5px; }
    .toolbar .btn-clear { flex: 1 1 100%; }
    #quiz-area { padding: 2px 10px 8px; }
    .progress { margin: 0 10px 12px; padding: 8px 12px; }
    .stats { margin: 2px 10px 8px; }
    footer { padding: 10px 10px calc(10px + env(safe-area-inset-bottom)); }
    .q-stem { font-size: 16px; line-height: 1.8; }
    /* 触摸目标放大（44px 触控标准） */
    .opt { padding: 15px 16px; font-size: 15.5px; }
    .judge-btn { padding: 22px; }
    .fill-input { padding: 15px 16px; font-size: 17px; }
    .fill-submit { padding: 16px; }
    .self-btn { padding: 16px; }
    footer .dock { padding: 10px; }
    footer button { padding: 15px; font-size: 15.5px; }
    .card { padding: 20px 16px; }
    /* 背景消防元素小屏时淡化（避免遮挡） */
    .bg-deco .fire-svg { opacity: 0.12; }
  }

  /* 超窄屏（<360px，老安卓） */
  @media (max-width: 360px) {
    header h1 { font-size: 18px; }
    .brand-en { display: none; }
    .toolbar .drop { flex: 1 1 100%; }
    .toolbar button { flex: 1 1 46%; }
    .q-head .crumb { font-size: 11.5px; }
    .q-head .tag { font-size: 11.5px; }
  }
</style>
</head>
<body>

<!-- 背景装饰色块（毛玻璃 blur 的素材） + 消防场景元素 -->
<div class="bg-deco" aria-hidden="true">
  <div class="blob b1"></div>
  <div class="blob b2"></div>
  <div class="blob b3"></div>
  <div class="blob b4"></div>
  <div class="blob b5"></div>

  <!-- 灭火器（右上角待命） -->
  <div class="fire-svg extinguisher">
    <svg viewBox="0 0 100 140" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M30 60 C30 38, 42 26, 50 26 C58 26, 70 38, 70 60 L70 105 C70 118, 63 125, 50 125 C37 125, 30 118, 30 105 Z"
            stroke="#B4553D" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M40 26 L40 18 C40 14, 45 12, 50 12 C55 12, 60 14, 60 18 L60 26"
            stroke="#B4553D" stroke-width="4" stroke-linecap="round"/>
      <path d="M44 12 C44 4, 56 4, 56 12" stroke="#B4553D" stroke-width="4" stroke-linecap="round"/>
      <circle cx="50" cy="60" r="8" stroke="#B4553D" stroke-width="3.5"/>
      <path d="M50 60 L54 55" stroke="#B4553D" stroke-width="2.5" stroke-linecap="round"/>
      <path d="M30 50 C20 48, 16 44, 14 38" stroke="#B4553D" stroke-width="4" stroke-linecap="round"/>
      <path d="M14 38 L8 34" stroke="#B4553D" stroke-width="4.5" stroke-linecap="round"/>
      <path d="M35 100 L65 100" stroke="#B4553D" stroke-width="3" stroke-linecap="round"/>
      <path d="M35 108 L60 108" stroke="#B4553D" stroke-width="3" stroke-linecap="round"/>
    </svg>
  </div>

  <!-- 消防员（头盔+身体+水枪，左侧喷水） -->
  <div class="fire-svg firefighter">
    <svg viewBox="0 0 150 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- 头盔 -->
      <path d="M38 78 C38 48, 56 36, 75 36 C94 36, 112 48, 112 78 Z"
            stroke="#B4553D" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M28 78 C28 86, 122 86, 122 78" stroke="#B4553D" stroke-width="5" stroke-linecap="round"/>
      <path d="M52 52 C62 45, 88 45, 98 52" stroke="#B4553D" stroke-width="3.5" stroke-linecap="round"/>
      <path d="M70 62 L75 54 L80 62 Z" stroke="#B4553D" stroke-width="3" stroke-linejoin="round"/>
      <!-- 面部 -->
      <circle cx="75" cy="92" r="14" stroke="#B4553D" stroke-width="3.5"/>
      <!-- 身体 -->
      <path d="M55 110 L55 160 C55 172, 65 178, 75 178 C85 178, 95 172, 95 160 L95 110"
            stroke="#B4553D" stroke-width="4.5" stroke-linecap="round"/>
      <!-- 手臂（持水枪伸向右下） -->
      <path d="M95 118 C110 122, 124 128, 132 136" stroke="#B4553D" stroke-width="4" stroke-linecap="round"/>
      <!-- 水枪 -->
      <path d="M132 136 L146 128" stroke="#B4553D" stroke-width="5" stroke-linecap="round"/>
      <!-- 防护带 -->
      <path d="M55 118 L95 118" stroke="#C98A6B" stroke-width="3" stroke-linecap="round"/>
      <path d="M55 128 L95 128" stroke="#C98A6B" stroke-width="3" stroke-linecap="round"/>
    </svg>
  </div>

  <!-- 水流弧线（消防员水枪 → 右下火焰） -->
  <div class="fire-svg stream">
    <svg viewBox="0 0 420 260" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- 水柱主弧线 -->
      <path d="M10 220 C120 200, 220 180, 320 150 C360 138, 395 122, 415 105"
            stroke="#7A94B5" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 14"/>
      <!-- 水柱内层 -->
      <path d="M10 214 C120 194, 220 174, 320 144 C360 132, 395 116, 415 99"
            stroke="#7A94B5" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="1 10"/>
      <!-- 溅起的水花（火焰上方） -->
      <path d="M415 105 C425 98, 420 88, 414 92" stroke="#7A94B5" stroke-width="3" stroke-linecap="round"/>
      <path d="M408 112 C416 118, 425 110, 418 104" stroke="#7A94B5" stroke-width="3" stroke-linecap="round"/>
      <circle cx="400" cy="96" r="3" stroke="#7A94B5" stroke-width="2"/>
      <circle cx="425" cy="102" r="2.5" stroke="#7A94B5" stroke-width="2"/>
      <circle cx="412" cy="88" r="2" stroke="#7A94B5" stroke-width="2"/>
    </svg>
  </div>

  <!-- 火焰 1（右下，被水浇） -->
  <div class="fire-svg flame1">
    <svg viewBox="0 0 60 80" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M30 6 C34 20, 48 30, 46 48 C45 60, 38 70, 30 70 C22 70, 15 60, 14 48 C13 38, 20 30, 22 22 C24 30, 30 32, 30 26 C30 18, 26 12, 30 6 Z"
            stroke="#B4553D" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M30 30 C33 38, 40 42, 39 52 C38 58, 35 62, 30 62 C25 62, 22 58, 21 52 C21 47, 24 43, 26 38"
            stroke="#C98A6B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>

  <!-- 火焰 2（更小，左下角） -->
  <div class="fire-svg flame2">
    <svg viewBox="0 0 50 66" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M25 4 C28 16, 40 25, 38 40 C37 50, 31 58, 25 58 C19 58, 13 50, 12 40 C11 32, 17 26, 18 19 C20 26, 25 28, 25 22 C25 16, 22 10, 25 4 Z"
            stroke="#B4553D" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>

  <!-- 水珠 1（水流中段） -->
  <div class="fire-svg drop1">
    <svg viewBox="0 0 40 50" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M20 4 C24 16, 32 22, 31 33 C30 41, 26 45, 20 45 C14 45, 10 41, 9 33 C8 22, 16 16, 20 4 Z"
            stroke="#7A94B5" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>

  <!-- 水珠 2 -->
  <div class="fire-svg drop2">
    <svg viewBox="0 0 34 42" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M17 3 C20 13, 27 18, 26 28 C25 34, 22 37, 17 37 C12 37, 9 34, 8 28 C7 18, 14 13, 17 3 Z"
            stroke="#7A94B5" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>

  <!-- 水珠 3 -->
  <div class="fire-svg drop3">
    <svg viewBox="0 0 36 44" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M18 3 C21 14, 29 19, 28 30 C27 37, 23 40, 18 40 C13 40, 9 37, 8 30 C7 19, 15 14, 18 3 Z"
            stroke="#7A94B5" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>

  <!-- 消防栓（左下角） -->
  <div class="fire-svg hydrant">
    <svg viewBox="0 0 70 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- 栓体 -->
      <rect x="24" y="30" width="22" height="55" rx="5" stroke="#B4553D" stroke-width="4"/>
      <!-- 顶部盖 -->
      <path d="M18 30 L52 30" stroke="#B4553D" stroke-width="4.5" stroke-linecap="round"/>
      <path d="M28 22 L42 22" stroke="#B4553D" stroke-width="4" stroke-linecap="round"/>
      <circle cx="35" cy="16" r="4" stroke="#B4553D" stroke-width="3"/>
      <!-- 侧出水口 -->
      <path d="M24 45 L12 45 L12 52 L24 52" stroke="#B4553D" stroke-width="3.5" stroke-linejoin="round"/>
      <path d="M46 45 L58 45 L58 52 L46 52" stroke="#B4553D" stroke-width="3.5" stroke-linejoin="round"/>
      <!-- 底部基座 -->
      <path d="M18 85 L52 85" stroke="#B4553D" stroke-width="4.5" stroke-linecap="round"/>
      <path d="M14 92 L56 92" stroke="#B4553D" stroke-width="4.5" stroke-linecap="round"/>
    </svg>
  </div>
</div>

<header>
  <div class="brand">
    <h1>消防安全公共知识</h1>
    <span class="brand-en">Fire Safety Quiz</span>
  </div>
  <div class="sub">卷A~E · 210 题 · 本地离线使用</div>
</header>

<div class="toolbar glass-liquid">
  <div class="drop" id="drop-paper">
    <button class="drop-btn" type="button"><span id="paper-label">全部卷</span><span class="chevron"></span></button>
  </div>
  <div class="drop" id="drop-type">
    <button class="drop-btn" type="button"><span id="type-label">全部题型</span><span class="chevron"></span></button>
  </div>
  <button id="btn-random">🎲 随机</button>
  <button id="btn-wrong">📕 错题</button>
  <button id="btn-fav">⭐ 收藏夹</button>
  <button class="btn-clear" id="btn-clear">🗑 清除记录</button>
</div>

<!-- 下拉面板放在 body 级（毛玻璃 backdrop-filter 不能嵌套在玻璃父元素内） -->
<div class="drop-panel" id="paper-panel">
  <div class="drop-opt selected" data-val="ALL">全部卷</div>
  <div class="drop-opt" data-val="A">卷A</div>
  <div class="drop-opt" data-val="B">卷B</div>
  <div class="drop-opt" data-val="C">卷C</div>
  <div class="drop-opt" data-val="D">卷D</div>
  <div class="drop-opt" data-val="E">卷E</div>
</div>
<div class="drop-panel" id="type-panel">
  <div class="drop-opt selected" data-val="ALL">全部题型</div>
  <div class="drop-opt" data-val="choice">选择题</div>
  <div class="drop-opt" data-val="judge">判断题</div>
  <div class="drop-opt" data-val="fill">填空题</div>
  <div class="drop-opt" data-val="short">简答题</div>
</div>

<div class="progress glass-liquid">
  <span id="p-pos">0/0</span>
  <div class="bar-wrap"><div class="bar" id="p-bar"></div></div>
  <span id="p-pct">0%</span>
</div>

<div id="quiz-area"></div>
<div id="empty" style="display:none;">
  🎉 没有题了！<br>
  <button onclick="resetProgress()">重置进度 / 清空错题</button>
</div>

<div class="stats glass-liquid" id="stats-row">
  <div class="stat"><div class="num" id="s-total">0</div><div class="lbl">已刷</div></div>
  <div class="stat"><div class="num" id="s-ok">0</div><div class="lbl">答对</div></div>
  <div class="stat"><div class="num" id="s-rate">0%</div><div class="lbl">正确率</div></div>
</div>

<footer>
  <div class="dock glass-liquid">
    <button class="btn-prev" id="btn-prev">◀ 上一题</button>
    <button class="btn-next" id="btn-next">下一题 ▶</button>
  </div>
</footer>

<script>
// ===== 数据（内嵌） =====
const QUESTIONS = __DATA__;

// ===== 状态管理（localStorage 持久化，file:// 下兼容降级） =====
const LS_KEY = "fire_quiz_v1";
// 部分安卓浏览器 file:// 下 localStorage 不可用（隐私模式/WebView），降级为内存态
let storageOk = true;
try {
  localStorage.setItem("__t", "1");
  localStorage.removeItem("__t");
} catch (e) {
  storageOk = false;
}
let state = {
  mode: "paper",        // paper | wrong | fav
  paper: "ALL",
  type: "ALL",
  shuffle: false,       // 随机 toggle 状态
  order: [],
  idx: 0,
  answered: {},
  wrongIds: [],
  favIds: [],
  totalAnswered: 0,
  totalOk: 0,
};
function loadState() {
  if (!storageOk) return;
  try { const s = localStorage.getItem(LS_KEY); if (s) state = Object.assign(state, JSON.parse(s)); } catch(e) {}
}
function saveState() {
  if (!storageOk) return;
  try { localStorage.setItem(LS_KEY, JSON.stringify(state)); } catch(e) {}
}
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
  if (state.mode === "fav") {
    const f = new Set(state.favIds);
    list = list.filter(x => f.has(qidOf(x.q, x.i)));
  }
  return list.map(x => x.i);
}

// ===== 渲染 =====
// animate: false=无动画直接替换; "qbody"=切题(内容层过渡); "card"=切模式(整卡离场入场); "empty"=空状态过渡
let _pendingRender = null;
function render(animate) {
  const area = document.getElementById("quiz-area");
  const empty = document.getElementById("empty");

  // 空状态处理（带离场/入场）
  if (!state.order.length) {
    const doEmpty = () => {
      area.innerHTML = "";
      empty.style.display = "block";
      empty.innerHTML = state.mode === "wrong"
        ? '🎉 没有错题了！<br><button onclick="resetProgress()">重置进度 / 清空错题</button>'
        : state.mode === "fav"
          ? '⭐ 收藏夹还是空的<br>在题目卡左上角点 ☆ 即可收藏<br><button onclick="resetProgress()">清空全部数据</button>'
          : '🎉 没有题了！<br><button onclick="resetProgress()">重置进度 / 清空错题</button>';
      document.getElementById("stats-row").style.display = "none";
    };
    // 空状态过渡：优先 View Transitions（交叉淡入淡出），降级为旧内容淡出
    const useVT = typeof document.startViewTransition === "function";
    if (animate && useVT) {
      document.startViewTransition(() => { doEmpty(); });
    } else if (animate && (area.querySelector(".card") || empty.style.display === "block")) {
      const target = area.querySelector(".card") ? area.querySelector(".card") : empty;
      target.classList.add("empty-leave");
      setTimeout(doEmpty, 160);
    } else {
      doEmpty();
    }
    return;
  }
  empty.style.display = "none";
  document.getElementById("stats-row").style.display = "grid";

  const i = state.order[state.idx];
  const q = QUESTIONS[i];
  const qid = qidOf(q, i);
  const answered = state.answered[qid];

  const done = Object.keys(state.answered).length;
  document.getElementById("p-pos").textContent = (state.idx+1) + "/" + state.order.length;
  document.getElementById("p-bar").style.width = ((state.idx+1)/state.order.length*100) + "%";
  document.getElementById("p-pct").textContent = Math.round(done/QUESTIONS.length*100) + "%";

  const typeName = {choice:"选择题", judge:"判断题", fill:"填空题", short:"简答题"}[q.type];
  const isFav = state.favIds.includes(qid);

  // 生成题目内容（不含卡片壳，供内容层动画复用）
  function buildBody() {
    let h = `<div class="q-head"><span class="crumb">卷<b>${q.paper}</b> · ${typeName} · 第 ${q.no} 题</span>`;
    h += `<button class="fav-btn ${isFav ? 'on' : ''}" onclick="toggleFav('${qid}')" title="${isFav ? '取消收藏' : '收藏本题'}">${isFav ? '★' : '☆'}</button>`;
    h += `<span class="tag" style="margin-left:auto;">${state.idx+1}/${state.order.length}</span></div>`;
    h += `<div class="q-stem">${escapeHtml(q.stem)}</div>`;
    if (q.type === "choice") {
      h += '<div class="opt-list">';
      q.options.forEach((opt) => {
        const letter = opt.match(/^([A-E])[.、]/);
        const cls = answered ? (letter && letter[1] === q.answer ? "correct" : (answered.my === letter[1] ? "wrong" : "")) : "";
        h += `<div class="opt ${cls}" onclick="answer('${qid}','${letter ? letter[1] : ""}')">${escapeHtml(opt)}</div>`;
      });
      h += '</div>';
    } else if (q.type === "judge") {
      h += '<div class="judge-row">';
      ["√","×"].forEach(v => {
        const cls = answered ? (v === q.answer ? "correct" : (answered.my === v ? "wrong" : "")) : "";
        h += `<div class="judge-btn ${cls}" onclick="answer('${qid}','${v}')">${v}</div>`;
      });
      h += '</div>';
    } else if (q.type === "fill") {
      h += `<input class="fill-input" id="fill-input" type="text" placeholder="请输入答案" value="${answered && answered.my ? escapeHtml(String(answered.my)) : ""}">`;
      h += `<button class="fill-submit" onclick="submitFill('${qid}')">${answered ? "重新提交" : "提交答案"}</button>`;
    } else {
      h += '<div class="short-ans"><button class="ans-toggle" onclick="toggleAns(this)"><span class="chev">▼</span>查看参考答案</button><div class="ans-wrap"><div><div class="ans-body">' + escapeHtml(q.answer) + '</div></div></div></div>';
      h += '<div class="self-row">';
      h += `<button class="self-btn self-no ${answered && answered.my === 'self-no' ? 'chosen' : ''}" onclick="answer('${qid}','self-no')">❌ 我没答对</button>`;
      h += `<button class="self-btn self-ok ${answered && answered.my === 'self-ok' ? 'chosen' : ''}" onclick="answer('${qid}','self-ok')">✅ 我答对了</button>`;
      h += '</div>';
    }
    if (answered && q.type !== "short") {
      const ok = answered.ok;
      h += `<div class="feedback show ${ok ? "ok" : "err"}">${ok ? "✅ 回答正确！" : "❌ 回答错误"}`;
      if (!ok) h += `<br>正确答案：<b>${escapeHtml(String(q.answer))}</b>`;
      h += '</div>';
    } else if (answered && q.type === "short" && answered.my) {
      const ok = answered.ok;
      h += `<div class="feedback show ${ok ? "ok" : "err"}">${ok ? "✅ 自评：答对了！" : "❌ 自评：没答对（已加入错题本）"}</div>`;
    }
    return h;
  }

  const doRender = () => {
    let html = '<div class="card glass-frost">';
    html += '<div class="q-body">';
    html += buildBody();
    html += '</div></div>';
    area.innerHTML = html;
    if (q.type === "fill" && !answered) {
      const inp = document.getElementById("fill-input");
      if (inp) inp.focus();
    }
    document.getElementById("s-total").textContent = state.totalAnswered;
    document.getElementById("s-ok").textContent = state.totalOk;
    document.getElementById("s-rate").textContent = state.totalAnswered ? Math.round(state.totalOk/state.totalAnswered*100) + "%" : "0%";
  };

  // 动画调度：优先 View Transitions API（交叉过渡，无空窗，大厂 fade-through 模式）
  const useVT = typeof document.startViewTransition === "function";
  if (animate && useVT) {
    // View Transitions：浏览器自动截取新旧快照交叉过渡（只对带 view-transition-name 的元素）
    document.startViewTransition(() => { doRender(); });
  } else if (animate === "qbody") {
    // 降级：切题（旧内容快速淡出 → 替换 → 新内容淡入）
    const oldBody = area.querySelector(".q-body");
    if (oldBody) {
      oldBody.classList.add("leaving");
      setTimeout(doRender, 150);
    } else {
      doRender();
    }
  } else if (animate === "card") {
    // 降级：切模式（整卡淡出 → 替换 → 淡入）
    const oldCard = area.querySelector(".card");
    if (oldCard) {
      oldCard.classList.add("card-leave");
      setTimeout(doRender, 150);
    } else {
      doRender();
    }
  } else {
    doRender();
  }
}

function escapeHtml(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

// ===== 答题（upsert 模式：可重复提交，统计/错题本保持一致） =====
function answer(qid, val) {
  const i = state.order[state.idx];
  const q = QUESTIONS[i];
  let ok;
  if (q.type === "short") ok = val === "self-ok";
  else ok = val === q.answer;
  record(qid, ok, val);
  render(false);
}
function submitFill(qid) {
  const val = document.getElementById("fill-input").value;
  const i = state.order[state.idx];
  const q = QUESTIONS[i];
  const ok = val.trim() === q.answer.trim();
  record(qid, ok, val.trim());
  render(false);
}
/**
 * 数据库式 upsert：已答过则更新记录（修正统计），未答过则插入
 * - 答对→答错：totalOk-1，加入错题本
 * - 答错→答对：totalOk+1，从错题本移除
 * - 未答→首次：totalAnswered+1
 */
function record(qid, ok, my) {
  const prev = state.answered[qid];
  if (prev) {
    // 更新已有记录：先撤销旧判定对统计的影响
    if (prev.ok && !ok) state.totalOk--;
    if (!prev.ok && ok) state.totalOk++;
    // 错题本同步
    if (!ok && !state.wrongIds.includes(qid)) state.wrongIds.push(qid);
    if (ok) state.wrongIds = state.wrongIds.filter(x => x !== qid);
  } else {
    // 首次作答
    state.totalAnswered++;
    if (ok) state.totalOk++;
    else state.wrongIds.push(qid);
  }
  state.answered[qid] = {ok, my};
  saveState();
  // 答对自动下一题（延迟 700ms 展示反馈；最后一题或空题序不跳）
  if (ok) {
    clearTimeout(state._autoNextTimer);
    const fromIdx = state.idx;   // 记录触发时位置，模式切换后不跳
    const fromOrder = state.order;
    state._autoNextTimer = setTimeout(() => {
      // 保护：仅当题序和位置都没变（用户没手动切换/跳题）才自动前进
      if (state.order === fromOrder && state.idx === fromIdx &&
          state.order.length && state.idx < state.order.length - 1) {
        state.idx++;
        saveState();
        render("qbody");
      }
    }, 700);
  }
}

// ===== 导航（切题带卡片动画） =====
function next() {
  clearTimeout(state._autoNextTimer);
  if (state.idx < state.order.length - 1) { state.idx++; saveState(); render("qbody"); }
}
function prev() {
  clearTimeout(state._autoNextTimer);
  if (state.idx > 0) { state.idx--; saveState(); render("qbody"); }
}

// ===== 自研液态玻璃下拉 =====
const DROP_META = {
  paper:  { label: "paper-label",  panel: "paper-panel",  key: "paper",  map: {"ALL":"全部卷", A:"卷A", B:"卷B", C:"卷C", D:"卷D", E:"卷E"} },
  type:   { label: "type-label",   panel: "type-panel",   key: "type",   map: {"ALL":"全部题型", choice:"选择题", judge:"判断题", fill:"填空题", short:"简答题"} },
};

function initDropdown(which) {
  const meta = DROP_META[which];
  const btn = document.querySelector(`#drop-${which} .drop-btn`);
  const panel = document.getElementById(meta.panel);
  const opts = panel.querySelectorAll(".drop-opt");

  function positionPanel() {
    const r = btn.getBoundingClientRect();
    // 面板宽度跟随按钮，手机窄屏时给足宽度保证选项可读
    let pw = Math.max(r.width, 140);
    if (window.innerWidth < 480) pw = Math.min(Math.max(r.width, window.innerWidth - 40), window.innerWidth - 20);
    panel.style.width = pw + "px";
    panel.style.left = Math.min(r.left, window.innerWidth - pw - 8) + "px";
    panel.style.top = (r.bottom + 6) + "px";
  }

  btn.addEventListener("click", e => {
    e.stopPropagation();
    const willOpen = !panel.classList.contains("show");
    // 关闭另一个下拉
    Object.keys(DROP_META).forEach(k => {
      if (k !== which) {
        document.getElementById(DROP_META[k].panel).classList.remove("show");
        document.querySelector(`#drop-${k} .drop-btn`).classList.remove("open");
      }
    });
    if (willOpen) positionPanel();
    panel.classList.toggle("show", willOpen);
    btn.classList.toggle("open", willOpen);
  });

  opts.forEach(opt => {
    opt.addEventListener("click", () => {
      const val = opt.dataset.val;
      state[meta.key] = val;
      state.mode = "paper"; state.idx = 0;
      state.shuffle = false;
      document.getElementById("btn-random").classList.remove("active");
      document.getElementById("btn-wrong").classList.remove("active");
      document.getElementById("btn-fav").classList.remove("active");
      state.order = filterQuestions();
      saveState();
      // 更新选中态
      document.getElementById(meta.label).textContent = meta.map[val] || val;
      opts.forEach(o => o.classList.toggle("selected", o === opt));
      // 先收起面板（动画完整跑完），再渲染内容——避免与 render 同帧打断收起动画
      panel.classList.remove("show");
      btn.classList.remove("open");
      setTimeout(() => render("card"), 280);
    });
  });
}
initDropdown("paper");
initDropdown("type");
// 滚动/缩放时同步已打开面板的位置
window.addEventListener("scroll", () => {
  document.querySelectorAll(".drop-panel.show").forEach(p => {
    const id = p.id === "paper-panel" ? "paper" : "type";
    const btn = document.querySelector(`#drop-${id} .drop-btn`);
    const r = btn.getBoundingClientRect();
    p.style.top = (r.bottom + 6) + "px";
  });
}, {passive: true});
window.addEventListener("resize", () => {
  document.querySelectorAll(".drop-panel.show").forEach(p => p.classList.remove("show"));
  document.querySelectorAll(".drop-btn.open").forEach(b => b.classList.remove("open"));
});
// 点击外部关闭下拉
document.addEventListener("click", e => {
  if (!e.target.closest(".drop")) {
    document.querySelectorAll(".drop-panel").forEach(p => p.classList.remove("show"));
    document.querySelectorAll(".drop-btn").forEach(b => b.classList.remove("open"));
  }
});
// 还原已保存的选择
function restoreDropdown() {
  Object.keys(DROP_META).forEach(which => {
    const meta = DROP_META[which];
    const cur = state[meta.key];
    document.getElementById(meta.label).textContent = meta.map[cur] || cur;
    const opts = document.getElementById(meta.panel).querySelectorAll(".drop-opt");
    opts.forEach(o => o.classList.toggle("selected", o.dataset.val === cur));
  });
}

document.getElementById("btn-random").onclick = () => {
  // 随机 toggle：再点一次恢复顺序
  state.shuffle = !state.shuffle;
  document.getElementById("btn-random").classList.toggle("active", state.shuffle);
  if (state.shuffle) {
    // 随机模式：只从未答题中抽取（已答过的不再出现）
    const list = filterQuestions().filter(i => !state.answered[qidOf(QUESTIONS[i], i)]);
    for (let i=list.length-1; i>0; i--) { const j=Math.floor(Math.random()*(i+1)); [list[i],list[j]]=[list[j],list[i]]; }
    state.order = list;
  } else {
    // 恢复顺序：全部题（含已答，便于回顾）
    state.order = filterQuestions();
  }
  state.idx = 0; saveState(); render("card");
};
document.getElementById("btn-wrong").onclick = () => {
  state.mode = state.mode === "wrong" ? "paper" : "wrong";
  state.shuffle = false;
  document.getElementById("btn-random").classList.remove("active");
  document.getElementById("btn-wrong").classList.toggle("active", state.mode === "wrong");
  document.getElementById("btn-fav").classList.remove("active");
  state.idx = 0; state.order = filterQuestions(); saveState(); render("card");
};
document.getElementById("btn-fav").onclick = () => {
  state.mode = state.mode === "fav" ? "paper" : "fav";
  state.shuffle = false;
  document.getElementById("btn-random").classList.remove("active");
  document.getElementById("btn-fav").classList.toggle("active", state.mode === "fav");
  document.getElementById("btn-wrong").classList.remove("active");
  state.idx = 0; state.order = filterQuestions(); saveState(); render("card");
};
document.getElementById("btn-clear").onclick = () => {
  if (!confirm("确定清除全部答题记录和错题？\\n（收藏不会清除）")) return;
  state.answered = {};
  state.wrongIds = [];
  state.totalAnswered = 0;
  state.totalOk = 0;
  saveState(); render("card");
};

function toggleFav(qid) {
  const i = state.favIds.indexOf(qid);
  if (i >= 0) state.favIds.splice(i, 1);
  else state.favIds.push(qid);
  saveState(); render(false);
}

// 简答题答案手风琴展开/收起
function toggleAns(btn) {
  btn.classList.toggle("open");
  const wrap = btn.nextElementSibling;
  if (wrap) wrap.classList.toggle("open");
}
document.getElementById("btn-next").onclick = next;
document.getElementById("btn-prev").onclick = prev;
document.addEventListener("keydown", e => {
  if (e.key === "ArrowRight" || e.key === "Enter") next();
  if (e.key === "ArrowLeft") prev();
});

function resetProgress() {
  if (!confirm("确定清除全部进度和错题记录？")) return;
  state = { mode:"paper", paper:"ALL", type:"ALL", shuffle:false, order:[], idx:0, answered:{}, wrongIds:[], favIds:[], totalAnswered:0, totalOk:0 };
  document.getElementById("btn-random").classList.remove("active");
  state.order = filterQuestions();
  saveState(); render("card");
}
window.resetProgress = resetProgress;

// ===== 启动 =====
loadState();
restoreDropdown();
// 还原随机 toggle 状态（持久化的 order 直接复用，否则按筛选生成）
if (state.shuffle && state.order.length) {
  document.getElementById("btn-random").classList.add("active");
} else {
  state.shuffle = false;
  state.order = filterQuestions();
}
render(false);
</script>
</body>
</html>
"""

html = html.replace("__DATA__", JS_DATA)
out = os.path.join(BASE, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"index.html v0.2 written: {out}, {os.path.getsize(out)/1024:.1f} KB")
