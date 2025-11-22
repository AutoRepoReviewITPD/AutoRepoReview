from services.git_service import GitService


def test_get_diff(
    git_service: GitService,
) -> None:
    diff = git_service.get_diff(".", "HEAD", "HEAD~1")
    assert isinstance(diff, str)
