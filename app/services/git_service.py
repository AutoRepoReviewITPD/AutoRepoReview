import os


class GitService:
    def _call_os(self, command: str) -> str:
        return os.popen(command).read()

    def get_diff(self, path: str, start_commit: str, end_commit: str) -> str:
        os.chdir(path)
        return self._call_os(f"git diff {start_commit} {end_commit}")

    def get_contributors(self, path: str, start_commit: str, end_commit: str) -> str:
        os.chdir(path)
        command = (
            f'git log {start_commit}..{end_commit} --pretty=format:"%an|%s" --no-merges'
        )
        output = self._call_os(command)

        if not output.strip():
            return ""

        contributors: dict[str, list[str]] = {}
        for line in output.strip().split("\n"):
            if "|" in line:
                author, message = line.split("|", 1)
                author = author.strip()
                if author not in contributors:
                    contributors[author] = []
                contributors[author].append(message.strip())

        result = []
        for author, messages in contributors.items():
            result.append(f"- {author}: {len(messages)} commit(s)")

        return "\n".join(result)

    def clone(self, repo_url: str, clone_path: str) -> None:
        self._call_os(f"git clone {repo_url} {clone_path}")
