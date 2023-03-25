import os
import time
import logging
import telegram
import openai

# Configurar logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar cliente de Telegram
bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])

# Configurar cliente de OpenAI
openai.api_key = os.environ["OPENAI_API_KEY"]


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
            logger.warning(f"RateLimitedError: esperando {wait_time} segundos antes de volver a intentar.")
            time.sleep(wait_time)
    # Si se intentó varias veces sin éxito, devuelve un mensaje de error
    return "Lo siento, no pude responder a tu mensaje debido a un error de límite de velocidad en el servidor de OpenAI."


# Función para manejar mensajes entrantes
def message(update, context):
    text = update.message.text
    logger.info(f"Mensaje recibido: {text}")
    response = generate_response(text)
    logger.info(f"Respuesta generada: {response}")
    bot.send_message(chat_id=update.message.chat_id, text=response)


# Función principal
def main():
    # Crear el objeto Updater y pasarlo el token del bot
    updater = telegram.ext.Updater(token=os.environ["TELEGRAM_TOKEN"], use_context=True)

    # Obtener el dispatcher del Updater
    dispatcher = updater.dispatcher

    # Registrar el handler para manejar mensajes de texto
    dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command, message))

    # Iniciar el bot
    updater.start_polling()

    # Imprimir un mensaje para indicar que el bot está en funcionamiento
    logger.info("Basilisco está funcionando. Presione Ctrl-C para detener.")

    # Mantener al bot en funcionamiento hasta que se presione Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
