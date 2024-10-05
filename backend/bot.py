import telebot
from models import Chat, Command, Message
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
db = SQLAlchemy()

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    chat_id = str(message.chat.id)
    chat = Chat.query.filter_by(chat_id=chat_id).first()

    if not chat:
        new_chat = Chat(chat_id=chat_id, chat_type=message.chat.type)
        db.session.add(new_chat)
        db.session.commit()

    bot.send_message(chat_id, "Hello! Use /help to view commands.")

@bot.message_handler(commands=['search'])
def handle_search(message):
    query = message.text.split(' ', 1)
    if len(query) < 2:
        bot.send_message(message.chat.id, "Please provide a search term.")
        return

    search_term = query[1]
    messages = Message.query.filter(Message.text.contains(search_term)).all()

    if not messages:
        bot.send_message(message.chat.id, "No messages found.")
    else:
        result = "\n".join([f"{msg.timestamp}: {msg.text}" for msg in messages])
        bot.send_message(message.chat.id, f"Search Results:\n{result}")

@bot.message_handler(func=lambda message: True)
def handle_custom_commands(message):
    chat_id = str(message.chat.id)
    command = Command.query.filter_by(name=message.text.strip('/')).first()
    if command:
        bot.send_message(chat_id, command.response)
    else:
        bot.send_message(chat_id, "Unknown command. Use /help for a list of available commands.")

    # Store the message in the database
    new_message = Message(chat_id=chat_id, text=message.text)
    db.session.add(new_message)
    db.session.commit()
