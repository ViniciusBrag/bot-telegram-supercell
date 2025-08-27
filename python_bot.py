import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os 
from pathlib import Path
import re
from bot_telegram_store.utils import parse_order
from pony.orm import db_session
from bot_telegram_store.db import Order

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
REXEX_SERVICES = re.compile(r'\b(tela|telas|bateria|pelicula|peliculas|capinhas)\b', re.IGNORECASE)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
IMAGE = BASE_DIR.parent / "assets"
TOKEN_API = os.getenv("TOKEN").strip()



@db_session
async def save_order(update: Update, context: ContextTypes.DEFAULT_TYPE, quantity_order: str, model_order: str):
    order = Order(quantity=int(quantity_order), model=model_order)
    commit()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"*{update.effective_user.first_name} Pedido efetuado com sucesso*", parse_mode="Markdown")

#async def save_order_pelicula(update: Update, context: ContextTypes.DEFAULT_TYPE):


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
   


async def verify_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    logging.info(f"Received message: {text} from user: {update.effective_user.first_name}")

    match = REXEX_SERVICES.search(text)
    if match:
        word = match.group(1).lower()

        if "bateria" in word:
            quantity, model = parse_order(text)
            await save_order(update, context, quantity, model)
        elif "tela" in word:
            quantity, model = parse_order(text)
            await save_order(update, context, quantity, model)
        #elif "pel" in word:  
         #   await save_order_pelicula(update, context)
    else:
        await help_command(update, context)
  
 
if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN_API).build()
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verify_text))

    application.run_polling(allowed_updates=Update.ALL_TYPES)