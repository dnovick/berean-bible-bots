"""Behavioral test for bible_grammar.exercise_pdf.__main__ — the
"regenerate all PDFs" entry point (`python3 -m bible_grammar.exercise_pdf`).

This module has NO `if __name__ == '__main__':` guard: every name it
imports is unconditionally called at module scope the moment it is
imported. Actually importing/running it here would trigger ~180 real
PDF builds into the real, git-tracked lesson exercise directories —
never do that in a test.

Instead, this statically parses the module's source (via `ast`, without
importing it) to extract every function name it imports from bbh/bbg/bba,
then verifies each one is a real, callable attribute of the corresponding
module — a regression guard against a typo'd or removed builder name
silently breaking the regeneration script, without ever executing it.
"""

import ast
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

_MAIN_PY = (
    Path(__file__).resolve().parents[2] / "src" / "bible_grammar"
    / "exercise_pdf" / "__main__.py"
)

_REPORTLAB_AVAILABLE = True
try:
    import reportlab  # noqa: F401
except ImportError:
    _REPORTLAB_AVAILABLE = False


def _skip_if_missing() -> None:
    if not _REPORTLAB_AVAILABLE:
        pytest.skip("reportlab not installed (exercise_pdf builders need it)")


def _imported_names_by_module() -> dict[str, list[str]]:
    tree = ast.parse(_MAIN_PY.read_text(encoding='utf-8'))
    by_module: dict[str, list[str]] = {}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module in ('bbh', 'bbg', 'bba'):
            by_module.setdefault(node.module, []).extend(
                alias.name for alias in node.names
            )
    return by_module


class TestMainModuleNeverAutoRunsAtCollection:
    def test_ast_parse_does_not_import_or_execute(self) -> None:
        # Sanity check on the test's own approach: parsing must not touch
        # sys.modules for bible_grammar.exercise_pdf.__main__.
        _imported_names_by_module()
        assert 'bible_grammar.exercise_pdf.__main__' not in sys.modules


class TestBuilderManifestConsistency:
    def test_every_imported_builder_name_is_a_real_callable(self) -> None:
        _skip_if_missing()
        by_module = _imported_names_by_module()
        assert set(by_module.keys()) == {'bbh', 'bbg', 'bba'}
        assert len(by_module['bbh']) >= 100
        assert len(by_module['bbg']) >= 30
        assert len(by_module['bba']) >= 20

        for mod_name, names in by_module.items():
            mod = __import__(
                f'bible_grammar.exercise_pdf.{mod_name}', fromlist=[mod_name]
            )
            for name in names:
                fn = getattr(mod, name, None)
                assert fn is not None, f"{mod_name}.{name} does not exist"
                assert callable(fn), f"{mod_name}.{name} is not callable"
