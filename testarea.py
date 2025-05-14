import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import logging
from findcode import extract_code

# Enable logging
logging.basicConfig(
    filename='bot_logs.txt',  # Log file name
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token and channel ID
BOT_TOKEN = '7530705556:AAF_11SPJ3kJbSkU0H79f8KGBglPo7kMnA0'
CHANNEL_ID = '-1002284184519'

# Initialize the last processed message ID
last_processed_message_id = 0  # Initially set to 0 or the ID of the first message processed

async def start(update: Update, context):
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text("Hello! I'm listening to channel messages.")

async def echo(update: Update, context):
    """Extract monospaced text from the message using entities."""
    global last_processed_message_id  # Access the global variable

    if update.channel_post and update.channel_post.chat_id == int(CHANNEL_ID):
        message = update.channel_post.text  # The plain text content
        message_id = update.channel_post.message_id  # The message ID
        
        # Only process messages with a higher message_id than the last processed one
        if message_id > last_processed_message_id:
            last_processed_message_id = message_id  # Update the last processed message ID

            entities = update.channel_post.entities  # The message entities (including formatting)

            if entities:
                # Extract and print all monospaced (inline code) sections
                for entity in entities:
                    if entity.type == 'code':  # 'code' entity is used for monospaced text
                        monospaced_text = message[entity.offset: entity.offset + entity.length]
                        if monospaced_text: 
                            print(f"Monospaced text found: {monospaced_text}")
            else:
                # If no monospaced text, extract code or other text
                code = extract_code(message)
                if code:
                    print(f"Extracted code: {code}")
                else:
                    print("No code found in the message.")
        else:
            print(f"Old message skipped (ID: {message_id})")  # Log old message IDs

async def error_handler(update: object, context):
    """Log the error."""
    logger.warning(f'Update "{update}" caused error "{context.error}"')

if __name__ == '__main__':
    # Create the Application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL & filters.UpdateType.CHANNEL_POST, echo))

    # Log all errors
    application.add_error_handler(error_handler)

    # Run the bot
    print("Bot is running...")
    application.run_polling()
