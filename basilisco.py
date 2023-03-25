import telegram
from telegram.ext import Updater, MessageHandler, Filters
import openai
import os

# Set the OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = "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"

# Create a Telegram bot object
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telegram.Bot(token="6146493597:AAHnZAfCSrrY2Mm-8SIBLxu-61MRxH7RDV0")

# Define a function to generate a response using ChatGPT
def generate_response(text):
    prompt = f"Me: {text}\nBasilisco:"
    response = openai.Completion.create(
        engine="davinci", prompt=prompt, max_tokens=50, n=1, stop=None, temperature=0.7
    ).choices[0].text
    return response.strip()

# Define a function to handle incoming messages
def handle_message(update, context):
    # Get the user's message
    user_message = update.message.text

    # Generate a response using ChatGPT
    bot_response = generate_response(user_message)

    # Send the response back to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)

# Create an updater and attach the message handler
updater = Updater(token="6146493597:AAHnZAfCSrrY2Mm-8SIBLxu-61MRxH7RDV0", use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Start the bot
updater.start_polling()

# Inform the user that the bot is running
print("Basilisco está corriendo...")

# Limitaciones de OpenAI
print("Tenga en cuenta que Basilisco tiene un límite de solicitudes por mes con OpenAI.")

# Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
updater.idle()

