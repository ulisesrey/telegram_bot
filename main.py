import logging
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

#from huggingface_hub import InferenceClient
from together import Together


# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Together.ai API Key
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')

CONTEXT = os.getenv('CONTEXT')
USER_CONTEXT = os.getenv('CONTEXT')

client = Together(api_key=TOGETHER_API_KEY)

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

# Async functions

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # modified_message = CONTEXT + update.message.text,

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[
            {"role": "system", "content": CONTEXT},
            {"role": "user", "content": update.message.text}],
    )
    
    response = completion.choices[0].message.content
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Send a Good morning message if it is 8:00 AM, send it daily
async def good_morning(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.context, text='Good morning!')

# This handler should be added last
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)

    # Exclude commands from the conversation handler
    not_command = ~filters.COMMAND
    conversation_handler = MessageHandler(filters.TEXT & not_command, conversation)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(conversation_handler)
    application.add_handler(unknown_handler)
    
    application.run_polling()