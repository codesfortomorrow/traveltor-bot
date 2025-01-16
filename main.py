from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import os
import traceback
import logging

load_dotenv()

with open("quotes.txt", "r", encoding="utf-8") as file:
    quotes = file.readlines()

# Store the last 15 bot replies to ensure uniqueness
last_replies = []

# Replace with the chat ID of your specific group (e.g., -1001234567890)
SPECIFIC_GROUP_CHAT_ID = os.getenv('CHAT_ID')


# Define the start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Chat ID: {update.message.chat.id}")
    print(f"G Chat ID: {SPECIFIC_GROUP_CHAT_ID}")
    if str(update.message.chat.id) == str(SPECIFIC_GROUP_CHAT_ID):
    #     await update.message.reply_text(
    #         f"Oh wow, you found the magic command `/start`! 🎩✨\n\n"
    #         "Unfortunately, this isn’t Hogwarts, and `/start` won’t summon anything exciting here. 😜\n\n"
    #         "But hey, feel free to explore the group, share your experiences, and let's make travel unforgettable—no magic spells required! 🚀",
    #         parse_mode="Markdown")
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Oh wow, you found the magic command `/start`! 🎩✨\n\n"
            "Unfortunately, this isn’t Hogwarts, and `/start` won’t summon anything exciting here. 😜\n\n"
            "But hey, feel free to explore the group, share your experiences, and let's make travel unforgettable—no magic spells required! 🚀",
            parse_mode="Markdown")


# Define a function to welcome new members with an inline button
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.message.chat.id) == str(SPECIFIC_GROUP_CHAT_ID):
        for member in update.message.new_chat_members:
            name = member.full_name
            chat_id = update.effective_chat.id

            # Create an inline keyboard with a button
            keyboard = [
                [
                    InlineKeyboardButton("Visit Traveltor",
                                            url="https://traveltor.io")
                ],
                [
                    InlineKeyboardButton("Follow us on X",
                                            url="https://x.com/Traveltorsocial")
                ],
                [
                    InlineKeyboardButton(
                        "Follow us on LinkedIn",
                        url="https://www.linkedin.com/company/traveltorsocial/"
                    )
                ]  # [InlineKeyboardButton("Instagram", url="https://www.instagram.com/traveltorsocial/")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            reply_markup = InlineKeyboardMarkup(keyboard)


            # Send the welcome message with the button
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"🌄 Welcome to Traveltor, {name}! 💫\n\n"
                "🌍 Traveltor turns your Journeys into Stories and *Movements into unforgettable Moments.*\n"
                "🎁 Wherever you go, Just Check In, inspire your friends, and earn rewards along the way! Discover travel like never before!\n\n"
                "🗺️ *Visit the platform and follow us on X and LinkedIn to stay connected!*",
                parse_mode="Markdown",
                reply_markup=reply_markup)
            
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.message.chat.id) == str(SPECIFIC_GROUP_CHAT_ID):
        for member in update.message.new_chat_members:
            name = member.full_name
            chat_id = update.effective_chat.id

            # Create an inline keyboard with a button
            keyboard = [
                [
                    InlineKeyboardButton("Visit Traveltor",
                                            url="https://traveltor.io")
                ],
                [
                    InlineKeyboardButton("Follow us on X",
                                            url="https://x.com/Traveltorsocial")
                ],
                [
                    InlineKeyboardButton(
                        "Follow us on LinkedIn",
                        url="https://www.linkedin.com/company/traveltorsocial/"
                    )
                ]  # [InlineKeyboardButton("Instagram", url="https://www.instagram.com/traveltorsocial/")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            reply_markup = InlineKeyboardMarkup(keyboard)


            # Send the welcome message with the button
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"🌄 Welcome to Traveltor, {name}! 💫\n\n"
                "🌍 Traveltor turns your Journeys into Stories and *Movements into unforgettable Moments.*\n"
                "🎁 Wherever you go, Just Check In, inspire your friends, and earn rewards along the way! Discover travel like never before!\n\n"
                "🗺️ *Visit the platform and follow us on X and LinkedIn to stay connected!*",
                parse_mode="Markdown",
                reply_markup=reply_markup)


async def handle_greeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Function called with message:", update.message.text)  # Debugging log

    # Message content
    message_text = update.message.text.lower()
    greetings = ['gm', 'gm gm', 'good morning', 'gn', 'good night']
    spiritual_greetings = [
        'jai shree ram', 'jay shree ram', 'jai shri ram', 'jay shri ram',
        'ram ram', 'sita ram', 'radhe radhe',
        'jai mata ki', 'jay mata ki', 'jai mata di', 'jay mata di',
        'jai ganesh', 'jay ganesh', 'jai shree shyam', 'jay shree shyam'
    ]


    # Check if the message matches a greeting
    if any(greeting in message_text for greeting in greetings):
        print("Greeting detected")  # Debugging log

        # Get the sender's first name
        user_first_name = update.message.from_user.first_name

        # Pick a random unique quote
        unique_reply = None
        while unique_reply is None:
            random_quote = random.choice(quotes).strip()
            if random_quote not in last_replies:
                unique_reply = random_quote

        # Keep the last 15 replies unique
        last_replies.append(unique_reply)
        if len(last_replies) > len(quotes):
            last_replies.pop(0)

        # Create the reply message
        reply_message = f"🌅 GM {user_first_name}!\n\n{unique_reply}"

        # Send the reply
        await context.bot.send_message(chat_id=update.message.chat_id, text=reply_message)
    elif any(greeting in message_text for greeting in spiritual_greetings):
        print("Spiritual greeting detected")  # Debugging log

        # Get the sender's first name
        user_first_name = update.message.from_user.first_name

        # Create the reply message
        reply_message = f"Jai Shree Mahakal 🙏, {user_first_name}"

        # Send the reply
        await context.bot.send_message(chat_id=update.message.chat_id, text=reply_message)

def main():
    # Replace 'YOUR_API_TOKEN' with the token you got from BotFather
    api_token = os.getenv("API_TOKEN")

    # Initialize the application
    application = Application.builder().token(api_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_greeting))

    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(traceback.format_exc())
        # Logs the error appropriately. 
