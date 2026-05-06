#!/usr/bin/env python3
import csv
import sys
from collections import Counter
from pathlib import Path

def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1]
    rows = list(csv.DictReader((root / "source_manifest" / "sources.csv").open(encoding="utf-8")))
    status_rows = list(csv.DictReader((root / "source_manifest" / "2025_67_texts_status.csv").open(encoding="utf-8")))
    fields = Counter(r["field"] for r in rows)
    statuses = Counter(r["source_status"] for r in rows)
    levels = Counter(r["authority_level"] for r in rows)
    true_count = sum(1 for r in rows if r["usable_for_generation"] == "true")
    completed_2025 = sum(1 for r in status_rows if r["download_status"] == "downloaded")
    risks = []
    if completed_2025 < 67:
        risks.append(f"2025示范文本附件正文未全部下载：{completed_2025}/67")
    if statuses["missing"]:
        risks.append(f"仍有missing记录：{statuses['missing']}")
    if fields["criminal"] < 35:
        risks.append("刑事文书覆盖不足")
    if fields["lawyer_practice"] < 35:
        risks.append("律师实务文书覆盖不足")
    print("总记录数:", len(rows))
    print("各field数量:", dict(fields))
    print("各source_status数量:", dict(statuses))
    print("各authority_level数量:", dict(levels))
    print("usable_for_generation=true数量:", true_count)
    print("official_collected数量:", statuses["official_collected"])
    print("guide_collected数量:", statuses["guide_collected"])
    print("missing数量:", statuses["missing"])
    print("criminal覆盖率:", f"{fields['criminal']}/35")
    print("lawyer_practice覆盖率:", f"{fields['lawyer_practice']}/35")
    print("2025年67类示范文本完成率:", f"{completed_2025}/67 downloaded; {len(status_rows)}/67 indexed")
    print("高风险缺口清单:", "；".join(risks) if risks else "无")
    if completed_2025 == 67:
        print("下一步建议: 抽查2025年67类Markdown拆分质量；补充经审定的律师实务内部模板。")
    else:
        print("下一步建议: 在可访问法院附件的网络环境中批量下载2025年doc/docx并转换Markdown；补充经审定的律师实务内部模板。")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
