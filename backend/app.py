import os
import threading
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import telebot

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///bot.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Telegram bot configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Import models
from models import Command, Chat, Message

# Initialize database
with app.app_context():
    db.create_all()

@app.route('/commands', methods=['POST'])
def add_command():
    with app.app_context():
        data = request.json
        new_command = Command(name=data['name'], response=data['response'])
        db.session.add(new_command)
        db.session.commit()
        return jsonify({'message': 'Command added successfully!'}), 201

@app.route('/broadcast', methods=['POST'])
def broadcast_message():
    with app.app_context():
        message_text = request.json.get('message')
        media_url = request.json.get('media_url')
        
        if not message_text or not media_url:
            return jsonify({"error": "Message and media URL are required"}), 400

        # Get chat IDs
        chats = Chat.query.all()

        for chat in chats:
            try:
                # Send media to each chat
                bot.send_photo(chat.chat_id, media_url, caption=message_text)
            except Exception as e:
                print(f"Failed to send message to chat ID {chat.chat_id}: {e}")

        return jsonify({'message': 'Broadcast message sent!'}), 200

@app.route('/commands/<int:command_id>', methods=['PUT'])
def edit_command(command_id):
    with app.app_context():
        data = request.json
        command = Command.query.get(command_id)
        if command:
            command.name = data['name']
            command.response = data['response']
            db.session.commit()
            return jsonify({"message": "Command updated successfully!"}), 200
        else:
            return jsonify({"error": "Command not found"}), 404

@app.route('/commands/<int:command_id>', methods=['DELETE'])
def delete_command(command_id):
    with app.app_context():
        command = Command.query.get(command_id)
        if command:
            db.session.delete(command)
            db.session.commit()
            return jsonify({"message": "Command deleted successfully!"}), 200
        else:
            return jsonify({"error": "Command not found"}), 404

def run_bot():
    bot.polling( timeout=30)

if __name__ == '__main__':
    # Start the bot in a separate thread
    threading.Thread(target=run_bot).start()
    app.run(debug=True, host='0.0.0.0', port=5001)  # Allow external access
