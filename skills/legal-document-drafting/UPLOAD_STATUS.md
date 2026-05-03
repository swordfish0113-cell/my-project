# legal-document-drafting upload status

Current status on 2026-05-03:

- The local `skills/legal-document-drafting/` skill is complete and validated.
- The repository already contains the core skill entry and key manifests/scripts uploaded through the GitHub connector.
- A complete compressed archive has been prepared locally and archive restore instructions/checksums have been added under `skills/legal-document-drafting/archive/`.
- Archive split upload has started: `legal-document-drafting-skill.tar.gz.b64.part001` has been uploaded.

Local complete package:

- `/private/tmp/legal-document-drafting-skill.tar.gz`
- SHA-256: `0c6b90a43871d6c977ad387217a370ac7d1b92eb0a6321c87a638d83021c8697`
- Size: 101326 bytes

Base64 archive:

- `/private/tmp/legal-document-drafting-skill.tar.gz.b64`
- SHA-256: `588751a2948631b754f42eb007f076bd7424102dfa752ba610164fc2125a2e38`
- Size: 135105 bytes

Local package contents:

- 288 skill files, excluding `.DS_Store`
- `source_manifest/sources.csv` with 249 records
- `source_manifest/2025_67_texts_status.csv` with 67 indexed records
- validation, normalization, coverage, and test scripts

Local validation before upload:

```text
python3 -m unittest skills/legal-document-drafting/scripts/test_validate_manifest.py
Ran 4 tests
OK

python3 skills/legal-document-drafting/scripts/validate_manifest.py skills/legal-document-drafting
OK: expanded source manifest, metadata, 2025 status, and coverage thresholds validated
```

Git transport notes:

- Direct HTTPS clone now works when network permission is granted.
- Direct Git push still fails because this machine has no GitHub HTTPS username/token configured for non-interactive Git.
- SSH push also fails because no GitHub public key is available on this machine.
- The GitHub connector can write files, but large payloads occasionally fail, so archive chunks are being uploaded in smaller parts.
