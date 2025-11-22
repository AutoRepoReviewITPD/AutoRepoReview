import pytest
from unittest.mock import Mock
from langchain_core.language_models import LanguageModelLike
from agents.agent import Agent


@pytest.fixture
def mock_model() -> Mock:
    return Mock(spec=LanguageModelLike)


@pytest.fixture
def agent(mock_model: Mock) -> Agent:
    return Agent(model=mock_model, tools=[])
