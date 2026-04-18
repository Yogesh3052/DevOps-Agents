from strands import Agent
from strands.models.gemini import GeminiModel
from strands_tools import http_request

model = GeminiModel(
    client_args={
        "api_key": "YOUR_API",
    },
    # **model_config
    model_id="gemini-3.1-flash-lite-preview",
    params={
        # some sample model parameters
        "temperature": 0.7,
        "max_output_tokens": 2048,
        "top_p": 0.9,
        "top_k": 40
    }
)

agent = Agent(model=model, tools=[http_request])
response = agent("What is 2+2")
print(response)
