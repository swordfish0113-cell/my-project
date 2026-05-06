#!/usr/bin/env python3
import csv
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

OFFICIAL_SOURCE_URL = "https://www.court.gov.cn/fabu/xiangqing/468671.html"
ISSUING_AUTHORITY = "最高人民法院、司法部、中华全国律师协会"
PUBLISH_DATE = "2025-06-23"


def safe_name(value):
    return (
        value.replace("/", "-")
        .replace("\\", "-")
        .replace("、", "-")
        .replace("，", "-")
        .replace(",", "-")
        .replace("：", "-")
        .replace(":", "-")
        .replace(" ", "")
    )


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, fieldnames):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def convert_docx_to_lines(docx_path):
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "converted.txt"
        subprocess.run(
            ["textutil", "-convert", "txt", "-output", str(out), str(docx_path)],
            check=True,
        )
        return out.read_text(encoding="utf-8", errors="ignore").splitlines()


def find_body_start(lines):
    for idx in range(len(lines) - 1):
        if lines[idx].strip() == "刑事（附带民事）自诉状" and lines[idx + 1].strip() == "（侮辱案）":
            return idx
    raise RuntimeError("未找到正文起点：刑事（附带民事）自诉状（侮辱案）")


def previous_non_empty(lines, idx, floor):
    pos = idx - 1
    while pos >= floor and not lines[pos].strip():
        pos -= 1
    if pos < floor:
        raise RuntimeError(f"无法定位标题行：{idx}")
    return pos


def build_starts(lines, status_rows):
    body_start = find_body_start(lines)
    starts = {}
    by_seq = {int(row["sequence"]): row for row in status_rows}

    for row in status_rows:
        seq = int(row["sequence"])
        case_type = row["case_type"]
        if seq == 51 or seq >= 59:
            continue
        target = f"（{case_type}）"
        for idx in range(body_start, len(lines)):
            if lines[idx].strip() == target:
                starts[seq] = previous_non_empty(lines, idx, body_start)
                break
        if seq not in starts:
            raise RuntimeError(f"未找到第{seq}类正文起点：{case_type}")

    # 第51类是通用行政答辩状，正文标题没有括号案由。
    for idx in range(starts[50] + 1, len(lines)):
        if lines[idx].strip() == "行政答辩状":
            preview = "|".join(part.strip() for part in lines[idx + 1 : idx + 8] if part.strip())
            if "说明" in preview:
                starts[51] = idx
                break
    if 51 not in starts:
        raise RuntimeError("未找到第51类行政答辩状正文起点")

    cursor = starts[58]
    for seq in range(59, 67):
        case_type = by_seq[seq]["case_type"]
        for idx in range(cursor + 1, len(lines)):
            if lines[idx].strip() == case_type:
                starts[seq] = idx
                cursor = idx
                break
        if seq not in starts:
            raise RuntimeError(f"未找到第{seq}类执行文书正文起点：{case_type}")

    # 第67类正文标题为“不予执行申请书”，副标题说明适用对象。
    for idx in range(cursor + 1, len(lines)):
        if lines[idx].strip() == "不予执行申请书":
            starts[67] = idx
            break
    if 67 not in starts:
        raise RuntimeError("未找到第67类不予执行申请书正文起点")

    return starts


def trim_blank(lines):
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def render_markdown(row, body_lines, local_path, original_docx_rel, retrieved_at):
    title = f"2025年示范文本：{row['case_type']}"
    body = "\n".join(trim_blank(body_lines))
    return f"""---
title: {title}
document_type: 部分案件起诉状答辩状示范文本
field: {row['field']}
intended_author: party
usable_for_generation: true
authority_level: A
issuing_authority: {ISSUING_AUTHORITY}
source_url: {OFFICIAL_SOURCE_URL}
publish_date: {PUBLISH_DATE}
retrieved_at: {retrieved_at}
local_path: {local_path}
source_status: official_collected
source_file: {original_docx_rel}
notes: 用户提供《最高人民法院、司法部、中华全国律师协会关于印发部分案件起诉状答辩状示范文本的通知（法〔2025〕82号）》DOCX；正文由本地 textutil 转换后按67类拆分，未改写官方模板实质内容；文件含空白模板及实例。该模板为要素式/表格式文本，默认仅作要素核对和结构参考；只有用户明确要求要素式或按2025示范文本填写时才直接用于该形态生成。传统诉状默认应转换为叙述式正文并由律师复核。
---

# {title}

> 来源说明：本文件从用户提供的法〔2025〕82号 DOCX 原件拆分整理；以下为转换后的官方模板正文，包含空白模板与实例。该文本为要素式/表格式文本，默认仅作要素核对和结构参考；实例仅供结构参考，生成正式文书时不得把实例事实写入用户文书。用户未明确要求要素式时，应生成传统叙述式诉状或答辩状。

## 官方模板正文

{body}
"""


def update_markdown_notes(path, old, new):
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace(old, new), encoding="utf-8")


def update_reports(root, retrieved_at):
    missing = root / "source_manifest" / "missing_sources.md"
    text = missing.read_text(encoding="utf-8")
    section = """## 2025年67类示范文本附件正文下载

已检索来源：最高法、最高检、司法部、中国政府网、全国人大、全国律协、贸仲或人社部等权威来源。当前未取得可纳入正式模板库的统一模板正文；不得使用普通网站范文替代，后续需人工下载官方附件或补充经审定内部模板。

"""
    text = text.replace(section, "")
    missing.write_text(text, encoding="utf-8")

    report = root / "source_manifest" / "collection_report.md"
    report_text = report.read_text(encoding="utf-8")
    report_text = report_text.replace(
        "- official_collected：10\n- official_reference_only：86\n- guide_collected：146",
        "- official_collected：77\n- official_reference_only：19\n- guide_collected：146",
    )
    report_text = report_text.replace(
        "已逐类建立 67 条状态记录和单独 Markdown 文件。当前本地网络访问法院站点附件时出现 TLS 连接失败，因此未把附件正文标记为已收集；所有 67 条均为 reference-only，需人工或可用网络环境继续下载核验。",
        "已根据用户提供的《最高人民法院、司法部、中华全国律师协会关于印发部分案件起诉状答辩状示范文本的通知（法〔2025〕82号）》DOCX 原件完成 67 类逐类拆分。每类均已写入 assets/official_templates/ 对应领域目录，source_status 更新为 official_collected，并保留原始 DOCX。",
    )
    report.write_text(report_text, encoding="utf-8")

    release = root / "references" / "official_rules" / "spc-2025-demonstration-texts-release.md"
    release_text = release.read_text(encoding="utf-8")
    release_text = release_text.replace(
        "notes: 最高法官网确认67类示范文本及2025年7月14日起全国推广；本地未成功下载官方附件，不能作为模板正文。",
        "notes: 最高法官网确认67类示范文本及2025年7月14日起全国推广；已根据用户提供的法〔2025〕82号DOCX原件拆分正文。",
    )
    release_text = release_text.replace(
        "本文件仅作来源说明。未取得附件正文前，不得把67类示范文本条目当作已收集模板使用。",
        f"本文件为来源说明。{retrieved_at} 已根据用户提供的法〔2025〕82号 DOCX 原件将67类示范文本拆分进入正式模板库；具体路径见 source_manifest/2025_67_texts_status.csv。",
    )
    release.write_text(release_text, encoding="utf-8")

    index = root / "references" / "official_rules" / "2025_67_demonstration_texts_index.md"
    update_markdown_notes(
        index,
        "本地逐类状态以 `source_manifest/2025_67_texts_status.csv` 为准。当前附件下载因 TLS 连接失败未完成，已按类建立 reference-only 文件。",
        "本地逐类状态以 `source_manifest/2025_67_texts_status.csv` 为准。已根据用户提供的法〔2025〕82号 DOCX 原件完成 67 类正文拆分，正式模板位于 `assets/official_templates/` 对应领域目录。",
    )


def main(argv):
    if len(argv) < 3:
        print("usage: import_2025_67_from_docx.py <skill-root> <source-docx>", file=sys.stderr)
        return 2
    root = Path(argv[1]).resolve()
    docx_path = Path(argv[2]).resolve()
    retrieved_at = date.today().isoformat()

    status_path = root / "source_manifest" / "2025_67_texts_status.csv"
    sources_path = root / "source_manifest" / "sources.csv"
    status_rows = read_csv(status_path)
    sources_rows = read_csv(sources_path)
    status_fields = list(status_rows[0].keys())
    sources_fields = list(sources_rows[0].keys())

    lines = convert_docx_to_lines(docx_path)
    starts = build_starts(lines, status_rows)
    ordered_starts = sorted(starts.items(), key=lambda item: item[1])
    end_by_seq = {}
    for index, (seq, start) in enumerate(ordered_starts):
        end_by_seq[seq] = ordered_starts[index + 1][1] if index + 1 < len(ordered_starts) else len(lines)

    original_dir = root / "assets" / "official_templates" / "2025_demonstration_texts" / "original"
    original_dir.mkdir(parents=True, exist_ok=True)
    original_name = "fa-2025-82-demonstration-texts.docx"
    original_dest = original_dir / original_name
    shutil.copy2(docx_path, original_dest)
    original_rel = "skills/legal-document-drafting/assets/official_templates/2025_demonstration_texts/original/" + original_name

    local_by_seq = {}
    for row in status_rows:
        seq = int(row["sequence"])
        filename = f"2025-67-{seq:02d}-{safe_name(row['case_type'])}.md"
        rel = f"skills/legal-document-drafting/assets/official_templates/{row['field']}/{filename}"
        target = root.parent.parent / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        markdown = render_markdown(row, lines[starts[seq] : end_by_seq[seq]], rel, original_rel, retrieved_at)
        target.write_text(markdown, encoding="utf-8")
        local_by_seq[str(seq)] = rel

        row["blank_template_url"] = OFFICIAL_SOURCE_URL
        row["example_template_url"] = OFFICIAL_SOURCE_URL
        row["source_page_url"] = OFFICIAL_SOURCE_URL
        row["download_status"] = "downloaded"
        row["local_blank_path"] = rel
        row["local_example_path"] = rel
        row["failure_reason"] = ""
        row["notes"] = "已从用户提供的法〔2025〕82号官方DOCX拆分正文；同一Markdown文件含空白模板和实例；原始DOCX已保留；默认作为传统诉状起草的要素核对表，只有用户明确要求要素式时才直接按该形态输出。"

    updated_sources = []
    status_by_case = {row["case_type"]: row for row in status_rows}
    for row in sources_rows:
        if row["title"] == "2025年67类示范文本附件正文下载":
            continue
        if row["title"].startswith("2025年示范文本："):
            case_type = row["title"].split("：", 1)[1]
            status_row = status_by_case[case_type]
            row["usable_for_generation"] = "true"
            row["authority_level"] = "A"
            row["issuing_authority"] = ISSUING_AUTHORITY
            row["source_url"] = OFFICIAL_SOURCE_URL
            row["publish_date"] = PUBLISH_DATE
            row["retrieved_at"] = retrieved_at
            row["local_path"] = status_row["local_blank_path"]
            row["source_status"] = "official_collected"
            row["notes"] = "已从用户提供的法〔2025〕82号官方DOCX拆分正文；含空白模板和实例；该模板为要素式/表格式文本，默认用于核对要素，不作为传统诉状的默认输出形态；只有用户明确要求要素式时才直接按该结构生成；正式生成需律师复核。"
        updated_sources.append(row)

    write_csv(status_path, status_rows, status_fields)
    write_csv(sources_path, updated_sources, sources_fields)
    update_reports(root, retrieved_at)
    print(f"imported {len(status_rows)} demonstration-text entries from {docx_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
