





from typing import Any, Optional

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider



def create_agent(model_name: str, 
                system_prompt: str, 
                api_key: str,
                provider_kwargs: Optional[dict[str, Any]] = None) -> Agent:
    """Simple function to create an agent with custom parameters"""
    provider_params = {"api_key": api_key}
    if provider_kwargs:
        provider_params.update(provider_kwargs)
    
    model = OpenAIModel(
        model_name,
        provider=OpenRouterProvider(**provider_params)
    )
    
    return Agent(
        model=model,
        system_prompt=system_prompt,
    )