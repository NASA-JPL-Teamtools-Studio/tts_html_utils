from pathlib import Path

import pytest

from tts_utilities.inspection import check_inspection_hash

from tts_html_utils.core.components.table import PowerTable
from tts_html_utils.core.compiler import HtmlCompiler


_ARTIFACT_PATH = Path(__file__).parent / "test_files" / "power_table_pagination_inspection.html"


@pytest.mark.inspection
@pytest.mark.unreviewed_ai
class TestPowerTablePaginationInspection:
    """Generate a PowerTable artifact for human inspection in a browser."""

    def test_write_pagination_inspection_html(self):
        rows = [
            {
                "id": index,
                "severity": "WARNING" if index % 3 == 0 else "INFO",
                "message": f"EVR message {index}",
            }
            for index in range(60)
        ]
        table = PowerTable(
            column_fields=["id", "severity", "message"],
            row_data=rows,
            add_filters="local",
            add_sorting="local",
            add_pagination=True,
            page_size=25,
        )
        table.add_header(["id", "severity", "message"])

        _ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
        compiler = HtmlCompiler("PowerTable Pagination Inspection")
        compiler.add_body_component(table)
        compiler.render_to_file(_ARTIFACT_PATH)

        print(
            "\n\n  Human-inspectable output -> open in browser:\n"
            f"  {_ARTIFACT_PATH.resolve()}\n"
        )
        assert _ARTIFACT_PATH.exists()
        assert _ARTIFACT_PATH.stat().st_size > 0
        content = _ARTIFACT_PATH.read_text()
        assert "Rows per page:" in content
        assert "let pageSize = 25" in content
        assert "EVR message 59" in content
        check_inspection_hash(_ARTIFACT_PATH)
