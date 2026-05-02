#!/usr/bin/env python3
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
