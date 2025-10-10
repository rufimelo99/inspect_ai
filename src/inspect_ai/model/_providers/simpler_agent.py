import os
import requests
from .._generate_config import GenerateConfig
from .openai_compatible import OpenAICompatibleAPI


class SimplerAgentAPI(OpenAICompatibleAPI):
    def __init__(
        self,
        model_name: str,
        base_url: str | None = None,
        api_key: str | None = None,
        config: GenerateConfig = GenerateConfig(),
    ) -> None:
        self.endpoint = os.getenv("SIMPLER_AGENT_ENDPOINT", None)
        if self.endpoint is None:
            raise ValueError("SIMPLER_AGENT_ENDPOINT environment variable not set. Please set it up with `export SIMPLER_AGENT_ENDPOINT=http://localhost:8000`")

        super().__init__(
            model_name=self.assess_model_server() or "Unknown Simpler Agent Model",
            base_url=base_url,
            api_key=api_key or "simpler_agent",
            config=config,
            service="simpler_agent",
            service_base_url=self.endpoint+"/v1",
        )

    def assess_model_server(self):
        """Start local model server if using local model."""

        # Checks if server is already running.
        try:
            response = requests.get(f"{self.endpoint}/llm", timeout=2)
            if response.status_code == 200:
                data = response.json()
                return data.get("model", "unknown")
        except:
            pass

        raise RuntimeError("Failed to start model server")
