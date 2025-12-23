from __future__ import annotations

import argparse
import json

from naylence.cli.commands.init import run_init


def test_local_scaffold_with_env_path(tmp_path, monkeypatch):
    starters_path = tmp_path / "starters"
    template_root = starters_path / "templates" / "agent-on-sentinel" / "ts"
    template_root.mkdir(parents=True)

    (template_root / "README.md").write_text(
        "__PROJECT_NAME__ __PACKAGE_NAME__ __PY_PACKAGE__\n", encoding="utf-8"
    )
    (template_root / ".env.agent.template").write_text("AGENT=1\n", encoding="utf-8")
    (template_root / ".env.client.template").write_text("CLIENT=1\n", encoding="utf-8")

    manifest = {
        "version": 1,
        "templates": [
            {
                "id": "agent-on-sentinel",
                "name": "Agent on Sentinel",
                "description": "Starter agent.",
                "flavors": [{"id": "ts", "path": "ts"}],
            }
        ],
    }
    manifest_path = starters_path / "templates" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    monkeypatch.setenv("NAYLENCE_STARTERS_PATH", str(starters_path))

    target_dir = tmp_path / "output"
    args = argparse.Namespace(
        target_dir=str(target_dir),
        template="agent-on-sentinel",
        flavor="ts",
        list=False,
        ref=None,
        from_local=True,
        from_github=False,
        no_overwrite=True,
    )

    result = run_init(args)
    assert result == 0

    readme = (target_dir / "README.md").read_text(encoding="utf-8")
    assert "__PROJECT_NAME__" not in readme
    assert "__PACKAGE_NAME__" not in readme
    assert "__PY_PACKAGE__" not in readme

    assert (target_dir / ".env.agent").exists()
    assert (target_dir / ".env.client").exists()
    assert (target_dir / ".gitignore").exists()
