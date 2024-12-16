from gpt4all import GPT4All
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from functools import partial


# Initialize the GPT4All model
model = GPT4All(r"mistral-7b-instruct-v0.1.Q4_0.gguf", device="cuda")

# List of allowed usernames
ALLOWED_USERNAMES = ["authorized_user1", "authorized_user2", ""]  # Add your allowed usernames here


# Function to handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, session) -> None:
    username = update.effective_user.username  # Get the Telegram username
    
    if username not in ALLOWED_USERNAMES:  # Check if user is unauthorized
        await update.message.reply_text("🚫 Unauthorized access. You are not allowed to use this bot.")
        return
    
    user_input = update.message.text
    response = session.generate(user_input)  # Use the session passed via partial
    await update.message.reply_text(response)


# Main function to set up the bot
def main():
    with model.chat_session() as session:  # Initialize the chat session once

        application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

        # Use functools.partial to pass 'session' to the handler
        message_handler = MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            partial(handle_message, session=session)
        )
        application.add_handler(message_handler)

        # Start the bot
        application.run_polling()


if __name__ == '__main__':
    main()
