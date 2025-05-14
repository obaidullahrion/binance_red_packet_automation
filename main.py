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

async def start(update: Update, context):
    """Send a welcome message when the /start command is issued."""
    await update.message.reply_text("Hello! I'm listening to channel messages.")

async def echo(update: Update, context):
    """Extract monospaced text from the message using entities."""
    if update.channel_post and update.channel_post.chat_id == int(CHANNEL_ID):
        message = update.channel_post.text  # The plain text content
        entities = update.channel_post.entities  # The message entities (including formatting)

        if entities:
            # Extract and print all monospaced (inline code) sections
            for entity in entities:
                if entity.type == 'code':  # 'code' entity is used for monospaced text
                    monospaced_text = message[entity.offset: entity.offset + entity.length]
    

                    if monospaced_text: 
                        print(monospaced_text)
        else:

            code = extract_code(message)
            if code:
                print(f"{', '.join(code)}")
            else:  
                print("No code found in the message.")


        



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
