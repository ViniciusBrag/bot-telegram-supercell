import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os 
import pdb

load_dotenv()

TOKEN_API = os.getenv("TOKEN").strip()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

save_order(first_name, text_model)

async def verify_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.lower().strip()
    except Exception as e:
        logging.error(e)
        return
    else:        
        if text in 'tela':
            quantity_of_display = text[2:]
            print(quantity_of_display)
            text_model = text[4:]
            first_name = update.effective_user.first_name
           


    

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello {text_model}, {first_name}")

if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN_API).build()
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verify_text))
    application.run_polling()