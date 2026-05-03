import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


FIELDS = [
    "administrative",
    "enforcement",
    "state_compensation",
    "ip",
    "labor",
    "arbitration",
]


def write_template(path: Path, **metadata):
    path.parent.mkdir(parents=True, exist_ok=True)
    defaults = {
        "title": "测试文书",
        "document_type": "测试文书",
        "field": "civil",
        "intended_author": "party",
        "usable_for_generation": "false",
        "authority_level": "A",
        "issuing_authority": "测试机关",
        "source_url": "https://example.gov.cn/source",
        "publish_date": "unknown",
        "retrieved_at": "2026-05-02",
        "local_path": str(path),
        "notes": "test",
    }
    defaults.update(metadata)
    frontmatter = "\n".join(f"{key}: {value}" for key, value in defaults.items())
    path.write_text(f"---\n{frontmatter}\n---\n\n# 测试文书\n\n已检索来源：测试来源。\n", encoding="utf-8")


def write_manifest(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
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
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_2025_status(path: Path, count=67):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "sequence",
        "field",
        "case_type",
        "document_name",
        "blank_template_url",
        "example_template_url",
        "source_page_url",
        "download_status",
        "local_blank_path",
        "local_example_path",
        "failure_reason",
        "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for idx in range(1, count + 1):
            writer.writerow(
                {
                    "sequence": idx,
                    "field": "civil",
                    "case_type": f"测试类型{idx}",
                    "document_name": "测试示范文本",
                    "blank_template_url": "https://example.gov.cn/source",
                    "example_template_url": "https://example.gov.cn/source",
                    "source_page_url": "https://example.gov.cn/source",
                    "download_status": "failed",
                    "local_blank_path": "",
                    "local_example_path": "",
                    "failure_reason": "test",
                    "notes": "test",
                }
            )


def build_valid_fixture(root: Path):
    rows = []

    def add_row(idx, field, status, authority="A", author="party", usable="false", folder="references"):
        local = root / folder / field / f"doc-{idx}.md"
        write_template(
            local,
            title=f"{field}-{idx}",
            field=field,
            intended_author=author,
            usable_for_generation=usable,
            authority_level=authority,
            local_path=str(local),
        )
        rows.append(
            {
                "title": f"{field}-{idx}",
                "document_type": "测试文书",
                "field": field,
                "intended_author": author,
                "usable_for_generation": usable,
                "authority_level": authority,
                "issuing_authority": "测试机关",
                "source_url": "https://example.gov.cn/source",
                "publish_date": "unknown",
                "retrieved_at": "2026-05-02",
                "local_path": str(local),
                "source_status": status,
                "notes": "已检索来源：测试来源。",
            }
        )

    idx = 0
    for _ in range(35):
        idx += 1
        add_row(idx, "criminal", "guide_collected")
    for _ in range(35):
        idx += 1
        add_row(idx, "lawyer_practice", "guide_collected")
    for field in FIELDS:
        idx += 1
        add_row(idx, field, "guide_collected")
    for _ in range(60):
        idx += 1
        add_row(idx, "civil", "official_reference_only", folder="assets/official_reference_only")

    write_manifest(root / "source_manifest" / "sources.csv", rows)
    write_2025_status(root / "source_manifest" / "2025_67_texts_status.csv")
    return rows


class ValidateManifestTest(unittest.TestCase):
    def test_validator_accepts_threshold_compliant_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "legal-document-drafting"
            build_valid_fixture(root)

            result = subprocess.run(
                [sys.executable, str(Path(__file__).with_name("validate_manifest.py")), str(root)],
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK", result.stdout)

    def test_validator_rejects_d_level_official_template(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "legal-document-drafting"
            rows = build_valid_fixture(root)
            local = root / "assets" / "official_templates" / "civil" / "bad.md"
            write_template(local, field="civil", authority_level="D", local_path=str(local))
            rows.append(
                {
                    "title": "错误模板",
                    "document_type": "民事文书",
                    "field": "civil",
                    "intended_author": "party",
                    "usable_for_generation": "true",
                    "authority_level": "D",
                    "issuing_authority": "未知",
                    "source_url": "https://example.com",
                    "publish_date": "unknown",
                    "retrieved_at": "2026-05-02",
                    "local_path": str(local),
                    "source_status": "unverified_candidate",
                    "notes": "已检索来源：测试来源。",
                }
            )
            write_manifest(root / "source_manifest" / "sources.csv", rows)

            result = subprocess.run(
                [sys.executable, str(Path(__file__).with_name("validate_manifest.py")), str(root)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("D-level source inside official_templates", result.stdout)

    def test_validator_rejects_short_2025_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "legal-document-drafting"
            build_valid_fixture(root)
            write_2025_status(root / "source_manifest" / "2025_67_texts_status.csv", count=66)

            result = subprocess.run(
                [sys.executable, str(Path(__file__).with_name("validate_manifest.py")), str(root)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must contain 67 rows", result.stdout)

    def test_validator_rejects_missing_without_search_note(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "legal-document-drafting"
            rows = build_valid_fixture(root)
            rows[0]["source_status"] = "missing"
            rows[0]["notes"] = "no details"
            write_manifest(root / "source_manifest" / "sources.csv", rows)

            result = subprocess.run(
                [sys.executable, str(Path(__file__).with_name("validate_manifest.py")), str(root)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing record lacks searched-source note", result.stdout)


if __name__ == "__main__":
    unittest.main()
