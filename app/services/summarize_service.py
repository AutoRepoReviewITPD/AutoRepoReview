from opentelemetry import trace
import tiktoken

from ..agents.agent import Agent
from ..models.llm_factory import LLMFactory
from ..config import config

tracer = trace.get_tracer(__name__)


class SummarizeService:
    def __init__(self) -> None:
        llm = LLMFactory.create_llm()
        self.agent = Agent(
            llm,
            tools=[],
        )

    def prepare_prompt(self, diff: str, contributors_info: str | None = None) -> str:
        contributors_instruction = ""
        contributors_format = ""
        if contributors_info:
            contributors_instruction = f"""

**Contributors Information:**
{contributors_info}

Please include a **Contributors** section in your summary showing who contributed what changes.
"""
            contributors_format = (
                "\n\n**Contributors:**\n- [List contributors and their contributions]"
            )

        return f"""Analyze the git diff below and provide a concise summary of the changes.

Focus on:
- Main purpose and high-level changes (what was done and why)
- Key functional changes (new features, bug fixes, refactorings)
- Breaking changes or important updates (if any)

Keep it brief and structured. Do NOT list every file or line change - focus on the big picture.
{contributors_instruction}
Format the response as:
**Summary:** [1-2 sentences about the main purpose]

**Key Changes:**
- [Brief bullet points of important changes]

**Breaking Changes:** [Only if there are any, otherwise omit this section]{contributors_format}

------------
{diff}
------------"""

    def get_token_count(self, diff: str, contributors_info: str | None = None) -> int:
        prompt = self.prepare_prompt(diff, contributors_info)

        model_config = config.get_model_config()
        model_name = (
            model_config.get("model_name", "gpt-4") if model_config else "gpt-4"
        )

        try:
            encoding = tiktoken.encoding_for_model(model_name)
            return len(encoding.encode(prompt))
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(prompt))

    def summarize(self, diff: str, contributors_info: str | None = None) -> str:
        with tracer.start_as_current_span("summarize_service.summarize") as span:
            span.set_attribute("diff_length", len(diff))
            prompt = self.prepare_prompt(diff, contributors_info)
            try:
                with tracer.start_as_current_span("agent.invoke"):
                    result = self.agent.invoke(prompt)
                    span.set_attribute("result_length", len(result))
                    return result
            except Exception as e:
                error_type = type(e).__name__
                error_msg = str(e)

                # Extract meaningful error message
                if "APIConnectionError" in error_type or "Connection" in error_type:
                    raise ConnectionError(
                        f"Failed to connect to API. Please check:\n"
                        f"  - Your internet connection\n"
                        f"  - API URL is correct (use 'show-config' to check)\n"
                        f"  - API server is accessible\n\n"
                        f"Error details: {error_msg}"
                    ) from None
                elif (
                    "AuthenticationError" in error_type
                    or "401" in error_msg
                    or "403" in error_msg
                ):
                    raise ValueError(
                        f"Authentication failed. Please check your API key.\n"
                        f"Use 'configure' command to update your API key.\n\n"
                        f"Error details: {error_msg}"
                    ) from None
                elif (
                    "APIError" in error_type or "400" in error_msg or "429" in error_msg
                ):
                    raise RuntimeError(
                        f"API error occurred. Please check:\n"
                        f"  - API URL and model name are correct\n"
                        f"  - You have sufficient API credits/quota\n"
                        f"  - The model name is valid for your API provider\n\n"
                        f"Error details: {error_msg}"
                    ) from None
                elif isinstance(e, ValueError):
                    raise
                else:
                    # For any other error, show a clean message
                    raise RuntimeError(
                        f"An error occurred while generating summary: {error_msg}"
                    ) from None
