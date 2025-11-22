import pytest
from services.summarize_service import SummarizeService


@pytest.fixture
def summarize_service() -> SummarizeService:
    return SummarizeService()
