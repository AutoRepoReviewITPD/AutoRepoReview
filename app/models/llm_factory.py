import os

from dotenv import load_dotenv
from langchain_core.language_models import LanguageModelLike
from langchain_gigachat.chat_models import GigaChat
from langchain_openai import ChatOpenAI

from ..config import config

load_dotenv()


class LLMFactory:
    """Factory for creating LLM models based on configuration."""

    @staticmethod
    def create_llm() -> LanguageModelLike:
        """Creates LLM based on saved configuration or environment variables."""
        model_config = config.get_model_config()

        # Backward compatibility: check environment variables
        if model_config is None:
            gigachat_credentials = os.getenv("GIGACHAT_CREDENTIALS")
            if gigachat_credentials:
                return GigaChat(
                    model="GigaChat-2-Max",
                    credentials=gigachat_credentials,
                    verify_ssl_certs=False,
                )
            raise ValueError(
                "Model is not configured. Use the 'configure' command to set up "
                "or set the GIGACHAT_CREDENTIALS environment variable."
            )

        api_url = model_config["api_url"]
        api_key = model_config.get("api_key")
        model_name = model_config.get("model_name", "")

        if not api_key:
            raise ValueError(
                "API key not found. Use the 'configure' command to set up."
            )

        return ChatOpenAI(
            model=model_name or "gpt-4",
            api_key=api_key,
            base_url=api_url,
        )

