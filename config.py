"""
Configuration for the AI-integrated chatbot.
Original source: https://github.com/microsoft/BotBuilder-Samples/tree/main/samples/python/02.echo-bot
Reason for copy: Extended DefaultConfig to include Azure AI Language Service credentials,
retrieved safely from environment variables rather than hard-coded in source.
"""

import os


class DefaultConfig:
    """Bot Configuration — read from environment variables."""

    # Bot Framework credentials (leave blank for unauthenticated local dev)
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    # --- AI Integration (added for course project) ---
    # Set these via environment variables before running the bot:
    #   Windows:  SET MicrosoftAIServiceEndpoint=https://<your-resource>.cognitiveservices.azure.com/
    #             SET MicrosoftAPIKey=<your-key>
    #   Linux/Mac: export MicrosoftAIServiceEndpoint=https://<your-resource>.cognitiveservices.azure.com/
    #              export MicrosoftAPIKey=<your-key>
    ENDPOINT_URI = os.environ.get("MicrosoftAIServiceEndpoint", "")
    API_KEY = os.environ.get("MicrosoftAPIKey", "")
