from __future__ import annotations

from naylence.utils.fs import ensure_env_files, ensure_gitignore_entries


def test_env_init_and_gitignore(tmp_path):
    template_dir = tmp_path / "template"
    dest_dir = tmp_path / "output"
    template_dir.mkdir()
    dest_dir.mkdir()

    (template_dir / ".env.agent.template").write_text("AGENT=1\n", encoding="utf-8")
    (template_dir / ".env.client.template").write_text("CLIENT=1\n", encoding="utf-8")
    (dest_dir / ".gitignore").write_text("dist\n", encoding="utf-8")

    ensure_env_files(str(template_dir), str(dest_dir))
    ensure_gitignore_entries(str(dest_dir))

    assert (dest_dir / ".env.agent").read_text(encoding="utf-8") == "AGENT=1\n"
    assert (dest_dir / ".env.client").read_text(encoding="utf-8") == "CLIENT=1\n"

    gitignore = (dest_dir / ".gitignore").read_text(encoding="utf-8")
    assert ".env.agent" in gitignore
    assert ".env.client" in gitignore
