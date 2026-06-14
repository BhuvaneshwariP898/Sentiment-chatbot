# Sentiment Analysis Chatbot

An AI-integrated chatbot built with the Microsoft Bot Framework and Azure AI Language Services (Text Analytics). This project was created for the *Connecting a Chatbot to an AI-as-a-Service* assignment.

## Origin

This project is adapted from the [Microsoft Bot Framework Python Echo Bot sample](https://github.com/microsoft/BotBuilder-Samples/tree/main/samples/python/02.echo-bot). It was chosen as a starting point because the echo bot provides a minimal but complete Bot Framework scaffold (aiohttp web server, adapter, activity handler) without adding unnecessary complexity. The core bot logic in `bot.py` and the configuration in `config.py` have been significantly extended to add Azure AI Language Service integration, sentiment response formatting, help/capabilities handling, and graceful error handling for malformed input.

## Features

- **Sentiment Analysis** — Uses Azure AI Text Analytics to classify user messages as positive, negative, neutral, or mixed.
- **Confidence Scores** — Displays positive/neutral/negative confidence percentages.
- **Sentence-level breakdown** — For multi-sentence input, each sentence is analyzed individually.
- **Capabilities listing** — Users can type `help` to see what the bot can do.
- **Graceful error handling** — Empty messages, very short input, and AI service failures all return friendly, informative responses.

## Prerequisites

- Python 3.8+
- [Bot Framework Emulator](https://github.com/Microsoft/BotFramework-Emulator/releases)
- An [Azure AI Language Service](https://azure.microsoft.com/en-us/products/ai-services/ai-language/) resource (free tier F0 works)

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Azure credentials

Set the following environment variables **before** starting the bot:

**Windows (Command Prompt):**
```cmd
SET MicrosoftAIServiceEndpoint=https://<your-resource-name>.cognitiveservices.azure.com/
SET MicrosoftAPIKey=<your-key-1-or-key-2>
```

**Linux / macOS:**
```bash
export MicrosoftAIServiceEndpoint=https://<your-resource-name>.cognitiveservices.azure.com/
export MicrosoftAPIKey=<your-key-1-or-key-2>
```

> 🔐 **Never commit API keys to source control.** The `.gitignore` excludes `.env` files.

### 3. Run the bot

```bash
python app.py
```

The bot listens on `http://localhost:3978/api/messages`.

### 4. Connect via Bot Framework Emulator

1. Open Bot Framework Emulator.
2. Click **Open Bot**.
3. Enter `http://localhost:3978/api/messages`.
4. Leave App ID and password blank for local development.
5. Click **Connect**.

## Project Structure

```
├── app.py          # Web server entry point, Bot Framework adapter setup
├── bot.py          # SentimentBot — core message handling and Azure AI calls
├── config.py       # DefaultConfig — reads credentials from environment variables
├── requirements.txt
└── README.md
```

## AI Disclosure

This project was built with assistance from Claude (Anthropic) for code scaffolding, docstring writing, and the accompanying APA report. All code was reviewed, tested, and understood before submission.
