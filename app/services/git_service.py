import os


class GitService:
    def get_diff(self, path: str, start_commit: str, end_commit: str) -> str:
        os.chdir(path)
        return os.popen(f"git diff {start_commit} {end_commit}").read()
