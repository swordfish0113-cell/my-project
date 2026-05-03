# legal-document-drafting full archive

This folder stores the complete `skills/legal-document-drafting/` skill as base64 split parts because the connector upload path was used after local Git push authentication was unavailable.

## Restore

From this `archive/` directory, run:

```bash
cat legal-document-drafting-skill.tar.gz.b64.part* > legal-document-drafting-skill.tar.gz.b64
base64 -d legal-document-drafting-skill.tar.gz.b64 > legal-document-drafting-skill.tar.gz
tar -xzf legal-document-drafting-skill.tar.gz
```

The archive expands to `skills/legal-document-drafting/` and contains the validated local skill snapshot, excluding `.DS_Store` files.

## Local validation before upload

```bash
python3 -m unittest skills/legal-document-drafting/scripts/test_validate_manifest.py
python3 skills/legal-document-drafting/scripts/validate_manifest.py skills/legal-document-drafting
python3 skills/legal-document-drafting/scripts/report_coverage.py skills/legal-document-drafting
```

Validation passed locally before archiving. Coverage summary: 249 source records, 96 official collected/reference records, 67/67 2025 demonstration texts indexed, 77 criminal records, 60 lawyer practice records.
