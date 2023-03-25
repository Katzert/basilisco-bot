import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Configura la API key de OpenAI
openai.api_key = "YOUR_API_KEY"

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
            logging.debug(f"RateLimitedError: esperando {wait_time} segundos antes de volver a intentar.")
            time.sleep(wait_time)
    # Si se intentó varias veces sin éxito, devuelve un mensaje de error
    return "Lo siento, no pude responder a tu mensaje debido a un error de límite de velocidad en el servidor de OpenAI."

# Función para manejar los comandos de inicio del bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy Basilisco, el bot que utiliza GPT-3 para responder a tus mensajes.")

# Función para manejar los mensajes enviados al bot
def message(update, context):
    text = update.message.text
    response = generate_response(text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Configura el updater y los handlers
updater = Updater(token="YOUR_BOT_TOKEN", use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & (~Filters.command), message)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

# Inicia el bot y espera a que se presione Ctrl+C
logging.debug(f"El bot está corriendo en el chat {updater.bot.get_me().username}.")
updater.start_polling()
updater.idle()

# Obtiene el límite actual de llamadas a la API de OpenAI
limits = openai.api_requestor.APIRequestor().get_rate_limits()
remaining = limits["remaining"]
logging.debug(f"Límite actual de llamadas a la API de OpenAI: {remaining}")
