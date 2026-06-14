"""
SentimentBot — A Bot Framework bot that integrates Azure AI Language Service
to perform sentiment analysis on user messages.

Original source: https://github.com/microsoft/BotBuilder-Samples/tree/main/samples/python/02.echo-bot
Reason for copy: Extended the echo bot to add Azure AI Text Analytics sentiment analysis,
capability listing, and graceful handling of malformed input, as required by the course project.
"""

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

HELP_TEXT = """
I'm the **Sentiment Analysis Bot**! Here's what I can do:

🔍 **Analyze Sentiment** — Type any sentence and I'll tell you if it's positive, negative, neutral, or mixed.

📋 **List Capabilities** — Type `help` or `capabilities` to see this menu.

🌡️ **Confidence Scores** — I'll share how confident I am in each sentiment category.

💬 **Multi-sentence support** — Send a paragraph and I'll break down sentiment sentence by sentence.

❓ **Unknown inputs** — If I can't understand your message, I'll let you know gracefully.

Go ahead — tell me how you're feeling today!
"""

GREETING = """
👋 Hello! I'm the **Sentiment Analysis Bot**, powered by Azure AI Language Services.

I can analyze the emotional tone of anything you type — positive, negative, neutral, or mixed.

Type **help** to see all my capabilities, or just start chatting!
"""


class SentimentBot(ActivityHandler):
    """Bot that uses Azure AI Text Analytics to respond with sentiment analysis."""

    def __init__(self, config):
        self.config = config
        self._ai_client = None

        # Initialize Azure AI client if credentials are available
        if config.API_KEY and config.ENDPOINT_URI:
            try:
                credential = AzureKeyCredential(config.API_KEY)
                self._ai_client = TextAnalyticsClient(
                    endpoint=config.ENDPOINT_URI,
                    credential=credential,
                )
                print("[SentimentBot] Azure AI Language client initialized successfully.")
            except Exception as e:
                print(f"[SentimentBot] Warning: Could not initialize Azure AI client: {e}")
        else:
            print(
                "[SentimentBot] Warning: Azure AI credentials not configured. "
                "Set MicrosoftAIServiceEndpoint and MicrosoftAPIKey environment variables."
            )

    async def on_members_added_activity(self, members_added: list, turn_context: TurnContext):
        """Greet new users when they join the conversation."""
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(GREETING)

    async def on_message_activity(self, turn_context: TurnContext):
        """Handle incoming text messages."""
        user_text = (turn_context.activity.text or "").strip()

        # Guard: empty or whitespace-only input
        if not user_text:
            await turn_context.send_activity(
                "It looks like you sent an empty message. "
                "Please type something and I'll analyze its sentiment!"
            )
            return

        # Help / capabilities request
        normalized = user_text.lower()
        if normalized in {"help", "capabilities", "?", "menu", "commands"}:
            await turn_context.send_activity(HELP_TEXT)
            return

        # Greetings
        if normalized in {"hi", "hello", "hey", "howdy", "greetings"}:
            await turn_context.send_activity(
                f"Hey there! Send me a sentence or paragraph and I'll analyze its sentiment. "
                f"Type **help** to see everything I can do."
            )
            return

        # Input too short to be meaningful
        if len(user_text) < 3:
            await turn_context.send_activity(
                f'"{user_text}" is a bit short for me to analyze meaningfully. '
                f"Could you give me a full sentence?"
            )
            return

        # Perform sentiment analysis
        response = await self._analyze_sentiment(user_text, turn_context)
        await turn_context.send_activity(response)

    async def _analyze_sentiment(self, text: str, turn_context: TurnContext) -> str:
        """Call Azure AI and format a response. Falls back gracefully if AI is unavailable."""
        if self._ai_client is None:
            return (
                "⚠️ **AI service not configured.**\n\n"
                "The Azure AI Language service credentials are missing. "
                "Please set the `MicrosoftAIServiceEndpoint` and `MicrosoftAPIKey` "
                "environment variables and restart the bot."
            )

        try:
            documents = [text]
            result = self._ai_client.analyze_sentiment(documents=documents)

            for doc in result:
                if doc.is_error:
                    return (
                        f"⚠️ The AI service returned an error: `{doc.error.code}` — "
                        f"{doc.error.message}\n\nPlease try rephrasing your input."
                    )

                overall = doc.sentiment.capitalize()
                scores = doc.confidence_scores
                emoji = self._sentiment_emoji(doc.sentiment)

                lines = [
                    f"{emoji} **Overall Sentiment: {overall}**\n",
                    f"📊 **Confidence Scores:**",
                    f"- Positive: {scores.positive:.1%}",
                    f"- Neutral:  {scores.neutral:.1%}",
                    f"- Negative: {scores.negative:.1%}",
                ]

                # Sentence-level breakdown (if more than one sentence)
                if len(doc.sentences) > 1:
                    lines.append("\n🔎 **Sentence Breakdown:**")
                    for i, sentence in enumerate(doc.sentences, 1):
                        s_emoji = self._sentiment_emoji(sentence.sentiment)
                        lines.append(
                            f"{i}. {s_emoji} *\"{sentence.text.strip()}\"* — "
                            f"{sentence.sentiment.capitalize()} "
                            f"(pos {sentence.confidence_scores.positive:.0%} / "
                            f"neg {sentence.confidence_scores.negative:.0%})"
                        )

                lines.append(f"\n💡 *Tip: Try a longer paragraph for sentence-by-sentence analysis!*")
                return "\n".join(lines)

        except Exception as e:
            print(f"[SentimentBot] Azure AI call failed: {e}")
            return (
                "⚠️ **Could not reach the AI service.** "
                f"Error: `{type(e).__name__}: {e}`\n\n"
                "Please check your internet connection and Azure credentials."
            )

        return "⚠️ No results returned from the AI service. Please try again."

    @staticmethod
    def _sentiment_emoji(sentiment: str) -> str:
        """Return an emoji that matches the sentiment label."""
        return {
            "positive": "😊",
            "negative": "😟",
            "neutral": "😐",
            "mixed": "😕",
        }.get(sentiment.lower(), "🤔")
