from __future__ import annotations

from naylence.utils.placeholders import build_substitutions, substitute_in_directory


def test_placeholder_substitution(tmp_path):
    file_path = tmp_path / "README.md"
    file_path.write_text(
        "Project: __PROJECT_NAME__\nPackage: __PACKAGE_NAME__\nPy: __PY_PACKAGE__\n",
        encoding="utf-8",
    )

    substitutions = build_substitutions("My App")
    substitute_in_directory(str(tmp_path), substitutions)

    content = file_path.read_text(encoding="utf-8")
    assert "__PROJECT_NAME__" not in content
    assert "__PACKAGE_NAME__" not in content
    assert "__PY_PACKAGE__" not in content
    assert "my-app" in content
    assert "my_app" in content
