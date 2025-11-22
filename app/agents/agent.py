from typing import Sequence
from uuid import uuid4
from langchain_core.language_models import LanguageModelLike
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig


class Agent:
    def __init__(self, model: LanguageModelLike, tools: Sequence[BaseTool]) -> None:
        self.model = model
        self.agent = create_react_agent(
            model,
            tools,
            checkpointer=InMemorySaver(),
        )
        self.config: RunnableConfig = {"configurable": {"thread_id": uuid4().hex}}

    def invoke(self, content: str, temperature: float = 0.1) -> str:
        message = {
            "role": "user",
            "content": content,
        }

        return self.agent.invoke(
            {
                "messages": [message],
                "temperature": temperature,
            },
            config=self.config,
        )["messages"][-1].content
