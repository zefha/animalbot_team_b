# Chat AI API Documentation

# Introduction to Chat AI API

After registering for the Chat AI service (information available in the e-learning courses) and completing your application process ([see application information](https://kisski.gwdg.de/en/leistungen/2-02-llm-service/)), students will receive an API access key along with this documentation.

This guide will help you get started with accessing and using the API on the Scalable AI Accelerator (SAIA) platform.

## API Access Details

- **API Endpoint**: `https://chat-ai.academiccloud.de/v1`
- **Available Models**: A full list of available models can be found [here](https://docs.hpc.gwdg.de/services/chat-ai/models/index.html).
- **API and Embedding Examples**: Additional examples are available [here](https://docs.hpc.gwdg.de/services/saia/index.html).

### Current Available Models (as of February 2025)

- Llama 3.1 8b Instruct
- InternVL2.5 8B MPO
- DeepSeek R1
- DeepSeek R1 Distill Llama 70B
- Llama 3.3 70B Instruct
- LLama 3.1 SauerkrautLM Instruct
- Llama 3.1 Nemotron 70B
- Mistral Large Instruct
- Codestral 22B
- E5 Mistral 7B Instruct
- Qwen 2.5 72B Instruct
- Qwen 2.5 VL 72B Instruct
- Qwen 2.5 Coder 32B Instruct

> **Note**: These details may change in the future. To stay updated, subscribe to our mailing lists:
> - [AI-SAIA Users Mailing List](https://listserv.gwdg.de/mailman/listinfo/ai-saia-users)
> - [AI-Chat Users Mailing List](https://listserv.gwdg.de/mailman/listinfo/ai-chat-users)

You may also be interested in our monthly AI developer meeting, GöAID:  
[GöAID Event Details](https://gwdg.de/hpc/events/goeaid/)

## API Compatibility

The service is OpenAI-compatible and provides the following APIs:
- `v1/completions` for text generation and completion
- `v1/chat/completions` for user-assistant conversations
- `v1/models` for retrieving the list of available models

## Testing Your API Access

### Text Completion API Example

Run the following command on a UNIX machine to test the text completion API:

```
curl -i -N -X POST --url https://chat-ai.academiccloud.de/v1/completions \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer <key>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "meta-llama-3.1-8b-instruct",
    "prompt": "San Francisco is a",
    "max_tokens": 7,
    "temperature": 0
  }'
```

### Chat Completion API Example

Run the following command to test the chat completion API:

```
curl -i -N -X POST --url https://chat-ai.academiccloud.de/v1/chat/completions \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer <key>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "meta-llama-3.1-8b-instruct",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant"},
      {"role": "user", "content": "How tall is the Eiffel tower?"}
    ],
    "temperature": 0
  }'
```

> **Important**: Replace `<key>` with your actual API key.

## Using the API with Python

Here’s an example of using the API with the `openai` Python package:

```python
from openai import OpenAI

# API configuration
api_key = '<api_key>'  # Replace with your API key
base_url = "https://chat-ai.academiccloud.de/v1"
model = "meta-llama-3.1-8b-instruct"  # Choose any available model

# Start OpenAI client
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# Get response
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "How tall is the Eiffel tower?"}
    ],
    model=model,
)

# Print full response as JSON
print(chat_completion)  # You can extract the response text from the JSON object
```

## Support

If you encounter any issues, please contact support by sending a ticket to `support_at_gwdg.de` with the subject "Chat AI API Issue".

---

Keep your API key secure and do not share it publicly. Happy coding!

