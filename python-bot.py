import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os 
from pathlib import Path


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
IMAGE = BASE_DIR.parent / "assets"
TOKEN_API = os.getenv("TOKEN").strip()



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
     
async def verify_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    logging.info(f"Received message: {text} from user: {update.effective_user.first_name}")

     # Check if the text starts with 'tela' or 'telas'
     # Example: 'tela 2 samsung' or 'telas 3 iphone'
     # Extract quantity and model
     # Default quantity to 1 if not specified
    parts = text.split(maxsplit=2) # divided of in 3 parts.
    if len(parts) >= 2 and parts[0].isdigit():
        if parts[1] not in ('telas', 'tela', 'bateria'):
            FILE_PATH = IMAGE / "example_order_display.png"
            if FILE_PATH.exists():
                with open(FILE_PATH, 'rb') as photo:      
                    await context.bot.send_photo(chat_id=update.effective_chat.id, caption=f"*Por favor adcionar conforme a foto*",photo=photo, parse_mode="MarkDownV2")
            else:  
                quantity = parts[0]
                text_model = " ".join(parts[1:])
                first_name = update.effective_user.first_name
                await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{first_name} *Adicionado o pedido: {quantity} {text_model} com sucesso*",
                parse_mode='MarkdownV2')

    
        #else if text_model in ('pelicula', 'peliculas', 'capinhas'):
 
if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN_API).build()
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verify_text))

    application.run_polling(allowed_updates=Update.ALL_TYPES)