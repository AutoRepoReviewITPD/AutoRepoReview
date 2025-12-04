from unittest.mock import Mock, patch

from pytest import CaptureFixture

from app import __main__ as main


def test_summary_function_prints_changes(capsys: CaptureFixture[str]) -> None:
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.return_value = "Test summary"

    with (
        patch.object(main.git_service, "get_diff", return_value="test diff"),
        patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
    ):
        main.summary("path", "commitA", "commitB")
    captured = capsys.readouterr()
    assert type(captured.out) is str
    mock_summarize_service.summarize.assert_called_once_with("test diff")
