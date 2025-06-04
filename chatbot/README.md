# Animalbot Chatbot

This is the chatbot component of the Animalbot project, which simulates conversations as either a duck or a fox based on user interaction.

## Features

- Dynamically switches between duck and fox personalities
- Uses LLMs from chat-ai.academiccloud.de
- Logs conversation history and classification details

## Running Locally

To run the chatbot locally without Docker:

1. Make sure you have Python 3.8+ installed
2. Create a `.env` file in the project root with your API key
3. Run:
   ```bash
   cd ..  # Go to project root
   python -m chatbot.animalbot
   ```

For Docker-based deployment, see the main project README.