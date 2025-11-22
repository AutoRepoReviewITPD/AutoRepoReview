# Link: https://github.com/AutoRepoReviewITPD/AutoRepoReview/blob/main/docs/requirements/quality-requirements.md#qast004-1

import main
from services.git_service import GitService


def test_qas004_1(
    git_service: GitService,
) -> None:
    repo = "https://github.com/ilnarkhasanov/AiToHuman"
    clone_path = "/tmp/repo"
    git_service.clone(repo, clone_path)

    main.summary(clone_path, "HEAD", "HEAD~1")
