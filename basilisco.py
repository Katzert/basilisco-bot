import logging
import os
import time
import telegram
import openai

# Configurar el bot de Telegram y la API de OpenAI
telegram_token = os.environ.get('TELEGRAM_TOKEN')
openai.api_key = os.environ.get('OPENAI_API_KEY')
bot = telegram.Bot(token=telegram_token)

# Configurar el registro de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

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
            rate_limits = openai.api_requestor.get_rate_limits()
            logger.info(f"Límite de OpenAI: {rate_limits}")
            return message
        except openai.error.RateLimitError as e:
            # Espera un tiempo exponencialmente creciente antes de volver a intentarlo
            wait_time = 2 ** i
            logger.warning(f"RateLimitedError: esperando {wait_time} segundos antes de volver a intentar.")
            time.sleep(wait_time)
    # Si se intentó varias veces sin éxito, devuelve un mensaje de error
    logger.error("Error de límite de velocidad de OpenAI.")
    return "Lo siento, no pude responder a tu mensaje debido a un error de límite de velocidad en el servidor de OpenAI."

# Función para manejar los mensajes recibidos
def message(update, context):
    text = update.message.text
    logger.info(f"Mensaje recibido: {text}")
    response = generate_response(text)
    logger.info(f"Respuesta generada: {response}")
    update.message.reply_text(response)

# Configurar el Dispatcher del bot de Telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher

# Añadir los handlers
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))

# Iniciar el bot
logger.info("Iniciando el bot...")
updater.start_polling()

# Esperar a que se reciban mensajes
updater.idle()
