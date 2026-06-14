# Sentiment Analysis Chatbot

An AI-integrated chatbot built with the Microsoft Bot Framework and Azure AI Language Services (Text Analytics). This project was created for the *Connecting a Chatbot to an AI-as-a-Service* assignment.

## Origin

This project is adapted from the [Microsoft Bot Framework Python Echo Bot sample](https://github.com/microsoft/BotBuilder-Samples/tree/main/samples/python/02.echo-bot). It was chosen as a starting point because the echo bot provides a minimal but complete Bot Framework scaffold (aiohttp web server, adapter, activity handler) without adding unnecessary complexity. The core bot logic in `bot.py` and the configuration in `config.py` have been significantly extended to add Azure AI Language Service integration, sentiment response formatting, help/capabilities handling, and graceful error handling for malformed input.

## Features

- **Sentiment Analysis** - Uses Azure AI Text Analytics to classify user messages as positive, negative, neutral, or mixed.
- **Confidence Scores** - Displays positive/neutral/negative confidence percentages.
- **Sentence-level breakdown** - For multi-sentence input, each sentence is analyzed individually.
- **Capabilities listing** - Users can type `help` to see what the bot can do.
- **Graceful error handling** - Empty messages, very short input, and AI service failures all return friendly, informative responses.

## Prerequisites

- Python 3.8+
- [Bot Framework Emulator](https://github.com/Microsoft/BotFramework-Emulator/releases)
- An [Azure AI Language Service](https://azure.microsoft.com/en-us/products/ai-services/ai-language/) resource (free tier F0 works)

## AI Disclosure

This project was built with assistance from Claude (Anthropic) for code scaffolding, docstring writing, and the accompanying APA report. All code was reviewed, tested, and understood before submission.
