#!/usr/bin/env python3
import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RETRIEVED_AT = "2026-05-02"
SPC_2025_RELEASE = "https://www.court.gov.cn/fabu/xiangqing/468671.html"
SPC_2025_GAZETTE = "https://gongbao.court.gov.cn/Details/58f1a4cb9bbdcc45faa565a6e0db5b.html"
SDCOURT_2025_PARTIAL = "https://www.sdcourt.gov.cn/dzpyfy/393147/393148/393150/43509906/index.html"
JINAN_EXECUTION_INDEX = "https://www.sdcourt.gov.cn/jinanzy/376241/376175/376727/41779668/index.html"
NPC_CRIMINAL_PROCEDURE = "https://www.npc.gov.cn/npc/c2/c12435/201905/t20190521_276591.html"
SPP_CUSTODY_REVIEW = "https://www.spp.gov.cn/spp/zdgz/201602/t20160202_112046.shtml"
GOV_SECURITIES_LEGAL = "https://www.gov.cn/gongbao/2023/issue_10886/202312/content_6921379.html"
CIETAC_APPLICATION = "https://www.cietac.org/articles/8324"
CIETAC_RULES = "https://www.cietac.org/articles/25022"
MOHRSS_ARBITRATION_RULES = "https://chinajob.mohrss.gov.cn/h5/c/2022-07-15/356204.shtml"
ACLA_MARRIAGE = "https://www.acla.org.cn/info/db55cc94958f4f8eaebeae94e37a77a5"
ACLA_PATENT = "https://acla.org.cn/info/505ba22a0d2d4b8fb8c30f63c1192ed7"
ACLA_DD = "https://2019.acla.org.cn/info/b8441f86f9b341af861129509eb895aa"
ACLA_SALE = "https://www.acla.org.cn/info/babca008c2ba43e9829b3192ed5f13a9"
ACLA_MARITIME = "https://www.acla.org.cn/info/dd085166c6ba4f4991a0551944c2cd31"
COURT_2016_ORDINARY = "https://www.court.gov.cn/susongyangshi/75.html"
COURT_2016_PUBLIC_INTEREST = "https://www.court.gov.cn/susongyangshi/78.html"
COURT_2016_ADMIN = "https://www.court.gov.cn/susongyangshi/xiangqing/752.html"

FIELDS = [
    "civil",
    "commercial",
    "family",
    "labor",
    "tort",
    "ip",
    "maritime",
    "administrative",
    "enforcement",
    "state_compensation",
    "arbitration",
    "criminal",
    "lawyer_practice",
]

MANIFEST_FIELDS = [
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


DEMO_67 = [
    ("criminal", "侮辱案", "侮辱案刑事（附带民事）自诉状/答辩状", "诽谤案刑事（附带民事）.doc"),
    ("criminal", "诽谤案", "诽谤案刑事（附带民事）自诉状/答辩状", "诽谤案刑事（附带民事）.doc"),
    ("criminal", "重婚案", "重婚案刑事（附带民事）自诉状/答辩状", "重婚案刑事（附带民事）.doc"),
    ("criminal", "拒不执行判决、裁定案", "拒不执行判决、裁定案刑事（附带民事）自诉状/答辩状", "拒不执行判决、裁定案刑事（附带民事）.doc"),
    ("family", "离婚纠纷", "离婚纠纷起诉状/答辩状", "离婚纠纷.doc"),
    ("civil", "民间借贷纠纷", "民间借贷纠纷起诉状/答辩状", "民间借贷纠纷.doc"),
    ("commercial", "金融借款合同纠纷", "金融借款合同纠纷起诉状/答辩状", "金融借款合同纠纷.doc"),
    ("commercial", "买卖合同纠纷", "买卖合同纠纷起诉状/答辩状", "买卖合同纠纷.doc"),
    ("labor", "劳动争议纠纷", "劳动争议纠纷起诉状/答辩状", "劳动争议纠纷.doc"),
    ("tort", "机动车交通事故责任纠纷", "机动车交通事故责任纠纷起诉状/答辩状", "机动车交通事故责任纠.doc"),
    ("commercial", "信用卡纠纷", "信用卡纠纷起诉状/答辩状", "信用卡纠纷.doc"),
    ("commercial", "物业服务合同纠纷", "物业服务合同纠纷起诉状/答辩状", "物业服务合同纠纷.doc"),
    ("commercial", "财产损失保险合同纠纷", "财产损失保险合同纠纷起诉状/答辩状", "财产损失保险合同纠纷.doc"),
    ("commercial", "证券虚假陈述责任纠纷", "证券虚假陈述责任纠纷起诉状/答辩状", "证券虚假陈述责任纠纷.doc"),
    ("commercial", "保证保险合同纠纷", "保证保险合同纠纷起诉状/答辩状", "保证保险合同纠纷.doc"),
    ("commercial", "融资租赁合同纠纷", "融资租赁合同纠纷起诉状/答辩状", "融资租赁合同纠纷.doc"),
    ("commercial", "房屋买卖合同纠纷", "房屋买卖合同纠纷起诉状/答辩状", "房屋买卖合同纠纷.doc"),
    ("commercial", "房屋租赁合同纠纷", "房屋租赁合同纠纷起诉状/答辩状", "房屋租赁合同纠纷.doc"),
    ("commercial", "建设工程施工合同纠纷", "建设工程施工合同纠纷起诉状/答辩状", "建设工程施工合同纠纷.doc"),
    ("commercial", "人身保险合同纠纷", "人身保险合同纠纷起诉状/答辩状", "人身保险合同纠纷.doc"),
    ("commercial", "责任保险合同纠纷", "责任保险合同纠纷起诉状/答辩状", "责任保险合同纠纷.doc"),
    ("ip", "侵害著作权及邻接权纠纷", "侵害著作权及邻接权纠纷起诉状/答辩状", "侵害著作权及邻接权纠纷.doc"),
    ("ip", "侵害商标权纠纷", "侵害商标权纠纷起诉状/答辩状", "侵害商标权纠纷.doc"),
    ("ip", "侵害发明专利权纠纷", "侵害发明专利权纠纷起诉状/答辩状", "侵害发明专利权纠纷.doc"),
    ("ip", "侵害外观设计专利权纠纷", "侵害外观设计专利权纠纷起诉状/答辩状", "侵害外观设计专利权纠纷.doc"),
    ("ip", "侵害植物新品种权纠纷", "侵害植物新品种权纠纷起诉状/答辩状", "侵害植物新品种权纠纷.doc"),
    ("ip", "侵害商业秘密纠纷", "侵害商业秘密纠纷起诉状/答辩状", "侵害商业秘密纠纷.doc"),
    ("ip", "技术合同纠纷", "技术合同纠纷起诉状/答辩状", "技术合同纠纷.doc"),
    ("ip", "不正当竞争纠纷", "不正当竞争纠纷起诉状/答辩状", "不正当竞争纠纷.doc"),
    ("ip", "垄断纠纷", "垄断纠纷起诉状/答辩状", "垄断纠纷.doc"),
    ("ip", "商标申请驳回复审纠纷", "商标申请驳回复审纠纷行政起诉状/答辩状", "商标申请驳回复审纠纷.doc"),
    ("ip", "商标撤销复审行政纠纷", "商标撤销复审行政纠纷行政起诉状/答辩状", "商标撤销复审行政纠纷.doc"),
    ("ip", "商标无效行政纠纷", "商标无效行政纠纷行政起诉状/答辩状", "商标无效行政纠纷.doc"),
    ("ip", "专利申请驳回复审行政纠纷", "专利申请驳回复审行政纠纷行政起诉状/答辩状", "专利申请驳回复审行政纠纷.doc"),
    ("ip", "专利无效行政纠纷", "专利无效行政纠纷行政起诉状/答辩状", "专利无效行政纠纷.doc"),
    ("maritime", "船舶碰撞损害责任纠纷", "船舶碰撞损害责任纠纷起诉状/答辩状", "船舶碰撞损害责任纠纷.doc"),
    ("maritime", "船员劳务合同纠纷", "船员劳务合同纠纷起诉状/答辩状", "船员劳务合同纠纷.doc"),
    ("maritime", "海上、通海水域货运代理合同纠纷", "海上、通海水域货运代理合同纠纷起诉状/答辩状", "海上、通海水域货运代理合同纠纷.doc"),
    ("maritime", "海上、通海水域人身损害责任纠纷", "海上、通海水域人身损害责任纠纷起诉状/答辩状", "海上、通海水域人身损害责任纠纷.doc"),
    ("administrative", "行政处罚", "行政处罚行政起诉状/答辩状", "行政处罚.docx"),
    ("administrative", "行政强制执行", "行政强制执行行政起诉状/答辩状", "行政强制执行.docx"),
    ("administrative", "行政许可", "行政许可行政起诉状/答辩状", "行政许可.docx"),
    ("administrative", "国有土地上房屋征收决定", "国有土地上房屋征收决定行政起诉状/答辩状", "国有土地上房屋征收决定.docx"),
    ("administrative", "工伤保险资格或者待遇认定", "工伤保险资格或者待遇认定行政起诉状/答辩状", "工伤保险资格或者待遇认定.docx"),
    ("administrative", "政府信息公开", "政府信息公开行政起诉状/答辩状", "政府信息公开.docx"),
    ("administrative", "行政复议", "行政复议行政起诉状/答辩状", "行政复议.docx"),
    ("administrative", "行政协议", "行政协议行政起诉状/答辩状", "行政协议.docx"),
    ("administrative", "行政补偿", "行政补偿行政起诉状/答辩状", "行政补偿.docx"),
    ("administrative", "行政赔偿", "行政赔偿行政起诉状/答辩状", "行政赔偿.docx"),
    ("administrative", "不履行法定职责", "不履行法定职责行政起诉状/答辩状", "不履行法定职.docx"),
    ("administrative", "行政答辩状", "行政答辩状", "行政答辩状.docx"),
    ("environmental_resources", "环境污染民事公益诉讼", "环境污染民事公益诉讼起诉状", "民事起诉状(环境污染民事公益诉讼).docx"),
    ("environmental_resources", "生态环境损害赔偿诉讼", "生态环境损害赔偿诉讼起诉状", "民事起诉状(生态环境损害赔偿诉讼).docx"),
    ("environmental_resources", "生态破坏民事公益诉讼", "生态破坏民事公益诉讼起诉状", "民事起诉状(生态破坏民事公益诉讼).docx"),
    ("state_compensation", "违法刑事拘留赔偿", "违法刑事拘留赔偿国家赔偿申请书/答辩状", "违法刑事拘留赔偿.docx"),
    ("state_compensation", "刑事改判无罪赔偿", "刑事改判无罪赔偿国家赔偿申请书/答辩状", "刑事改判无罪赔偿.docx"),
    ("state_compensation", "怠于履行监管职责致伤致死赔偿", "怠于履行监管职责致伤致死赔偿国家赔偿申请书/答辩状", "怠于履行监管职责致伤致死赔偿.docx"),
    ("state_compensation", "错误执行赔偿", "错误执行赔偿国家赔偿申请书/答辩状", "错误执行赔偿.docx"),
    ("enforcement", "强制执行申请书", "强制执行申请书", "强制执行申请书.docx"),
    ("enforcement", "暂时解除乘坐飞机、高铁限制措施申请书", "暂时解除乘坐飞机、高铁限制措施申请书", "暂时解除乘坐飞机、高铁限制措施申请书.docx"),
    ("enforcement", "参与分配申请书", "参与分配申请书", "参与分配申请书.docx"),
    ("enforcement", "执行担保申请书", "执行担保申请书", "执行担保申请书.docx"),
    ("enforcement", "确认优先购买权申请书", "确认优先购买权申请书", "确认优先购买权申请书.docx"),
    ("enforcement", "执行异议申请书", "执行异议申请书", "执行异议申请书.docx"),
    ("enforcement", "执行复议申请书", "执行复议申请书", "执行复议申请书.docx"),
    ("enforcement", "执行监督申请书", "执行监督申请书", "执行监督申请书.docx"),
    ("enforcement", "不予执行仲裁裁决、调解书或公证债权文书申请书", "不予执行仲裁裁决、调解书或公证债权文书申请书", "不予执行仲裁裁决、调解书或公证债权文书申请书.docx"),
]

ADDITIONAL_COURT_2016 = [
    ("civil", "民事反诉状（公民提起民事反诉用）", COURT_2016_ORDINARY),
    ("civil", "民事反诉状（法人或者其他组织提起民事反诉用）", COURT_2016_ORDINARY),
    ("civil", "民事答辩状（法人或者其他组织对民事起诉提出答辩用）", "https://www.court.gov.cn/susongyangshi/xiangqing/224.html"),
    ("civil", "申请书（申请追加必要的共同诉讼当事人用）", COURT_2016_ORDINARY),
    ("civil", "申请书（无独立请求权的第三人申请参加诉讼用）", COURT_2016_ORDINARY),
    ("civil", "申请书（申请增加诉讼请求用）", COURT_2016_ORDINARY),
    ("civil", "申请书（申请变更诉讼请求用）", COURT_2016_ORDINARY),
    ("civil", "申请书（申请撤回起诉用）", COURT_2016_ORDINARY),
    ("civil", "申请书（申请撤回反诉用）", COURT_2016_ORDINARY),
    ("civil", "申请书（申请恢复诉讼用）", COURT_2016_ORDINARY),
    ("environmental_resources", "民事起诉状（提起公益诉讼用）", "https://www.court.gov.cn/susongyangshi/xiangqing/318.html"),
    ("environmental_resources", "申请书（其他机关和有关组织申请参加公益诉讼用）", COURT_2016_PUBLIC_INTEREST),
    ("environmental_resources", "意见书（支持起诉单位提交书面意见用）", COURT_2016_PUBLIC_INTEREST),
    ("administrative", "行政起诉状", COURT_2016_ADMIN),
    ("enforcement", "民事起诉状（案外人提起执行异议之诉用）", "https://www.court.gov.cn/susongyangshi/xiangqing/361.html"),
    ("enforcement", "民事起诉状（申请执行人提起执行异议之诉用）", "https://www.court.gov.cn/susongyangshi/xiangqing/370.html"),
    ("civil", "民事起诉状（提起第三人撤销之诉用）", "https://www.court.gov.cn/susongyangshi/xiangqing/353.html"),
]

CRIMINAL_EXTRA = [
    "取保候审申请书", "变更强制措施申请书", "解除取保候审申请书", "解除监视居住申请书", "会见犯罪嫌疑人申请书",
    "会见在押犯罪嫌疑人函", "通信申请", "阅卷申请书", "调取证据申请书", "收集证据申请书", "不予批准逮捕法律意见书",
    "羁押必要性审查申请书", "侦查阶段法律意见书", "控告申诉材料", "立案监督申请书", "撤销案件法律意见书",
    "复制案卷材料申请", "补充侦查申请或意见", "不起诉法律意见书", "相对不起诉法律意见书", "附条件不起诉意见",
    "认罪认罚从宽法律意见", "认罪认罚具结书审查意见", "量刑建议调整意见", "非法证据排除申请书",
    "证人出庭申请书", "鉴定人出庭申请书", "重新鉴定申请书", "庭前会议申请书", "庭前会议意见",
    "有专门知识的人出庭申请书", "回避申请书", "管辖异议申请书", "延期审理申请书", "重新开庭申请书",
    "辩护词（无罪）", "辩护词（罪轻）", "辩护词（量刑）", "辩护词（程序违法）", "被害人代理词",
    "刑事附带民事代理词", "质证意见", "庭审发问提纲", "量刑意见", "缓刑适用意见", "罚金刑调整意见",
    "刑事上诉状", "刑事申诉状", "再审申请书", "刑事抗诉申请书", "暂予监外执行申请书", "减刑、假释法律意见",
    "财产刑执行异议", "涉案财物处理异议", "刑事赔偿申请书", "会见笔录", "阅卷笔录", "案件分析报告",
    "证据摘录表", "证据目录", "辩护方案", "庭审提纲", "发问提纲", "质证提纲", "法律检索报告",
    "类案检索报告", "风险告知书", "委托人沟通记录", "律师工作日志",
]

LAWYER_DOCS = [
    "律师函", "催告函", "解除合同通知函", "违约责任告知函", "侵权停止通知函", "知识产权侵权警告函", "谈判函",
    "和解建议书", "调解方案", "法律意见书", "专项法律意见书", "律师见证书", "律师声明", "尽职调查报告",
    "法律尽职调查清单", "合同审查意见", "合同修改说明", "合同风险提示函", "合规审查意见", "数据合规审查意见",
    "劳动用工合规意见", "公司治理法律意见", "股权架构法律意见", "投融资法律意见", "并购法律意见", "破产重整法律意见",
    "代理词", "辩护词", "质证意见", "举证意见", "证据目录", "证据说明", "庭审提纲", "发问提纲", "交叉询问提纲",
    "类案检索报告", "法律检索报告", "案件分析备忘录", "诉讼策略备忘录", "风险评估报告", "诉讼可视化时间线",
    "争议焦点归纳", "裁判规则摘要", "委托代理合同附件", "授权委托书", "客户访谈笔录", "律师谈话笔录", "风险告知书",
    "利益冲突审查表", "材料交接清单", "工作计划", "工作日志", "项目进度报告", "结案报告", "法律服务成果交付清单",
]

LABOR_ARBITRATION_DOCS = [
    "劳动仲裁申请书", "劳动仲裁答辩书", "确认劳动关系申请书", "违法解除劳动合同赔偿申请", "工伤待遇争议申请",
    "加班费争议申请", "竞业限制纠纷申请", "社会保险待遇争议申请", "劳动仲裁证据目录", "仲裁代理意见", "劳动争议调解申请书",
]

ARBITRATION_DOCS = [
    "仲裁申请书", "仲裁答辩书", "仲裁反请求申请书", "仲裁财产保全申请书", "仲裁证据保全申请书", "仲裁管辖异议书",
    "仲裁代理词", "撤回仲裁申请书", "申请撤销仲裁裁决申请书", "申请确认仲裁协议效力申请书", "申请执行仲裁裁决申请书",
    "申请不予执行仲裁裁决申请书",
]


def slugify(text):
    words = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "-", text).strip("-")
    return words[:80] or "document"


def local(path):
    return f"skills/legal-document-drafting/{path.relative_to(ROOT).as_posix()}"


def yaml_block(meta):
    return "---\n" + "\n".join(f"{k}: {v}" for k, v in meta.items() if k != "source_status") + "\n---\n\n"


def write_md(path, meta, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = dict(meta)
    meta["retrieved_at"] = RETRIEVED_AT
    meta["local_path"] = local(path)
    path.write_text(yaml_block(meta) + body.strip() + "\n", encoding="utf-8")
    return meta["local_path"]


def read_existing_official_templates(rows):
    for path in sorted((ROOT / "assets" / "official_templates").glob("**/*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---", 4)
        meta = {}
        for line in text[4:end].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        rows.append({
            "title": meta.get("title", path.stem),
            "document_type": meta.get("document_type", "官方文书样式"),
            "field": meta.get("field", "civil"),
            "intended_author": meta.get("intended_author", "party"),
            "usable_for_generation": meta.get("usable_for_generation", "true"),
            "authority_level": meta.get("authority_level", "A"),
            "issuing_authority": meta.get("issuing_authority", "中华人民共和国最高人民法院"),
            "source_url": meta.get("source_url", SPC_2025_RELEASE),
            "publish_date": meta.get("publish_date", "unknown"),
            "retrieved_at": meta.get("retrieved_at", RETRIEVED_AT),
            "local_path": local(path),
            "source_status": meta.get("source_status", "official_collected"),
            "notes": meta.get("notes", "既有官方模板。"),
        })


def add_row(rows, **kwargs):
    row = {key: "" for key in MANIFEST_FIELDS}
    row.update(kwargs)
    row.setdefault("retrieved_at", RETRIEVED_AT)
    rows.append(row)


def setup_dirs():
    for sub in ["official_templates", "official_reference_only"]:
        for field in FIELDS:
            (ROOT / "assets" / sub / field).mkdir(parents=True, exist_ok=True)
    for d in [
        "assets/reviewed_templates", "assets/unverified_candidates",
        "references/official_rules", "references/drafting_guides", "references/civil_guides",
        "references/commercial_guides", "references/criminal_defense_guides",
        "references/administrative_guides", "references/enforcement_guides",
        "references/arbitration_guides", "references/lawyer_practice_guides",
        "references/prohibited_behavior", "references/source_notes", "source_manifest",
    ]:
        (ROOT / d).mkdir(parents=True, exist_ok=True)


def upgrade_legacy_yaml():
    legacy_paths = list((ROOT / "references" / "court-civil-procedure").glob("*.md")) + [
        ROOT / "assets" / "style-selection-guide.md"
    ]
    mapping = {
        "文书名称": "title",
        "文书类型": "document_type",
        "发布机关": "issuing_authority",
        "来源 URL": "source_url",
        "发布时间": "publish_date",
        "抓取日期": "retrieved_at",
        "备注": "notes",
    }
    for path in legacy_paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            continue
        lines = text.splitlines()
        meta = {}
        body_start = 0
        for idx, line in enumerate(lines[:12]):
            if "：" not in line:
                body_start = idx
                break
            key, value = line.split("：", 1)
            if key in mapping:
                meta[mapping[key]] = value.strip()
            body_start = idx + 1
        title = meta.get("title", path.stem)
        field = "civil"
        if "执行" in title:
            field = "enforcement"
        if "授权委托" in title or "选择说明" in title:
            field = "lawyer_practice" if "授权委托" in title else "other"
        yaml_meta = {
            "title": title,
            "document_type": meta.get("document_type", "历史参考文件"),
            "field": field,
            "intended_author": "party" if "选择说明" not in title else "other",
            "usable_for_generation": "false",
            "authority_level": "A" if meta.get("source_url", "").startswith("https://www.court.gov.cn") else "C",
            "issuing_authority": meta.get("issuing_authority", "本项目整理"),
            "source_url": meta.get("source_url", SPC_2025_RELEASE),
            "publish_date": meta.get("publish_date", "unknown"),
            "retrieved_at": meta.get("retrieved_at", RETRIEVED_AT),
            "local_path": local(path),
            "notes": meta.get("notes", "由旧版中文元数据头转换为 YAML；正文未改写。"),
        }
        body = "\n".join(lines[body_start:]).lstrip()
        path.write_text(yaml_block(yaml_meta) + body + "\n", encoding="utf-8")


def generate_2025(rows):
    status_rows = []
    for i, (field, case_type, doc_name, attachment) in enumerate(DEMO_67, start=1):
        path = ROOT / "assets" / "official_reference_only" / field / f"2025-67-{i:02d}-{slugify(case_type)}.md"
        meta = {
            "title": f"2025年示范文本：{case_type}",
            "document_type": doc_name,
            "field": field,
            "intended_author": "party",
            "usable_for_generation": "false",
            "authority_level": "C",
            "issuing_authority": "平原县人民法院（转载最高法、司法部、中华全国律师协会示范文本）",
            "source_url": SDCOURT_2025_PARTIAL,
            "publish_date": "2025-08-26",
            "notes": f"转载最高法、司法部、全国律协示范文本；附件名：{attachment}。当前本地 curl/Python 下载尝试出现 TLS SSL_ERROR_SYSCALL/EOF，未取得正文，不作为正式生成模板。",
        }
        local_path = write_md(path, meta, f"# 2025年示范文本：{case_type}\n\n来源页面列出附件：{attachment}。\n\n本地下载尝试失败，未取得空白模板或实例正文。本文件仅记录逐类来源状态，不能直接用于生成正式法律文书。")
        add_row(
            rows,
            title=meta["title"],
            document_type=doc_name,
            field=field,
            intended_author="party",
            usable_for_generation="false",
            authority_level="C",
            issuing_authority=meta["issuing_authority"],
            source_url=SDCOURT_2025_PARTIAL,
            publish_date="2025-08-26",
            retrieved_at=RETRIEVED_AT,
            local_path=local_path,
            source_status="official_reference_only",
            notes=meta["notes"],
        )
        status_rows.append({
            "sequence": i,
            "field": field,
            "case_type": case_type,
            "document_name": doc_name,
            "blank_template_url": SDCOURT_2025_PARTIAL,
            "example_template_url": SDCOURT_2025_PARTIAL,
            "source_page_url": SDCOURT_2025_PARTIAL,
            "download_status": "failed",
            "local_blank_path": local_path,
            "local_example_path": "",
            "failure_reason": f"附件名 {attachment}；已尝试 curl -L --http1.1 -k 和 Python urllib 访问法院站点，当前环境返回 SSL_ERROR_SYSCALL/EOF，未能下载原始附件。",
            "notes": "C级来源，地方基层法院转载最高法、司法部、全国律协示范文本；需人工或可用网络环境下载核验正文。",
        })
    status_path = ROOT / "source_manifest" / "2025_67_texts_status.csv"
    with status_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(status_rows[0].keys()))
        writer.writeheader()
        writer.writerows(status_rows)
    index_meta = {
        "title": "2025年67类起诉状答辩状示范文本逐类索引",
        "document_type": "官方示范文本索引",
        "field": "other",
        "intended_author": "party",
        "usable_for_generation": "false",
        "authority_level": "A",
        "issuing_authority": "最高人民法院、司法部、中华全国律师协会",
        "source_url": SPC_2025_RELEASE,
        "publish_date": "2025-06-23",
        "notes": "最高法发布页确认67类示范文本；逐类状态见 source_manifest/2025_67_texts_status.csv。",
    }
    body = "# 2025年67类起诉状答辩状示范文本逐类索引\n\n最高法发布页确认示范文本覆盖9个领域、67类常见纠纷，并自2025年7月14日起推广使用。\n\n本地逐类状态以 `source_manifest/2025_67_texts_status.csv` 为准。当前附件下载因 TLS 连接失败未完成，已按类建立 reference-only 文件。"
    path = ROOT / "references" / "official_rules" / "2025_67_demonstration_texts_index.md"
    local_path = write_md(path, index_meta, body)
    add_row(rows, **{**index_meta, "retrieved_at": RETRIEVED_AT, "local_path": local_path, "source_status": "official_reference_only"})


def generate_2016_reference(rows):
    for field, title, url in ADDITIONAL_COURT_2016:
        path = ROOT / "assets" / "official_reference_only" / field / f"spc-2016-reference-{slugify(title)}.md"
        meta = {
            "title": title,
            "document_type": "最高人民法院诉讼文书样式索引",
            "field": field,
            "intended_author": "party",
            "usable_for_generation": "false",
            "authority_level": "A",
            "issuing_authority": "中华人民共和国最高人民法院",
            "source_url": url,
            "publish_date": "2016-09-28",
            "notes": "最高法官网诉讼文书样式；当前仅建立索引或结构参考，未机械复制正文。",
        }
        lp = write_md(path, meta, f"# {title}\n\n来源为最高人民法院诉讼文书样式页面。该文件为 reference-only 索引，正式使用前应打开来源页面核验正文。")
        add_row(rows, **{**meta, "retrieved_at": RETRIEVED_AT, "local_path": lp, "source_status": "official_reference_only"})


def generate_criminal(rows):
    for title in CRIMINAL_EXTRA:
        url = SPP_CUSTODY_REVIEW if "羁押必要性" in title else NPC_CRIMINAL_PROCEDURE
        path = ROOT / "references" / "criminal_defense_guides" / f"{slugify(title)}.md"
        meta = {
            "title": title,
            "document_type": "刑事案件律师/当事人文书起草指南",
            "field": "criminal",
            "intended_author": "lawyer",
            "usable_for_generation": "false",
            "authority_level": "A",
            "issuing_authority": "全国人民代表大会或最高人民检察院",
            "source_url": url,
            "publish_date": "2018-11-05" if url == NPC_CRIMINAL_PROCEDURE else "2016-02-02",
            "notes": "已检索来源：全国人大刑事诉讼法、最高检羁押必要性审查规则。未找到统一官方模板时，只能作为参考草稿依据并需律师复核。",
        }
        body = f"# {title}\n\n用途：刑事案件相关文书的起草参考。\n\n权威依据：刑事诉讼法；涉及羁押必要性审查的，同时参考最高检羁押必要性审查规定。\n\n起草要求：区分案件阶段、提交对象、涉嫌罪名、强制措施状态、羁押期限、证据状况和申请目标。不得承诺结果，不得生成串供、毁灭证据、伪造证据、规避侦查等内容。"
        lp = write_md(path, meta, body)
        add_row(rows, **{**meta, "retrieved_at": RETRIEVED_AT, "local_path": lp, "source_status": "guide_collected"})


def lawyer_source_for(title):
    if any(k in title for k in ["法律意见", "合规", "投融资", "并购", "公司治理", "股权架构"]):
        return GOV_SECURITIES_LEGAL, "国务院公报/司法部证券法律业务规则", "A", "2023-10-26"
    if any(k in title for k in ["尽职", "调查清单"]):
        return ACLA_DD, "中华全国律师协会业务文章/指引线索", "B", "2022-02-23"
    if any(k in title for k in ["合同", "催告", "解除", "违约"]):
        return ACLA_SALE, "中华全国律师协会买卖合同业务操作指引", "B", "2017-11-16"
    if any(k in title for k in ["知识产权", "侵权停止"]):
        return ACLA_PATENT, "中华全国律师协会专利侵权业务操作指引", "B", "2017-11-16"
    if any(k in title for k in ["代理词", "质证", "举证", "证据", "庭审", "发问", "争议焦点"]):
        return ACLA_MARRIAGE, "中华全国律师协会婚姻家庭业务操作指引", "B", "2017-11-16"
    return GOV_SECURITIES_LEGAL, "司法部/中国政府网律师执业与法律意见规则", "A", "2023-10-26"


def generate_lawyer(rows):
    for title in LAWYER_DOCS:
        url, authority, level, date = lawyer_source_for(title)
        path = ROOT / "references" / "lawyer_practice_guides" / f"{slugify(title)}.md"
        meta = {
            "title": title,
            "document_type": "律师实务文书起草指南",
            "field": "lawyer_practice",
            "intended_author": "lawyer",
            "usable_for_generation": "false",
            "authority_level": level,
            "issuing_authority": authority,
            "source_url": url,
            "publish_date": date,
            "notes": "已检索来源：司法部/中国政府网、全国律协业务指引。多数律师实务文书无全国统一模板，标记为指南收集，需结合委托范围和律师执业风险复核。",
        }
        body = f"# {title}\n\n本文件不是统一官方模板，而是基于司法部、国务院公报或全国律协业务指引形成的起草规则索引。\n\n起草时应列明委托范围、事实来源、已审阅材料、法律分析、结论限制、风险提示和待补充材料。不得虚构律师身份、律所名称、执业证号或承诺结果。"
        lp = write_md(path, meta, body)
        add_row(rows, **{**meta, "retrieved_at": RETRIEVED_AT, "local_path": lp, "source_status": "guide_collected"})


def generate_labor_arbitration(rows):
    for title in LABOR_ARBITRATION_DOCS:
        path = ROOT / "references" / "arbitration_guides" / f"labor-{slugify(title)}.md"
        meta = {
            "title": title,
            "document_type": "劳动人事争议仲裁文书起草指南",
            "field": "labor",
            "intended_author": "party",
            "usable_for_generation": "false",
            "authority_level": "A",
            "issuing_authority": "人力资源和社会保障部相关平台",
            "source_url": MOHRSS_ARBITRATION_RULES,
            "publish_date": "2022-07-15",
            "notes": "已检索来源：劳动人事争议仲裁办案规则。该文件为规则依据，不是统一模板。",
        }
        lp = write_md(path, meta, f"# {title}\n\n依据劳动人事争议仲裁办案规则记录起草要点：当事人信息、仲裁请求、事实理由、证据和证据来源、证人信息。")
        add_row(rows, **{**meta, "retrieved_at": RETRIEVED_AT, "local_path": lp, "source_status": "guide_collected"})
    for title in ARBITRATION_DOCS:
        url = CIETAC_APPLICATION if title == "仲裁申请书" else CIETAC_RULES
        path = ROOT / "references" / "arbitration_guides" / f"{slugify(title)}.md"
        meta = {
            "title": title,
            "document_type": "商事仲裁文书起草指南",
            "field": "arbitration",
            "intended_author": "party",
            "usable_for_generation": "false",
            "authority_level": "A",
            "issuing_authority": "中国国际经济贸易仲裁委员会",
            "source_url": url,
            "publish_date": "2024-01-01",
            "notes": "已检索来源：中国国际经济贸易仲裁委员会仲裁规则或仲裁申请书示范文本。需结合具体仲裁机构规则复核。",
        }
        lp = write_md(path, meta, f"# {title}\n\n依据贸仲规则或示范文本提炼起草要点。仲裁申请类文书应写明当事人、仲裁协议、案情和争议要点、仲裁请求、事实理由、证据材料。")
        add_row(rows, **{**meta, "retrieved_at": RETRIEVED_AT, "local_path": lp, "source_status": "guide_collected" if title != "仲裁申请书" else "official_reference_only"})


def generate_rules_and_reports(rows):
    authority = ROOT / "source_manifest" / "authority_level_rules.md"
    write_md(authority, {
        "title": "权威来源分级规则",
        "document_type": "来源治理规则",
        "field": "other",
        "intended_author": "other",
        "usable_for_generation": "false",
        "authority_level": "A",
        "issuing_authority": "本项目整理",
        "source_url": SPC_2025_RELEASE,
        "publish_date": "2026-05-02",
        "notes": "记录A/B/C/D来源分级和使用限制。",
    }, "# 权威来源分级规则\n\nA级：最高法、最高检、司法部、全国人大、中国政府网、公安部、全国律协、12348、中国仲裁协会或官方仲裁机构、人社部。\n\nB级：省级高院、检察院、司法厅、律协、人社厅、仲裁委、公共法律服务网、法院诉讼服务网。\n\nC级：中级/基层法院、地方司法局、地方律协、官方转载页面。\n\nD级：律所官网、商业平台、培训机构、公众号、博客、文库、论坛、问答社区。D级不得进入正式模板。")
    legal = ROOT / "references" / "official_rules" / "legal_authority_rules.md"
    write_md(legal, {
        "title": "法律依据引用规则",
        "document_type": "起草规则",
        "field": "other",
        "intended_author": "other",
        "usable_for_generation": "false",
        "authority_level": "A",
        "issuing_authority": "本项目整理",
        "source_url": "https://www.npc.gov.cn/",
        "publish_date": "2026-05-02",
        "notes": "规定法律依据引用和现行有效性核验要求。",
    }, "# 法律依据引用规则\n\n不得虚构法条。不得引用无法确认现行有效性的法律。没有接入实时法规库时，应标注“法律依据需人工核验现行有效性”。优先引用法律、行政法规、司法解释、部门规章、地方性法规和规范性文件。刑事、劳动、知识产权、行政、执行案件应分别核验对应基本法律和司法解释。引用法律依据时写明条文要旨，避免机械堆砌。")
    prohibited = ROOT / "references" / "prohibited_behavior" / "prohibited_behavior.md"
    write_md(prohibited, {
        "title": "法律文书起草禁止行为",
        "document_type": "禁止行为",
        "field": "other",
        "intended_author": "other",
        "usable_for_generation": "false",
        "authority_level": "A",
        "issuing_authority": "本项目整理",
        "source_url": NPC_CRIMINAL_PROCEDURE,
        "publish_date": "2026-05-02",
        "notes": "法律文书起草安全边界。",
    }, "# 禁止行为\n\n禁止虚构事实、证据、法条、案例、案号、机关、律师身份、律所名称、执业证号。禁止承诺胜诉、取保候审成功、不起诉、缓刑或无罪。禁止指导串供、毁灭、伪造、隐匿证据、规避侦查。禁止威胁、恐吓、骚扰对方当事人或以律师函不当施压。禁止将不确定事实写成确定事实。禁止把未经核验的网络模板作为权威模板。禁止把法院裁判文书当作律师提交模板。禁止把 guide_collected 当作 official_collected。禁止在缺少事实和证据时直接生成定稿。")

    missing_titles = [
        "2025年67类示范文本附件正文下载", "律师函全国统一模板", "律师见证书全国统一模板", "类案检索报告统一模板",
        "刑事不予批准逮捕法律意见书官方模板", "认罪认罚具结书审查意见官方模板", "撤销案件法律意见书官方模板",
    ]
    missing_body = ["# 缺口报告\n"]
    for title in missing_titles:
        missing_body.append(f"## {title}\n\n已检索来源：最高法、最高检、司法部、中国政府网、全国人大、全国律协、贸仲或人社部等权威来源。当前未取得可纳入正式模板库的统一模板正文；不得使用普通网站范文替代，后续需人工下载官方附件或补充经审定内部模板。\n")
    write_md(ROOT / "source_manifest" / "missing_sources.md", {
        "title": "未找到权威模板的文书清单",
        "document_type": "缺口报告",
        "field": "other",
        "intended_author": "other",
        "usable_for_generation": "false",
        "authority_level": "A",
        "issuing_authority": "本项目整理",
        "source_url": SPC_2025_RELEASE,
        "publish_date": "2026-05-02",
        "notes": "每项缺口说明已检索权威来源和后续处理。",
    }, "\n".join(missing_body))
    for title in missing_titles:
        add_row(rows, title=title, document_type="待补权威模板", field="lawyer_practice" if "律师" in title or "类案" in title else "criminal", intended_author="lawyer", usable_for_generation="false", authority_level="A", issuing_authority="本项目整理", source_url=SPC_2025_RELEASE, publish_date="2026-05-02", retrieved_at=RETRIEVED_AT, local_path="skills/legal-document-drafting/source_manifest/missing_sources.md", source_status="missing", notes="已检索来源：最高法、最高检、司法部、中国政府网、全国人大、全国律协等；未取得权威模板正文，需人工补充。")

    status_counts = Counter(r["source_status"] for r in rows)
    field_counts = Counter(r["field"] for r in rows)
    report = f"""# 收集报告

## 已完成

- 来源记录数：{len(rows)}
- official_collected：{status_counts.get('official_collected', 0)}
- official_reference_only：{status_counts.get('official_reference_only', 0)}
- guide_collected：{status_counts.get('guide_collected', 0)}

## 2025年67类示范文本

已逐类建立 67 条状态记录和单独 Markdown 文件。当前本地网络访问法院站点附件时出现 TLS 连接失败，因此未把附件正文标记为已收集；所有 67 条均为 reference-only，需人工或可用网络环境继续下载核验。

## 刑事和律师实务

criminal 记录数：{field_counts.get('criminal', 0)}。刑事官方正文不足 5 条，原因是除 2025 刑事自诉类示范文本外，取保、不捕、不诉、排非、辩护词等多无统一公开模板；已按刑诉法和最高检规则建立指南。

lawyer_practice 记录数：{field_counts.get('lawyer_practice', 0)}。多数律师实务文书没有全国统一模板，已优先按司法部、中国政府网、全国律协业务指引建立 guide_collected。

## 不建议纳入来源

百度文库、公众号、个人博客、知乎、简书、论坛、CSDN、豆丁、道客巴巴、培训机构营销页、商业法律平台和未注明机关/时间的文件不得进入正式模板库。
"""
    write_md(ROOT / "source_manifest" / "collection_report.md", {
        "title": "legal-document-drafting 收集报告",
        "document_type": "收集报告",
        "field": "other",
        "intended_author": "other",
        "usable_for_generation": "false",
        "authority_level": "A",
        "issuing_authority": "本项目整理",
        "source_url": SPC_2025_RELEASE,
        "publish_date": "2026-05-02",
        "notes": "总结本轮扩充状态、缺口和不建议纳入来源。",
    }, report)


def write_skill():
    body = """# Legal Document Drafting

## 1. Skill 适用范围

用于中文法律文书的起草、改写、审查和结构化，包括诉讼、仲裁、执行、刑事辩护、国家赔偿、行政、知识产权、海事、环境资源和律师实务文书。

## 2. 文书类型识别规则

先识别用户需要的是起诉状、答辩状、申请书、意见书、代理词、辩护词、律师函、报告、清单、笔录还是内部工作文书。若不明确，先追问，不直接生成定稿。

## 3. 案件领域识别规则

字段使用 civil、commercial、family、labor、tort、ip、maritime、administrative、enforcement、state_compensation、arbitration、criminal、lawyer_practice。无法归类时标记 other 并说明原因。

## 4. 模板选择优先级

优先 `assets/official_templates/`，其次 `assets/official_reference_only/` 作结构参考，再次 `assets/reviewed_templates/`，最后 `references/` 中的规则指南。`unverified_candidates/` 不得直接用于正式文书。

## 5. 权威来源分级规则

A级为中央机关、全国律协、12348、官方仲裁机构、人社部等；B级为省级法院、检察院、司法厅、律协、人社厅、仲裁委；C级为中基层法院、地方司法局、地方律协和官方转载；D级不得作为正式模板。

## 6. 无模板时的处理规则

没有正式模板时，只能基于规则和用户事实输出“参考草稿”，并写明：缺少权威模板，需律师复核。不得把指南包装成模板。

## 7. 民事/商事文书起草规则

明确当事人、管辖、案由、请求事项、事实理由、证据和诉讼费用承担。请求事项应具体、明确、可执行，事实与证据逐项对应。

## 8. 刑事文书起草规则

必须区分侦查、审查起诉、一审、二审、再审、执行阶段；记录涉嫌罪名、强制措施、羁押地点、羁押期限、办案机关、证据状况和申请目标。不得承诺取保、不捕、不诉、缓刑或无罪，不得生成串供、毁证、伪证、规避侦查内容。

## 9. 行政文书起草规则

确认行政行为、被告机关、复议前置要求、起诉期限、诉讼请求、事实根据、证据和规范性文件审查需求。

## 10. 执行文书起草规则

确认执行依据、生效情况、履行期限、被执行人信息、财产线索、申请事项和执行风险。执行异议类文书需区分当事人异议、案外人异议和执行异议之诉。

## 11. 仲裁文书起草规则

确认仲裁协议、仲裁机构、仲裁请求、事实理由、证据、仲裁费用和保全需求。不同机构规则不一致时，优先适用约定机构规则。

## 12. 律师实务文书起草规则

律师函、法律意见书、尽调报告、合同审查意见等不属于法院统一样式。必须说明委托范围、事实来源、审阅材料、假设限制、风险揭示、结论和复核需求。

## 13. 法律依据引用规则

不得虚构法条。没有实时法规库时标注“法律依据需人工核验现行有效性”。优先引用法律、行政法规、司法解释、部门规章、地方性法规和规范性文件，并写明条文要旨。

## 14. 事实与证据区分规则

区分用户已确认事实、用户主张、证据材料、法律依据、法律分析、诉求、风险提示和待补充信息。不确定事实使用“据用户陈述”“待核验”等表述。

## 15. 风险提示规则

提示管辖、期限、证据不足、主体资格、诉讼费用、保全担保、刑事合规和律师执业风险。

## 16. 禁止行为

禁止虚构事实、证据、法条、案例、案号、机关、律师身份。禁止承诺结果。禁止指导串供、毁证、伪证、规避侦查、威胁骚扰或不当施压。禁止把 guide_collected 当作 official_collected。

## 17. 输出前检查清单

检查标题、提交对象、当事人身份、请求事项、事实理由、证据支撑、法律依据、未核实事实、结果承诺、落款日期、刑事合规、模板属性、占位符和律师复核提示。

## 18. 需要向用户追问的信息清单

追问适用法域、文书类型、案件领域、阶段、提交对象、当事人身份、事实经过、诉求、证据、期限、案号、承办法官/检察官/机关/仲裁机构、是否引用法律依据、正式版或初稿、表达风格。刑事另追问罪名、强制措施、羁押地点和起算时间、批捕/移诉、认罪认罚、退赔谅解、量刑情节、非法取证线索、申请目标和申请人身份。

## 19. 不同文书默认结构

默认使用标题、当事人信息、接收对象、请求或核心意见、事实与理由、证据清单、法律依据、风险提示、待补充信息、落款、日期。官方模板另有结构时以官方模板为准。

## 20. 模板缺失时的降级输出格式

先写“模板状态：缺少权威模板，以下为参考草稿，需律师复核”，再给草稿、依据来源、事实假设、风险提示和待补充材料。不得输出成定稿口吻。
"""
    path = ROOT / "SKILL.md"
    path.write_text("""---
name: legal-document-drafting
description: Use when drafting, revising, checking, or structuring Chinese legal documents, pleadings, applications, criminal defense documents, enforcement filings, arbitration documents, lawyer letters, legal opinions, evidence lists, court submissions, or lawyer practice documents.
---

""" + body, encoding="utf-8")


def write_manifest(rows):
    path = ROOT / "source_manifest" / "sources.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_validate_script():
    script = r'''#!/usr/bin/env python3
import csv
import os
import sys
from collections import Counter
from pathlib import Path

REQUIRED_COLUMNS = {"title","document_type","field","intended_author","usable_for_generation","authority_level","issuing_authority","source_url","publish_date","retrieved_at","local_path","source_status","notes"}
ALLOWED_AUTHORITY_LEVELS = {"A","B","C","D"}
ALLOWED_USABLE = {"true","false"}
ALLOWED_SOURCE_STATUS = {"official_collected","official_reference_only","guide_collected","unverified_candidate","missing","needs_manual_review"}
REQUIRED_FIELDS = {"administrative","enforcement","state_compensation","ip","labor","arbitration"}
INSTITUTION_AUTHORS = {"court","procuratorate","public_security"}
PLACEHOLDERS = ["XXX","某某","【】","TODO"]

def resolve(root, value):
    p = Path(value)
    if p.is_absolute():
        return p
    if value.startswith("skills/legal-document-drafting/"):
        return root.parent.parent / value
    return root / value

def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    data = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data

def validate(root):
    errors = []
    manifest = root / "source_manifest" / "sources.csv"
    status = root / "source_manifest" / "2025_67_texts_status.csv"
    if not manifest.exists():
        return [f"Missing sources.csv: {manifest}"]
    if not status.exists():
        errors.append("Missing 2025_67_texts_status.csv")
    else:
        with status.open(encoding="utf-8", newline="") as h:
            status_rows = list(csv.DictReader(h))
        if len(status_rows) != 67:
            errors.append(f"2025_67_texts_status.csv must contain 67 rows; found {len(status_rows)}")
    with manifest.open(encoding="utf-8", newline="") as h:
        rows = list(csv.DictReader(h))
    if not rows:
        errors.append("sources.csv is empty")
        return errors
    missing_cols = REQUIRED_COLUMNS - set(rows[0].keys())
    if missing_cols:
        errors.append("sources.csv missing columns: " + ", ".join(sorted(missing_cols)))
        return errors
    if len(rows) < 120:
        errors.append(f"sources.csv must contain at least 120 rows; found {len(rows)}")
    official_total = sum(1 for r in rows if r["source_status"] in {"official_collected","official_reference_only"})
    if official_total < 60:
        errors.append(f"official_collected + official_reference_only must be at least 60; found {official_total}")
    counts = Counter(r["field"] for r in rows)
    if counts["criminal"] < 35:
        errors.append(f"criminal records must be at least 35; found {counts['criminal']}")
    if counts["lawyer_practice"] < 35:
        errors.append(f"lawyer_practice records must be at least 35; found {counts['lawyer_practice']}")
    for field in REQUIRED_FIELDS:
        if counts[field] == 0:
            errors.append(f"required field has no records: {field}")
    seen_paths = set()
    for idx, row in enumerate(rows, start=2):
        title = row["title"].strip()
        source_url = row["source_url"].strip()
        if not source_url or "missing" in source_url.lower():
            errors.append(f"Line {idx}: invalid source_url for {title}")
        if row["authority_level"] not in ALLOWED_AUTHORITY_LEVELS:
            errors.append(f"Line {idx}: invalid authority_level for {title}")
        if row["source_status"] not in ALLOWED_SOURCE_STATUS:
            errors.append(f"Line {idx}: invalid source_status for {title}")
        if row["usable_for_generation"] not in ALLOWED_USABLE:
            errors.append(f"Line {idx}: invalid usable_for_generation for {title}")
        if row["source_status"] == "missing" and "已检索来源" not in row["notes"]:
            errors.append(f"Line {idx}: missing record lacks searched-source note for {title}")
        path = resolve(root, row["local_path"])
        seen_paths.add(path.resolve())
        if not path.exists():
            errors.append(f"Line {idx}: local_path does not exist for {title}: {row['local_path']}")
            continue
        if path.suffix == ".md":
            meta = frontmatter(path)
            if meta is None:
                errors.append(f"Line {idx}: Markdown lacks YAML metadata: {row['local_path']}")
            text = path.read_text(encoding="utf-8")
            if row["source_status"] not in {"official_collected","official_reference_only"}:
                for ph in PLACEHOLDERS:
                    if ph in text:
                        errors.append(f"Line {idx}: unresolved placeholder {ph} in {row['local_path']}")
        normalized = str(path)
        if row["authority_level"] == "D" and f"assets{os.sep}official_templates" in normalized:
            errors.append(f"Line {idx}: D-level source inside official_templates: {title}")
        if row["intended_author"] in INSTITUTION_AUTHORS and row["usable_for_generation"] == "true":
            errors.append(f"Line {idx}: institution-authored document marked usable_for_generation=true: {title}")
    for md in root.rglob("*.md"):
        if ".DS_Store" in str(md):
            continue
        meta = frontmatter(md)
        if meta is None:
            errors.append(f"Markdown lacks YAML metadata: {md.relative_to(root)}")
    return errors

def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate(root.resolve())
    if errors:
        for e in errors:
            print(e)
        return 1
    print("OK: expanded source manifest, metadata, 2025 status, and coverage thresholds validated")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
'''
    (ROOT / "scripts" / "validate_manifest.py").write_text(script, encoding="utf-8")


def write_report_script():
    script = r'''#!/usr/bin/env python3
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
    print("下一步建议: 在可访问法院附件的网络环境中批量下载2025年doc/docx并转换Markdown；补充经审定的律师实务内部模板。")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
'''
    (ROOT / "scripts" / "report_coverage.py").write_text(script, encoding="utf-8")


def main():
    setup_dirs()
    upgrade_legacy_yaml()
    rows = []
    read_existing_official_templates(rows)
    generate_2025(rows)
    generate_2016_reference(rows)
    generate_criminal(rows)
    generate_lawyer(rows)
    generate_labor_arbitration(rows)
    generate_rules_and_reports(rows)
    write_skill()
    write_manifest(rows)
    write_validate_script()
    write_report_script()
    print(f"Generated {len(rows)} source rows and {len(DEMO_67)} 2025 status rows")


if __name__ == "__main__":
    main()
