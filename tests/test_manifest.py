from __future__ import annotations

import json

from naylence.starters.manifest import list_templates_from_manifest, parse_manifest


def test_manifest_parsing_and_listing(tmp_path):
    manifest_data = {
        "version": 1,
        "templates": [
            {
                "id": "agent-on-sentinel",
                "name": "Agent on Sentinel",
                "description": "Starter agent.",
                "flavors": [
                    {"id": "ts", "path": "ts"},
                    {"id": "py", "path": "py"},
                ],
                "order": 1,
            }
        ],
    }
    raw = json.dumps(manifest_data)
    manifest = parse_manifest(raw, "manifest.json")

    (tmp_path / "templates" / "agent-on-sentinel" / "ts").mkdir(parents=True)
    (tmp_path / "templates" / "agent-on-sentinel" / "py").mkdir(parents=True)

    templates = list_templates_from_manifest(str(tmp_path), manifest)
    assert len(templates) == 1
    assert templates[0].id == "agent-on-sentinel"
    assert templates[0].flavors == ["ts", "py"]


def test_manifest_accepts_string_flavors(tmp_path):
    manifest_data = {
        "version": 1,
        "templates": [
            {
                "id": "agent-on-sentinel",
                "name": "Agent on Sentinel",
                "description": "Starter agent.",
                "flavors": ["ts", "py"],
            }
        ],
    }
    raw = json.dumps(manifest_data)
    manifest = parse_manifest(raw, "manifest.json")

    (tmp_path / "templates" / "agent-on-sentinel" / "ts").mkdir(parents=True)
    (tmp_path / "templates" / "agent-on-sentinel" / "py").mkdir(parents=True)

    templates = list_templates_from_manifest(str(tmp_path), manifest)
    assert templates[0].flavors == ["ts", "py"]
