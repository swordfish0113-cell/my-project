#!/usr/bin/env python3
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RETRIEVED_AT = "2026-05-02"


LEGACY_TEMPLATES = [
    {
        "source": "references/court-civil-procedure/civil-complaint-individual.md",
        "target": "assets/official_templates/civil/spc-2016-civil-complaint-individual.md",
        "title": "民事起诉状（公民提起民事诉讼用）",
        "document_type": "民事诉讼文书样式",
        "field": "civil",
        "intended_author": "party",
        "usable_for_generation": "true",
        "authority_level": "A",
        "issuing_authority": "中华人民共和国最高人民法院",
        "source_url": "https://www.court.gov.cn/susongyangshi/xiangqing/181.html",
        "publish_date": "2016-09-28",
        "source_status": "official_collected",
        "notes": "可作为律师/当事人提交文书模板；由旧 references 文件机械迁移，未改写官方正文。",
    },
    {
        "source": "references/court-civil-procedure/civil-complaint-organization.md",
        "target": "assets/official_templates/civil/spc-2016-civil-complaint-organization.md",
        "title": "民事起诉状（法人或者其他组织提起民事诉讼用）",
        "document_type": "民事诉讼文书样式",
        "field": "civil",
        "intended_author": "party",
        "usable_for_generation": "true",
        "authority_level": "A",
        "issuing_authority": "中华人民共和国最高人民法院",
        "source_url": "https://www.court.gov.cn/susongyangshi/xiangqing/187.html",
        "publish_date": "2016-09-28",
        "source_status": "official_collected",
        "notes": "可作为律师/当事人提交文书模板；由旧 references 文件机械迁移，未改写官方正文。",
    },
    {
        "source": "references/court-civil-procedure/civil-answer-individual.md",
        "target": "assets/official_templates/civil/spc-2016-civil-answer-individual.md",
        "title": "民事答辩状（公民对民事起诉提出答辩用）",
        "document_type": "民事诉讼文书样式",
        "field": "civil",
        "intended_author": "party",
        "usable_for_generation": "true",
        "authority_level": "A",
        "issuing_authority": "中华人民共和国最高人民法院",
        "source_url": "https://www.court.gov.cn/susongyangshi/xiangqing/216.html",
        "publish_date": "2016-09-28",
        "source_status": "official_collected",
        "notes": "可作为律师/当事人提交文书模板；由旧 references 文件机械迁移，未改写官方正文。",
    },
    {
        "source": "references/court-civil-procedure/civil-appeal.md",
        "target": "assets/official_templates/civil/spc-2016-civil-appeal.md",
        "title": "民事上诉状（当事人提起上诉用）",
        "document_type": "民事诉讼文书样式",
        "field": "civil",
        "intended_author": "party",
        "usable_for_generation": "true",
        "authority_level": "A",
        "issuing_authority": "中华人民共和国最高人民法院",
        "source_url": "https://www.court.gov.cn/susongyangshi/xiangqing/379.html",
        "publish_date": "2016-09-28",
        "source_status": "official_collected",
        "notes": "可作为律师/当事人提交文书模板；由旧 references 文件机械迁移，未改写官方正文。",
    },
    {
        "source": "references/court-civil-procedure/property-preservation-pre-litigation.md",
        "target": "assets/official_templates/civil/spc-2016-property-preservation-pre-litigation.md",
        "title": "申请书（诉前或者仲裁前申请财产保全用）",
        "document_type": "民事诉讼文书样式",
        "field": "civil",
        "intended_author": "party",
        "usable_for_generation": "true",
        "authority_level": "A",
        "issuing_authority": "中华人民共和国最高人民法院",
        "source_url": "https://www.court.gov.cn/susongyangshi/xiangqing/113.html",
        "publish_date": "2016-09-28",
        "source_status": "official_collected",
        "notes": "可作为律师/当事人提交文书模板；由旧 references 文件机械迁移，未改写官方正文。",
    },
    {
        "source": "references/court-civil-procedure/property-preservation-litigation.md",
        "target": "assets/official_templates/civil/spc-2016-property-preservation-litigation.md",
        "title": "申请书（申请诉讼财产保全用）",
        "document_type": "民事诉讼文书样式",
        "field": "civil",
        "intended_author": "party",
        "usable_for_generation": "true",
        "authority_level": "A",
        "issuing_authority": "中华人民共和国最高人民法院",
        "source_url": "https://www.court.gov.cn/susongyangshi/xiangqing/126.html",
        "publish_date": "2016-09-28",
        "source_status": "official_collected",
        "notes": "可作为律师/当事人提交文书模板；由旧 references 文件机械迁移，未改写官方正文。",
    },
    {
        "source": "references/court-civil-procedure/enforcement-application.md",
        "target": "assets/official_templates/enforcement/spc-2016-enforcement-application.md",
        "title": "申请书（申请执行用）",
        "document_type": "民事执行文书样式",
        "field": "enforcement",
        "intended_author": "party",
        "usable_for_generation": "true",
        "authority_level": "A",
        "issuing_authority": "中华人民共和国最高人民法院",
        "source_url": "https://www.court.gov.cn/susongyangshi/xiangqing/639.html",
        "publish_date": "2016-09-28",
        "source_status": "official_collected",
        "notes": "可作为律师/当事人提交文书模板；由旧 references 文件机械迁移，未改写官方正文。",
    },
    {
        "source": "references/court-civil-procedure/service-address-confirmation.md",
        "target": "assets/official_templates/civil/spc-2016-service-address-confirmation.md",
        "title": "送达地址确认书（确认送达地址用）",
        "document_type": "民事诉讼文书样式",
        "field": "civil",
        "intended_author": "party",
        "usable_for_generation": "true",
        "authority_level": "A",
        "issuing_authority": "中华人民共和国最高人民法院",
        "source_url": "https://www.court.gov.cn/susongyangshi/xiangqing/378.html",
        "publish_date": "2016-09-28",
        "source_status": "official_collected",
        "notes": "可作为律师/当事人提交文书模板；由旧 references 文件机械迁移，未改写官方正文。",
    },
    {
        "source": "references/court-civil-procedure/power-of-attorney-individual.md",
        "target": "assets/official_templates/lawyer_practice/spc-2016-power-of-attorney-individual.md",
        "title": "授权委托书（公民委托诉讼代理人用）",
        "document_type": "诉讼代理授权文书样式",
        "field": "lawyer_practice",
        "intended_author": "party",
        "usable_for_generation": "true",
        "authority_level": "A",
        "issuing_authority": "中华人民共和国最高人民法院",
        "source_url": "https://www.court.gov.cn/susongyangshi/xiangqing/51.html",
        "publish_date": "2016-09-28",
        "source_status": "official_collected",
        "notes": "可作为律师/当事人提交文书模板；由旧 references 文件机械迁移，未改写官方正文。",
    },
    {
        "source": "references/court-civil-procedure/power-of-attorney-organization.md",
        "target": "assets/official_templates/lawyer_practice/spc-2016-power-of-attorney-organization.md",
        "title": "授权委托书（法人或者其他组织委托诉讼代理人用）",
        "document_type": "诉讼代理授权文书样式",
        "field": "lawyer_practice",
        "intended_author": "party",
        "usable_for_generation": "true",
        "authority_level": "A",
        "issuing_authority": "中华人民共和国最高人民法院",
        "source_url": "https://www.court.gov.cn/susongyangshi/xiangqing/59.html",
        "publish_date": "2016-09-28",
        "source_status": "official_collected",
        "notes": "可作为律师/当事人提交文书模板；由旧 references 文件机械迁移，未改写官方正文。",
    },
]

GUIDES = [
    {
        "target": "references/official_rules/spc-2025-demonstration-texts-release.md",
        "title": "2025年部分案件起诉状答辩状示范文本发布说明",
        "document_type": "官方发布说明",
        "field": "other",
        "intended_author": "other",
        "usable_for_generation": "false",
        "authority_level": "A",
        "issuing_authority": "最高人民法院、司法部、中华全国律师协会",
        "source_url": "https://www.court.gov.cn/fabu/xiangqing/468671.html",
        "publish_date": "2025-06-23",
        "source_status": "guide_collected",
        "notes": "最高法官网确认67类示范文本及2025年7月14日起全国推广；本地未成功下载官方附件，不能作为模板正文。",
        "body": "该官方发布页确认《部分案件起诉状答辩状示范文本》覆盖刑事（自诉）、民事、商事、知识产权、海事、行政、环境资源、国家赔偿、执行等9个领域、合计67类常见多发纠纷，并定于2025年7月14日起在全国法院全面推广使用。\n\n本文件仅作来源说明。未取得附件正文前，不得把67类示范文本条目当作已收集模板使用。",
    },
    {
        "target": "references/source_notes/sdcourt-2025-execution-demonstration-index.md",
        "title": "67类起诉状、答辩状空白示范文本及实例-执行",
        "document_type": "地方法院示范文本下载索引",
        "field": "enforcement",
        "intended_author": "party",
        "usable_for_generation": "false",
        "authority_level": "C",
        "issuing_authority": "济南市中级人民法院网站",
        "source_url": "https://www.sdcourt.gov.cn/jinanzy/376241/376175/376727/41779668/index.html",
        "publish_date": "2025-07-10",
        "source_status": "guide_collected",
        "notes": "页面列明执行领域9类docx下载项；当前环境未成功下载附件正文，不能作为正式模板正文。",
        "body": "页面列明：确认优先购买权申请书、暂时解除乘坐飞机高铁限制措施申请书、执行监督申请书、执行担保申请书、执行异议申请书、执行复议申请书、强制执行申请书、参与分配申请书、不予执行仲裁裁决调解书或公证债权文书申请书。\n\n本文件仅作下载索引和后续补收提示。",
    },
]

CRIMINAL_GUIDES = [
    ("取保候审申请书", "bail-pending-trial-application.md"),
    ("变更强制措施申请书", "change-coercive-measure-application.md"),
    ("羁押必要性审查申请书", "custody-necessity-review-application.md"),
    ("阅卷申请书", "case-file-review-application.md"),
    ("会见申请书", "detention-meeting-application.md"),
    ("调取证据申请书", "evidence-collection-application.md"),
    ("证人出庭申请书", "witness-appearance-application.md"),
    ("鉴定申请书", "appraisal-application.md"),
    ("非法证据排除申请书", "illegal-evidence-exclusion-application.md"),
    ("刑事自诉状", "criminal-private-prosecution-complaint.md"),
    ("刑事附带民事起诉状", "criminal-incidental-civil-complaint.md"),
    ("辩护词", "criminal-defense-statement.md"),
]

LAWYER_GUIDES = [
    ("法律意见书", "references/lawyer_practice_guides/legal-opinion-guide.md", "律师事务所从事证券法律业务管理办法", "https://www.moj.gov.cn/pub/sfbgw/flfggz/flfggzbmgz/202409/t20240905_505346.html", "2023-10-26", "A"),
    ("尽职调查报告", "references/lawyer_practice_guides/due-diligence-report-guide.md", "并购业务法律尽职调查的原则与方法", "https://2019.acla.org.cn/info/b8441f86f9b341af861129509eb895aa", "2022-02-23", "B"),
    ("合同审查意见", "references/lawyer_practice_guides/contract-review-opinion-guide.md", "律师办理买卖合同法律事务操作指引", "https://www.acla.org.cn/info/babca008c2ba43e9829b3192ed5f13a9", "2017-11-16", "B"),
    ("代理词", "references/lawyer_practice_guides/representation-statement-guide.md", "律师办理婚姻家庭法律业务操作指引", "https://www.acla.org.cn/info/db55cc94958f4f8eaebeae94e37a77a5", "2017-11-16", "B"),
    ("质证意见", "references/lawyer_practice_guides/cross-examination-opinion-guide.md", "律师承办海商海事案件业务操作指引", "https://www.acla.org.cn/info/dd085166c6ba4f4991a0551944c2cd31", "2017-11-16", "B"),
    ("证据目录", "references/lawyer_practice_guides/evidence-list-guide.md", "律师承办海商海事案件业务操作指引", "https://www.acla.org.cn/info/dd085166c6ba4f4991a0551944c2cd31", "2017-11-16", "B"),
]


def body_without_legacy_header(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].startswith("文书名称："):
        return "\n".join(lines[9:]).lstrip() + "\n"
    return path.read_text(encoding="utf-8")


def write_markdown(path: Path, metadata: dict, body: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    local_path = f"skills/legal-document-drafting/{path.relative_to(ROOT).as_posix()}"
    metadata = {**metadata, "retrieved_at": RETRIEVED_AT, "local_path": local_path}
    frontmatter = "\n".join(f"{key}: {value}" for key, value in metadata.items() if key != "source_status")
    path.write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8")
    return local_path


def main():
    rows = []

    for item in LEGACY_TEMPLATES:
        source_path = ROOT / item["source"]
        target_path = ROOT / item["target"]
        body = body_without_legacy_header(source_path)
        local_path = write_markdown(target_path, item, body)
        rows.append({**item, "retrieved_at": RETRIEVED_AT, "local_path": local_path})

    for item in GUIDES:
        target_path = ROOT / item["target"]
        local_path = write_markdown(target_path, item, item["body"] + "\n")
        rows.append({**item, "retrieved_at": RETRIEVED_AT, "local_path": local_path})

    criminal_source_url = "https://www.npc.gov.cn/npc/c2/c12435/201905/t20190521_276591.html"
    custody_url = "https://www.spp.gov.cn/spp/zdgz/201602/t20160202_112046.shtml"
    for title, filename in CRIMINAL_GUIDES:
        target_path = ROOT / "references" / "criminal_defense_guides" / filename
        source_url = custody_url if title == "羁押必要性审查申请书" else criminal_source_url
        metadata = {
            "title": title,
            "document_type": "刑事文书起草依据",
            "field": "criminal",
            "intended_author": "lawyer",
            "usable_for_generation": "false",
            "authority_level": "A",
            "issuing_authority": "全国人民代表大会或最高人民检察院",
            "source_url": source_url,
            "publish_date": "2018-11-05" if source_url == criminal_source_url else "2016-02-02",
            "source_status": "guide_collected",
            "notes": "未找到官方固定模板；本文件仅记录权威法律依据/办事规则，起草时需标注缺少权威模板并由律师复核。",
        }
        body = f"# {title}\n\n未收录官方固定模板。起草时只能依据用户事实、现行刑事诉讼规则和本 skill 的刑事特别规则形成草稿。\n\n必须提示：缺少权威模板，需律师复核。\n"
        local_path = write_markdown(target_path, metadata, body)
        rows.append({**metadata, "retrieved_at": RETRIEVED_AT, "local_path": local_path})

    for title, target, source_name, source_url, publish_date, level in LAWYER_GUIDES:
        metadata = {
            "title": title,
            "document_type": "律师实务文书起草依据",
            "field": "lawyer_practice",
            "intended_author": "lawyer",
            "usable_for_generation": "false",
            "authority_level": level,
            "issuing_authority": "司法部或中华全国律师协会",
            "source_url": source_url,
            "publish_date": publish_date,
            "source_status": "guide_collected",
            "notes": f"来源为{source_name}；未作为统一模板，仅供执业规则和结构要点参考。",
        }
        body = f"# {title}\n\n本文件记录权威或相对权威来源中的业务规则线索，不是统一模板。\n\n来源依据：{source_name}。\n\n起草时应结合委托目的、事实材料、证据范围、核验过程、风险揭示和律师执业规范审慎处理。\n"
        local_path = write_markdown(ROOT / target, metadata, body)
        rows.append({**metadata, "retrieved_at": RETRIEVED_AT, "local_path": local_path})

    missing_path = "skills/legal-document-drafting/source_manifest/missing_sources.md"
    for title, field in [
        ("2025年67类示范文本附件正文逐类Markdown拆分", "other"),
        ("不予批准逮捕法律意见书", "criminal"),
        ("认罪认罚具结书审查意见", "criminal"),
        ("律师函", "lawyer_practice"),
        ("律师见证书", "lawyer_practice"),
        ("类案检索报告", "lawyer_practice"),
        ("仲裁申请书", "lawyer_practice"),
        ("劳动仲裁申请书", "lawyer_practice"),
    ]:
        rows.append(
            {
                "title": title,
                "document_type": "待补权威模板",
                "field": field,
                "intended_author": "lawyer",
                "usable_for_generation": "false",
                "authority_level": "A",
                "issuing_authority": "待核验",
                "source_url": "missing - see missing_sources.md",
                "publish_date": "unknown",
                "retrieved_at": RETRIEVED_AT,
                "local_path": missing_path,
                "source_status": "missing",
                "notes": "未找到可纳入 official_templates 的权威模板正文；不得使用非官方范文替代。",
            }
        )

    manifest = ROOT / "source_manifest" / "sources.csv"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "title",
        "document_type",
        "field",
        "intended_author",
        "usable_for_generation",
        "authority_level",
        "issuing_authority",
        "source_url",
        "publish_date",
        "retrieved_at",
        "local_path",
        "source_status",
        "notes",
    ]
    with manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in fieldnames})

    print(f"Wrote {len(rows)} manifest rows")


if __name__ == "__main__":
    main()
