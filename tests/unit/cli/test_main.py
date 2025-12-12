from unittest.mock import Mock, patch

import pytest
from pytest import CaptureFixture
import typer
from rich.markdown import Markdown

from app import __main__ as main


def test_summary_function_prints_changes(capsys: CaptureFixture[str]) -> None:
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.return_value = "Test summary"
    mock_summarize_service.get_token_count.return_value = 100
    mock_git_service = Mock()
    mock_git_service.get_diff.return_value = "test diff"

    try:
        with (
            patch("app.__main__.git_service", mock_git_service),
            patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
            patch("app.__main__.typer.confirm", return_value=True),
            patch("app.__main__.console.print"),
        ):
            main.summary("path", "commitA", "commitB")
    except typer.Exit as e:
        # If exit code is 0, that's fine (user cancelled)
        # If exit code is 1, something went wrong
        if e.exit_code != 0:
            raise
    captured = capsys.readouterr()
    assert type(captured.out) is str
    # Verify summarize was called with the diff as first argument
    mock_summarize_service.summarize.assert_called_once()
    call_args = mock_summarize_service.summarize.call_args
    assert call_args[0][0] == "test diff"


def test_summary_with_contributors_calls_get_contributors(
    capsys: CaptureFixture[str],
) -> None:
    """Test that get_contributors is called when contributors flag is True."""
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.return_value = "Test summary with contributors"
    mock_summarize_service.get_token_count.return_value = 150
    mock_git_service = Mock()
    mock_git_service.get_diff.return_value = "test diff"
    mock_git_service.get_contributors.return_value = (
        "- Alice: 2 commit(s)\n- Bob: 1 commit(s)"
    )

    try:
        with (
            patch("app.__main__.git_service", mock_git_service),
            patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
            patch("app.__main__.typer.confirm", return_value=True),
            patch("app.__main__.console.print"),
        ):
            main.summary("path", "commitA", "commitB", contributors=True)
    except typer.Exit as e:
        if e.exit_code != 0:
            raise

    # Verify get_contributors was called
    mock_git_service.get_contributors.assert_called_once_with(
        "path", "commitA", "commitB"
    )

    # Verify get_token_count was called with contributors_info
    mock_summarize_service.get_token_count.assert_called_once()
    token_call_args = mock_summarize_service.get_token_count.call_args
    assert token_call_args[0][0] == "test diff"
    assert token_call_args[0][1] == "- Alice: 2 commit(s)\n- Bob: 1 commit(s)"

    # Verify summarize was called with contributors_info
    mock_summarize_service.summarize.assert_called_once()
    summarize_call_args = mock_summarize_service.summarize.call_args
    assert summarize_call_args[0][0] == "test diff"
    assert summarize_call_args[0][1] == "- Alice: 2 commit(s)\n- Bob: 1 commit(s)"


def test_summary_without_contributors_does_not_call_get_contributors(
    capsys: CaptureFixture[str],
) -> None:
    """Test that get_contributors is not called when contributors flag is False."""
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.return_value = "Test summary"
    mock_summarize_service.get_token_count.return_value = 100
    mock_git_service = Mock()
    mock_git_service.get_diff.return_value = "test diff"

    try:
        with (
            patch("app.__main__.git_service", mock_git_service),
            patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
            patch("app.__main__.typer.confirm", return_value=True),
            patch("app.__main__.console.print"),
        ):
            main.summary("path", "commitA", "commitB", contributors=False)
    except typer.Exit as e:
        if e.exit_code != 0:
            raise

    # Verify get_contributors was not called
    mock_git_service.get_contributors.assert_not_called()

    # Verify get_token_count was called with None for contributors_info
    mock_summarize_service.get_token_count.assert_called_once()
    token_call_args = mock_summarize_service.get_token_count.call_args
    assert token_call_args[0][0] == "test diff"
    assert token_call_args[0][1] is None

    # Verify summarize was called with None for contributors_info
    mock_summarize_service.summarize.assert_called_once()
    summarize_call_args = mock_summarize_service.summarize.call_args
    assert summarize_call_args[0][0] == "test diff"
    assert summarize_call_args[0][1] is None


def test_summary_prints_markdown_output(capsys: CaptureFixture[str]) -> None:
    """Test that console.print is called with Markdown object."""
    mock_summarize_service = Mock()
    summary_text = "# Summary\n\nThis is a **test** summary."
    mock_summarize_service.summarize.return_value = summary_text
    mock_summarize_service.get_token_count.return_value = 100
    mock_git_service = Mock()
    mock_git_service.get_diff.return_value = "test diff"

    try:
        with (
            patch("app.__main__.git_service", mock_git_service),
            patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
            patch("app.__main__.typer.confirm", return_value=True),
            patch("app.__main__.console.print") as mock_console_print,
        ):
            main.summary("path", "commitA", "commitB")
    except typer.Exit as e:
        if e.exit_code != 0:
            raise

    # Verify console.print was called twice: once with newline, once with Markdown
    assert mock_console_print.call_count == 2

    # First call should be with newline
    first_call = mock_console_print.call_args_list[0]
    assert first_call[0][0] == "\n"

    # Second call should be with Markdown object
    second_call = mock_console_print.call_args_list[1]
    assert isinstance(second_call[0][0], Markdown)
    assert second_call[0][0].markup == summary_text


def test_summary_handles_value_error(capsys: CaptureFixture[str]) -> None:
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.side_effect = ValueError("Config error")
    mock_summarize_service.get_token_count.return_value = 100
    mock_git_service = Mock()
    mock_git_service.get_diff.return_value = "test diff"

    with (
        patch("app.__main__.git_service", mock_git_service),
        patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
        patch("app.__main__.typer.confirm", return_value=True),
        pytest.raises(typer.Exit) as exc_info,
    ):
        main.summary("path", "commitA", "commitB")

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert "Configuration error: Config error" in captured.err


def test_summary_handles_connection_error(capsys: CaptureFixture[str]) -> None:
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.side_effect = ConnectionError("Connection failed")
    mock_summarize_service.get_token_count.return_value = 100
    mock_git_service = Mock()
    mock_git_service.get_diff.return_value = "test diff"

    with (
        patch("app.__main__.git_service", mock_git_service),
        patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
        patch("app.__main__.typer.confirm", return_value=True),
        pytest.raises(typer.Exit) as exc_info,
    ):
        main.summary("path", "commitA", "commitB")

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert "Connection error: Connection failed" in captured.err


def test_summary_handles_runtime_error(capsys: CaptureFixture[str]) -> None:
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.side_effect = RuntimeError("Runtime error")
    mock_summarize_service.get_token_count.return_value = 100
    mock_git_service = Mock()
    mock_git_service.get_diff.return_value = "test diff"

    with (
        patch("app.__main__.git_service", mock_git_service),
        patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
        patch("app.__main__.typer.confirm", return_value=True),
        pytest.raises(typer.Exit) as exc_info,
    ):
        main.summary("path", "commitA", "commitB")

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert "Error: Runtime error" in captured.err


def test_summary_handles_unexpected_error(capsys: CaptureFixture[str]) -> None:
    mock_summarize_service = Mock()
    mock_summarize_service.summarize.side_effect = KeyError("Unexpected error")
    mock_summarize_service.get_token_count.return_value = 100
    mock_git_service = Mock()
    mock_git_service.get_diff.return_value = "test diff"

    with (
        patch("app.__main__.git_service", mock_git_service),
        patch("app.__main__.SummarizeService", return_value=mock_summarize_service),
        patch("app.__main__.typer.confirm", return_value=True),
        pytest.raises(typer.Exit) as exc_info,
    ):
        main.summary("path", "commitA", "commitB")

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert "Unexpected error: 'Unexpected error'" in captured.err


def test_configure_with_empty_api_key(capsys: CaptureFixture[str]) -> None:
    with (
        patch("app.__main__.getpass.getpass", return_value=""),
        pytest.raises(typer.Exit) as exc_info,
    ):
        main.configure("https://api.openai.com/v1", "")

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert "Error: API key cannot be empty" in captured.err


def test_configure_success(capsys: CaptureFixture[str]) -> None:
    with (
        patch("app.__main__.getpass.getpass", return_value="test-key"),
        patch("app.__main__.config.set_model_config") as mock_set_config,
    ):
        main.configure("https://api.openai.com/v1", "gpt-4")

    mock_set_config.assert_called_once_with(
        "https://api.openai.com/v1", "test-key", "gpt-4"
    )
    captured = capsys.readouterr()
    assert "Configuration saved successfully!" in captured.out


def test_configure_handles_exception(capsys: CaptureFixture[str]) -> None:
    with (
        patch("app.__main__.getpass.getpass", return_value="test-key"),
        patch(
            "app.__main__.config.set_model_config", side_effect=Exception("Save failed")
        ),
        pytest.raises(typer.Exit) as exc_info,
    ):
        main.configure("https://api.openai.com/v1", "")

    assert exc_info.value.exit_code == 1
    captured = capsys.readouterr()
    assert "Error saving configuration: Save failed" in captured.err


def test_show_config_when_not_configured(capsys: CaptureFixture[str]) -> None:
    with patch("app.__main__.config.get_model_config", return_value=None):
        main.show_config()

    captured = capsys.readouterr()
    assert (
        "Model is not configured. Use the 'configure' command to set up."
        in captured.out
    )


def test_show_config_with_model_name(capsys: CaptureFixture[str]) -> None:
    config = {
        "api_url": "https://api.openai.com/v1",
        "api_key": "test-key",
        "model_name": "gpt-4",
    }
    with patch("app.__main__.config.get_model_config", return_value=config):
        main.show_config()

    captured = capsys.readouterr()
    assert "API URL: https://api.openai.com/v1" in captured.out
    assert "Model name: gpt-4" in captured.out


def test_show_config_without_model_name(capsys: CaptureFixture[str]) -> None:
    config = {
        "api_url": "https://api.openai.com/v1",
        "api_key": "test-key",
    }
    with patch("app.__main__.config.get_model_config", return_value=config):
        main.show_config()

    captured = capsys.readouterr()
    assert "API URL: https://api.openai.com/v1" in captured.out
    assert "Model name:" not in captured.out
