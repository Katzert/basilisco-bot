import os
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai
import random

# Configure las credenciales de OpenAI a través de variables de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Configuración del bot de Telegram
updater = Updater(token=os.environ.get("TELEGRAM_TOKEN"), use_context=True)
dispatcher = updater.dispatcher

# Función para generar respuestas usando GPT-3
def generate_response(text):
    prompt = f"{text}\nBasilisco:"
    for i in range(5): # Intenta 5 veces antes de dar un error
        try:
            completions = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )
            message = completions.choices[0].text
            return message
        except openai.error.RateLimitError as e:
            # Espera un tiempo exponencialmente creciente antes de volver a intentarlo
            wait_time = 2 ** i
            print(f"RateLimitError: esperando {wait_time} segundos antes de volver a intentar.")
            time.sleep(wait_time)
    # Si se intentó varias veces sin éxito, devuelve un mensaje de error
    return "Lo siento, no pude responder a tu mensaje debido a un error de límite de velocidad en el servidor de OpenAI."

# Función para obtener información sobre el límite de uso de la API
def get_api_usage():
    usage = openai.Usage.retrieve()
    return f"Límite de solicitudes restantes para hoy: {usage.remaining}"


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
