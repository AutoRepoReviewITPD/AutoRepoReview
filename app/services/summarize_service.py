from ..agents.agent import Agent
from ..models.gigachat import llm


class SummarizeService:
    def __init__(self) -> None:
        self.agent = Agent(
            llm,
            tools=[],
        )

    def prepare_prompt(self, diff: str) -> str:
        return f"""
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

    def summarize(self, diff: str) -> str:
        prompt = self.prepare_prompt(diff)
        return self.agent.invoke(prompt)
