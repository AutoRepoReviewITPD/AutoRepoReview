class SummarizeService:
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
