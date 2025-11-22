import pytest
from unittest.mock import Mock
from langchain_core.language_models import LanguageModelLike
from services.git_service import GitService
from services.summarize_service import SummarizeService
from agents.agent import Agent


@pytest.fixture
def summarize_service() -> SummarizeService:
    return SummarizeService()


@pytest.fixture
def git_service() -> GitService:
    return GitService()


@pytest.fixture
def mock_model() -> Mock:
    return Mock(spec=LanguageModelLike)


@pytest.fixture
def agent(mock_model: Mock) -> Agent:
    return Agent(model=mock_model, tools=[])
