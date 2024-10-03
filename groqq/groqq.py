import os
from langchain_groq import ChatGroq
from ..base import VannaBase

class Groq(VannaBase):
    def __init__(self, config=None):
        if config is None:
            raise ValueError(
                "For Groq, config must be provided with an api_key and model"
            )
        if "api_key" not in config:
            raise ValueError("config must contain a Groq api_key")
        if "model" not in config:
            raise ValueError("config must contain a Groq model")
        
        api_key = config["api_key"]
        model = config["model"]
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model,
            #temperature=0.2
        )

    def system_message(self, message: str) -> any:
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> any:
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> any:
        return {"role": "assistant", "content": message}

    def generate_sql(self, question: str, **kwargs) -> str:
        # Use the super generate_sql
        sql = super().generate_sql(question, **kwargs)
        # Replace "\_" with "_"
        sql = sql.replace("\\_", "_")
        return sql

    def submit_prompt(self, prompt, **kwargs) -> str:
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in prompt]
        response = self.llm.invoke(messages)
        return response.content