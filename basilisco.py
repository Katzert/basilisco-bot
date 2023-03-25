import os
import telegram
import openai
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# Configuración del bot
TELEGRAM_TOKEN = os.environ.get("6146493597:AAH9jS7kG7bTXYquy51ajw45VeMrLRROehE")
OPENAI_API_KEY = os.environ.get("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")
openai.api_key = OPENAI_API_KEY
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Función para manejar el comando /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy Basilisco, un bot de conversación. ¿En qué puedo ayudarte?")

# Función para manejar los mensajes de texto
def message(update, context):
    message_text = update.message.text
    chat_id = update.effective_chat.id

    # Genera una respuesta de ChatGPT
    response = openai.Completion.create(engine="davinci", prompt=message_text, max_tokens=100)["choices"][0]["text"]

    # Envía la respuesta al usuario
    context.bot.send_message(chat_id=chat_id, text=response)

# Manejadores de comandos y mensajes
start_handler = CommandHandler("start", start)
message_handler = MessageHandler(Filters.text & (~Filters.command), message)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

# Inicia el bot
updater.start_polling()
