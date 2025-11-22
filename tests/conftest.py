import pytest

from services.git_service import GitService
from services.summarize_service import SummarizeService


@pytest.fixture
def summarize_service() -> SummarizeService:
    return SummarizeService()


@pytest.fixture
def git_service() -> GitService:
    return GitService()
