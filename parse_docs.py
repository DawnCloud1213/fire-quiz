# -*- coding: utf-8 -*-
"""解析 5 份带答案卷 docx -> questions.json（供刷题小程序使用）"""
import os, re, json
from docx import Document

SRC = r"E:\JUST_DO_IT\Hermes-daily\消防试卷"
OUT = r"E:\JUST_DO_IT\消防刷题\questions.json"

def parse_paper(paper):
    path = os.path.join(SRC, f"卷{paper}_含答案.docx")
    doc = Document(path)
    questions = []
    mode = None
    cur = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # 题型标题
        if text.startswith("一、填空题"):
            mode = "fill"; continue
        if text.startswith("二、选择题"):
            mode = "choice"; continue
        if text.startswith("三、判断题"):
            mode = "judge"; continue
        if text.startswith("四、简答题"):
            mode = "short"; continue

        # 答案行（红色答案已经注入在题干后）: "答案：xxx" / "【答案：X】" / "参考答案：xxx"
        ans_match = re.search(r"(?:【?答案：|参考答案：)(.+)$", text)

        if mode == "fill":
            m = re.match(r"^(\d+)[.、]\s*(.*?)(?:\s*(?:【?答案：|参考答案：)(.+))?$", text)
            if m:
                num, stem, ans = m.group(1), m.group(2), (m.group(3) or "").strip()
                if cur and cur["type"] == "fill" and cur.get("answer") is None and not num:
                    pass
                questions.append({"paper": paper, "type": "fill", "no": int(num),
                                  "stem": stem.strip(), "answer": ans})
        elif mode == "choice":
            # 题干行: "1. xxx 【答案：C】"
            m = re.match(r"^(\d+)[.、]\s*(.*?)(?:\s*【答案：([A-E])】)?$", text)
            if m:
                num, stem, ans = m.group(1), m.group(2), (m.group(3) or "")
                q = {"paper": paper, "type": "choice", "no": int(num),
                     "stem": stem.strip(), "options": [], "answer": ans}
                questions.append(q)
                cur = q
                continue
            # 选项行: "A. xxx"
            om = re.match(r"^([A-E])[.、]\s*(.*)$", text)
            if om and cur and cur["type"] == "choice":
                cur["options"].append(text.strip())
        elif mode == "judge":
            m = re.match(r"^(\d+)[.、]\s*(.*?)(?:\s*答案：([√×]))?$", text)
            if m:
                num, stem, ans = m.group(1), m.group(2), (m.group(3) or "")
                questions.append({"paper": paper, "type": "judge", "no": int(num),
                                  "stem": stem.strip(), "answer": ans})
        elif mode == "short":
            m = re.match(r"^(\d+)[.、]\s*(.*)$", text)
            if m:
                questions.append({"paper": paper, "type": "short", "no": int(m.group(1)),
                                  "stem": m.group(2).strip(), "answer": ""})
            elif text.startswith("参考答案："):
                if questions and questions[-1]["type"] == "short" and not questions[-1]["answer"]:
                    questions[-1]["answer"] = text.replace("参考答案：", "").strip()

    return questions

all_q = []
for p in "ABCDE":
    qs = parse_paper(p)
    all_q.extend(qs)
    # 统计
    from collections import Counter
    c = Counter(q["type"] for q in qs)
    print(f"卷{p}: {len(qs)}题 {dict(c)}")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(all_q, f, ensure_ascii=False, indent=1)
print(f"\n总计 {len(all_q)} 题 -> {OUT}")

# 完整性检查：每卷每题型数量
for p in "ABCDE":
    qs = [q for q in all_q if q["paper"] == p]
    missing = []
    for q in qs:
        if q["type"] in ("fill", "judge") and not q["answer"]:
            missing.append(f"fill/judge#{q['no']} 无答案")
        if q["type"] == "choice" and (not q["answer"] or len(q["options"]) < 2):
            missing.append(f"choice#{q['no']} 选项/答案缺失")
        if q["type"] == "short" and not q["answer"]:
            missing.append(f"short#{q['no']} 无参考答案")
    print(f"卷{p} 检查: {'OK' if not missing else missing}")
