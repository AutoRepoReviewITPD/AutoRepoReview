from unittest.mock import patch

from pytest import CaptureFixture

from app import __main__ as main


def test_summary_function_prints_changes(capsys: CaptureFixture[str]) -> None:
    with (
        patch.object(main.git_service, "get_diff"),
        patch.object(main.summarize_service, "summarize"),
    ):
        main.summary("path", "commitA", "commitB")
    captured = capsys.readouterr()
    assert type(captured.out) is str
