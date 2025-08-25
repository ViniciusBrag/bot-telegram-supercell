import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os 
from pathlib import Path
import re

REXEX_SERVICES = re.compile(r'\b(tela|telas|bateria|pelicula|peliculas|capinhas)\b', re.IGNORECASE)


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
IMAGE = BASE_DIR.parent / "assets"
TOKEN_API = os.getenv("TOKEN").strip()



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
async def save_order(update: Update, context: ContextTypes.DEFAULT_TYPE):

async def save_order_pelicula(update: Update, context: ContextTypes.DEFAULT_TYPE):

    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not IMAGE.exists():
        logging.ERROR("Error in found dir of images")
        return   

    images = list(IMAGE.glob("*.[pj][pn]g"))

    for img_path in images:
        with open(img_path, "rb") as photo:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo,
                caption=f"📷 Examples como enviar mensagem para o BOT: {img_path.name}"
            )
            logging.INFO(f"Send photos {img_path}")


async def verify_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    logging.info(f"Received message: {text} from user: {update.effective_user.first_name}")

    match = REXEX_SERVICES.search(text)
    if match:
        word = match.group(1).lower()
        if "bateria" in word:
            await save_order(update, context)
        elif "tela" in word:
            await save_order(update, context)
        elif "pel" in word:  
            await save_order_pelicula(update, context)
    else:
        await help_command(update, context)
  
 
if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN_API).build()
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verify_text))

    application.run_polling(allowed_updates=Update.ALL_TYPES)