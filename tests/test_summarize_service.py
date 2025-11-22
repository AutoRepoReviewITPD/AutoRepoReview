from uuid import uuid4
from services.summarize_service import SummarizeService


def test_formulating_prompt(
    summarize_service: SummarizeService,
) -> None:
    diff = str(uuid4())
    prompt = summarize_service.prepare_prompt(diff)

    assert prompt == f"""
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
        """, prompt
