from unittest.mock import patch
from uuid import uuid4
from services.summarize_service import SummarizeService


def test_formulating_prompt(
    summarize_service: SummarizeService,
) -> None:
    diff = str(uuid4())
    prompt = summarize_service.prepare_prompt(diff)

    assert (
        prompt
        == f"""
            Below is the result of running 'git diff A B'. 
            Please summarize the changes made between these two commits, 
            focusing on modified files, added or removed lines, 
            and any significant functional updates or refactorings.
            Also summarize the changes for each person that contributed.
                
            Rules:
                1. Return only a text with summary
            
            -----------
            {diff}
            -----------
        """
    ), prompt


def test_summarize(
    summarize_service: SummarizeService,
) -> None:
    diff = "diff --git a/file.txt b/file.txt\nindex 83db48f..f735c2d 100644\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1,2 @@\n-Hello World\n+Hello, World!\n+This is a new line."
    with patch.object(
        summarize_service.agent,
        "invoke",
        return_value="Summary of changes",
    ) as mock_invoke:
        summary = summarize_service.summarize(diff)
        mock_invoke.assert_called_with(
            summarize_service.prepare_prompt(diff)
        )

    assert isinstance(summary, str)
    assert len(summary) > 0
