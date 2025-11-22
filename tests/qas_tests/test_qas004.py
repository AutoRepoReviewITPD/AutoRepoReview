# Link: https://github.com/AutoRepoReviewITPD/AutoRepoReview/blob/main/docs/requirements/quality-requirements.md#qast004-1

import main


def test_qas004_1(
    cloned_repo: str,
) -> None:
    main.summary(cloned_repo, "HEAD", "HEAD~1")
