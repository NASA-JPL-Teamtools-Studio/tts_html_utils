"""Review and certify PowerTable inspection artifacts."""

import sys
from pathlib import Path

from tts_utilities.inspection import certify, print_status, render_status_report


TEST_FILES_DIR = Path(__file__).parent / "test_files"
STATUS_REPORT_PATH = TEST_FILES_DIR / "inspection_status.html"


def inspection_artifacts():
    return sorted(
        path for path in TEST_FILES_DIR.glob("*.html")
        if path.name != STATUS_REPORT_PATH.name
    )


def main():
    artifacts = inspection_artifacts()
    if "--certify" in sys.argv:
        targets = [Path(path) for path in sys.argv[1:] if path != "--certify"]
        certify(targets or artifacts)
        return

    if not artifacts:
        print(f"No HTML artifacts found in {TEST_FILES_DIR}")
        return
    certify_command = f"python {Path(__file__).resolve()} --certify"
    print_status(artifacts, certify_command)
    STATUS_REPORT_PATH.write_text(
        render_status_report(artifacts, certify_command), encoding="utf-8"
    )
    print(f"\n  Full dashboard: {STATUS_REPORT_PATH.resolve()}\n")


if __name__ == "__main__":
    main()
