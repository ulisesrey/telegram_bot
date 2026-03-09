import os
import logging
import boto3
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
# from dotenv import load_dotenv
# load_dotenv()


# --- Environment Setup ---
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
CONTEXT = os.getenv('CONTEXT', "You are a helpful assistant.")

# Initialize Bedrock
bedrock_runtime = boto3.client("bedrock-runtime", region_name=AWS_REGION)
MODEL_ID = "amazon.nova-micro-v1:0"

# --- User Storage ---
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm a bot powered by AWS Bedrock! How can I help you today?")

async def conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    user_text = update.message.text
    
    # 1. Initialize user history if new
    if user_id not in user_data:
        user_data[user_id] = {"conversation_history": []}
    
    # 2. Get history (Last 10 messages for better context)
    history = user_data[user_id]["conversation_history"][-10:]

    # 3. Format messages for Bedrock Converse API
    # Bedrock requires: [{"role": "user", "content": [{"text": "..."}]}]
    bedrock_messages = []
    for msg in history:
        bedrock_messages.append({
            "role": msg["role"],
            "content": [{"text": msg["content"]}]
        })
    
    # Add current user message
    bedrock_messages.append({
        "role": "user",
        "content": [{"text": user_text}]
    })

    try:
        # 4. Call Bedrock
        response = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=bedrock_messages,
            system=[{"text": CONTEXT}],
            inferenceConfig={"maxTokens": 1000, "temperature": 0.5}
        )

        # 5. Extract response text
        assistant_response = response['output']['message']['content'][0]['text']

        # 6. Update local history (we store raw strings for simplicity)
        user_data[user_id]["conversation_history"].append({"role": "user", "content": user_text})
        user_data[user_id]["conversation_history"].append({"role": "assistant", "content": assistant_response})

        await update.message.reply_text(assistant_response)

    except Exception as e:
        logging.error(f"Bedrock Error: {e}")
        await update.message.reply_text("I hit a snag connecting to AWS. Please try again in a moment!")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sorry, I didn't understand that command.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), conversation))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    
    print(f"Bot started in {AWS_REGION} using {MODEL_ID}...")
    application.run_polling()