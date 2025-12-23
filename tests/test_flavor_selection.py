from __future__ import annotations

import argparse
import json
import builtins

from naylence.cli.commands.init import run_init


def _write_manifest(path, flavors):
    manifest = {
        "version": 1,
        "templates": [
            {
                "id": "agent-on-sentinel",
                "name": "Agent on Sentinel",
                "description": "Starter agent.",
                "flavors": flavors,
            }
        ],
    }
    manifest_path = path / "templates" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")


def _write_template(starters_path, flavor, marker):
    template_root = starters_path / "templates" / "agent-on-sentinel" / flavor
    template_root.mkdir(parents=True, exist_ok=True)
    (template_root / "README.md").write_text(marker, encoding="utf-8")


def _base_args(target_dir, template="agent-on-sentinel", flavor=None):
    return argparse.Namespace(
        target_dir=str(target_dir),
        template=template,
        flavor=flavor,
        list=False,
        ref=None,
        from_local=True,
        from_github=False,
        no_overwrite=True,
    )


def test_defaults_to_py_without_prompt(tmp_path, monkeypatch):
    starters_path = tmp_path / "starters"
    _write_template(starters_path, "py", "py-template")
    _write_template(starters_path, "ts", "ts-template")
    _write_manifest(
        starters_path, [{"id": "ts", "path": "ts"}, {"id": "py", "path": "py"}]
    )

    monkeypatch.setenv("NAYLENCE_STARTERS_PATH", str(starters_path))

    def _no_prompt(*_args, **_kwargs):
        raise AssertionError("Prompt should not be called for default py flavor")

    monkeypatch.setattr(builtins, "input", _no_prompt)

    target_dir = tmp_path / "output"
    result = run_init(_base_args(target_dir))
    assert result == 0
    assert (target_dir / "README.md").read_text(encoding="utf-8") == "py-template"


def test_defaults_to_only_flavor_without_prompt(tmp_path, monkeypatch):
    starters_path = tmp_path / "starters"
    _write_template(starters_path, "ts", "ts-only")
    _write_manifest(starters_path, [{"id": "ts", "path": "ts"}])

    monkeypatch.setenv("NAYLENCE_STARTERS_PATH", str(starters_path))

    def _no_prompt(*_args, **_kwargs):
        raise AssertionError("Prompt should not be called for single flavor")

    monkeypatch.setattr(builtins, "input", _no_prompt)

    target_dir = tmp_path / "output"
    result = run_init(_base_args(target_dir))
    assert result == 0
    assert (target_dir / "README.md").read_text(encoding="utf-8") == "ts-only"


def test_prompts_when_no_py_and_multiple_flavors(tmp_path, monkeypatch):
    starters_path = tmp_path / "starters"
    _write_template(starters_path, "ts", "ts-template")
    _write_template(starters_path, "poly", "poly-template")
    _write_manifest(
        starters_path, [{"id": "ts", "path": "ts"}, {"id": "poly", "path": "poly"}]
    )

    monkeypatch.setenv("NAYLENCE_STARTERS_PATH", str(starters_path))

    called = []

    def _prompt(_message=""):
        called.append(True)
        return "2"

    monkeypatch.setattr(builtins, "input", _prompt)

    target_dir = tmp_path / "output"
    result = run_init(_base_args(target_dir))
    assert result == 0
    assert called
    assert (target_dir / "README.md").read_text(encoding="utf-8") == "poly-template"


def test_flavor_flag_overrides_default(tmp_path, monkeypatch):
    starters_path = tmp_path / "starters"
    _write_template(starters_path, "py", "py-template")
    _write_template(starters_path, "ts", "ts-template")
    _write_manifest(
        starters_path, [{"id": "ts", "path": "ts"}, {"id": "py", "path": "py"}]
    )

    monkeypatch.setenv("NAYLENCE_STARTERS_PATH", str(starters_path))

    target_dir = tmp_path / "output"
    args = _base_args(target_dir, flavor="ts")
    result = run_init(args)
    assert result == 0
    assert (target_dir / "README.md").read_text(encoding="utf-8") == "ts-template"


def test_flavor_flag_invalid_shows_error(tmp_path, monkeypatch):
    starters_path = tmp_path / "starters"
    _write_template(starters_path, "py", "py-template")
    _write_manifest(starters_path, [{"id": "py", "path": "py"}])

    monkeypatch.setenv("NAYLENCE_STARTERS_PATH", str(starters_path))

    target_dir = tmp_path / "output"
    args = _base_args(target_dir, flavor="ts")
    result = run_init(args)
    assert result == 2
