import typer

from .services.git_service import GitService
from .services.summarize_service import SummarizeService

app = typer.Typer()

git_service = GitService()
summarize_service = SummarizeService()


@app.command()
def summary(path: str, start_commit: str, end_commit: str) -> None:
    diff = git_service.get_diff(path, start_commit, end_commit)
    print(summarize_service.summarize(diff))

if __name__ == "__main__":
    app()

