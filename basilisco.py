import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai
import random

# Configure las credenciales de OpenAI a través de variables de entorno
openai.api_key = os.environ.get("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")

# Configuración del bot de Telegram
updater = Updater(token=os.environ.get("6146493597:AAH9jS7kG7bTXYquy51ajw45VeMrLRROehE"), use_context=True)
dispatcher = updater.dispatcher

# Función para generar respuestas usando GPT-3
def generate_response(text):
    prompt = f"{text}\nBasilisco:"
    completions = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = completions.choices[0].text
    return message

# Función para manejar el comando /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy Basilisco, tu asistente personal de chat. ¿En qué puedo ayudarte?")

# Función para manejar los mensajes recibidos
def message(update, context):
    # Obtiene el texto del mensaje
    text = update.message.text
    # Genera una respuesta usando GPT-3
    response = generate_response(text)
    # Envía la respuesta al usuario
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Manejadores de eventos
start_handler = CommandHandler("start", start)
message_handler = MessageHandler(Filters.text & (~Filters.command), message)

# Registramos los manejadores de eventos en el despachador
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

# Iniciamos el bot
updater.start_polling()
