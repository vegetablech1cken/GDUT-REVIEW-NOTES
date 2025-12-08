# 题库转换脚本
# 用途：将 "军事理论题库" 目录下的 .docx 题库文件转换为 Markdown 和 CSV 格式
# 说明：脚本采用启发式规则解析题目，可能无法覆盖所有格式。处理完成后会在源目录下生成 Markdown/ 和 CSV/ 子目录。

import os
import re
import pandas as pd
from docx import Document

INPUT_DIR = r"C:\Users\Admin\Desktop\Obsidian-Notes\GDUT-REVIEW-NOTES\广工学生手册考试答案"
MD_DIR = os.path.join(INPUT_DIR, "Markdown")
CSV_DIR = os.path.join(INPUT_DIR, "CSV")
os.makedirs(MD_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)

question_start_re = re.compile(r'^\s*\d+\s*[\.、\)）]')
option_re = re.compile(r'^\s*([A-D]|[A-D]、|\([A-D]\)|（[A-D]）|【([A-D])】)')
option_letter_re = re.compile(r'([A-D])')
answer_re = re.compile(r'答案[:：\s]*([A-D,，、\s]+|正确|错误|√|×|T|F|对|错)', re.IGNORECASE)


def split_lines_from_docx(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件不存在: {path}")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"无法读取文件: {path}")
    doc = Document(path)
    lines = []
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue
        # 保持原有换行分段
        for sub in text.splitlines():
            s = sub.strip()
            if s:
                lines.append(s)
    return lines


def process_block(block_lines):
    # block_lines: list of lines starting from question number to before next question
    q = {"question": "", "options": [], "answer": [], "type": "未知", "raw": "\n".join(block_lines)}
    # find indices of option lines
    opt_indices = []
    for i, ln in enumerate(block_lines):
        if re.match(r'^\s*[A-D][\.\、\)）\s]', ln) or re.match(r'^\s*（?[A-D]）?\s*[:：]?', ln) or re.match(r'^\s*[A-D]、', ln):
            opt_indices.append(i)
        else:
            # 有些格式是 A. 选项紧跟在题干后无换行（如：1. 问题 A.选项 B.选项）
            if re.search(r'\bA[\.、]\s*', ln):
                # 将行按 A. B. C. D. 切分
                parts = re.split(r'(?=\b[A-D][\.、])', ln)
                if len(parts) > 1:
                    # 替换原行为分割的多行
                    new_lines = [p.strip() for p in parts if p.strip()]
                    block_lines[i:i+1] = new_lines
                    return process_block(block_lines)  # 重新处理

    if opt_indices:
        first_opt = opt_indices[0]
        question_lines = block_lines[:first_opt]
        option_lines = block_lines[first_opt:]
    else:
        # 没有明显选项，整段作为题干，可能是判断或填空
        question_lines = block_lines
        option_lines = []

    q['question'] = ' '.join(question_lines).strip()

    # 解析选项
    opts = []
    for ln in option_lines:
        m = re.match(r'^\s*([A-D])[\.、\)）]?\s*(.*)$', ln)
        if m:
            letter = m.group(1)
            text = m.group(2).strip()
            opts.append((letter, text))
        else:
            # 如果不是标准前缀，尝试以 "X、文本" 形式
            m2 = re.match(r'^\s*([A-D])、\s*(.*)$', ln)
            if m2:
                opts.append((m2.group(1), m2.group(2).strip()))
            else:
                # 如果为续行，则附加到最后一个选项文本
                if opts:
                    opts[-1] = (opts[-1][0], opts[-1][1] + ' ' + ln)
                else:
                    # 无选项时跳过
                    pass

    # 排序并填充到 q['options'] 为 ["A. ...", ...]
    opts_sorted = sorted(opts, key=lambda x: x[0])
    q['options'] = [f"{k}. {v}" for k, v in opts_sorted]

    # 查找答案
    joined = '\n'.join(block_lines)
    am = answer_re.search(joined)
    if am:
        rawans = am.group(1)
        if any(x in rawans for x in ['正确', '对', '√', 'T']):
            q['type'] = '判断'
            q['answer'] = ['对']
        elif any(x in rawans for x in ['错误', '错', '×', 'F']):
            q['type'] = '判断'
            q['answer'] = ['错']
        else:
            letters = re.findall(r'[A-D]', rawans)
            letters = [l.upper() for l in letters]
            if len(letters) > 1:
                q['type'] = '多选'
            else:
                q['type'] = '单选'
            q['answer'] = letters
    else:
        # 尝试在末尾查找类似 "答案 A" 或单独一行 "A"
        for ln in reversed(block_lines):
            if re.match(r'^\s*[A-D](?:[,，、\s][A-D])*\s*$', ln):
                letters = re.findall(r'[A-D]', ln)
                q['answer'] = letters
                q['type'] = '多选' if len(letters) > 1 else '单选'
                break
            if ln.startswith('正确') or ln.startswith('错误') or ln.startswith('对') or ln.startswith('错'):
                q['type'] = '判断'
                q['answer'] = [ln.strip()]
                break

    # 若无选项但答案为判断类型，填充标准选项
    if not q['options'] and q['type'] == '判断':
        q['options'] = ['对', '错']

    # 最后若仍未识别类型，默认单选
    if q['type'] == '未知':
        if q['options']:
            q['type'] = '单选'
        else:
            q['type'] = '未知'

    return q


def parse_docx(path):
    lines = split_lines_from_docx(path)
    blocks = []
    cur = []
    for ln in lines:
        if question_start_re.match(ln):
            if cur:
                blocks.append(cur)
            cur = [ln]
        else:
            if cur:
                cur.append(ln)
            else:
                # 文件开头可能没有题号，尝试合并到上一个
                cur = [ln]
    if cur:
        blocks.append(cur)

    qs = []
    for b in blocks:
        try:
            q = process_block(b)
            qs.append(q)
        except (ValueError, IndexError, KeyError, AttributeError) as e:
            print(f'处理题目块失败 (行内容: {b[0][:50]}...): {e}')
    return qs


def save_md(qs, src_name, out_path):
    lines = [f'# {src_name}\n']
    for i, q in enumerate(qs, start=1):
        lines.append(f'{i}. {q["question"]}')
        for opt in q['options']:
            lines.append(f'- {opt}')
        # 将答案作为注释保留
        lines.append(f'<!-- 答案: {"、".join(q["answer"]) if q["answer"] else ""} 类型: {q["type"]} -->')
        lines.append('')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def save_csv(qs, src_name, out_path):
    rows = []
    for i, q in enumerate(qs, start=1):
        row = {
            'id': i,
            'source_file': src_name,
            'question': q['question'],
            'type': q['type'],
            'answer': '|'.join(q['answer']) if q['answer'] else '',
            'raw': q['raw']
        }
        for idx, opt in enumerate(q.get('options', [])):
            key = f'option_{chr(ord("A") + idx)}'
            row[key] = opt
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(out_path, index=False, encoding='utf-8-sig')
    return df


def main():
    all_qs = []
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.docx') and not f.startswith('~$')]
    if not files:
        print('未找到 .docx 文件，目录：', INPUT_DIR)
        return
    for fn in files:
        path = os.path.join(INPUT_DIR, fn)
        print('解析', fn)
        qs = parse_docx(path)
        if not qs:
            print('未解析出题目：', fn)
            continue
        md_path = os.path.join(MD_DIR, os.path.splitext(fn)[0] + '.md')
        csv_path = os.path.join(CSV_DIR, os.path.splitext(fn)[0] + '.csv')
        save_md(qs, fn, md_path)
        df = save_csv(qs, fn, csv_path)
        all_qs.extend(df.to_dict(orient='records'))

    # 汇总 CSV
    if all_qs:
        df_all = pd.DataFrame(all_qs)
        df_all.to_csv(os.path.join(CSV_DIR, 'all_questions.csv'), index=False, encoding='utf-8-sig')
        print('已生成汇总文件: all_questions.csv')
    print('处理完成。')

if __name__ == '__main__':
    main()
