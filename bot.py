import telebot
import os
import cv2
from database import DatabaseManager
from logic import create_collage

bot = telebot.TeleBot('ВАШ_ТОКЕН')
db = DatabaseManager('database.db')

@bot.message_handler(commands=['my_score'])
def get_my_score(message):
    user_id = message.from_user.id
    prizes = db.get_winners_img(user_id)

    image_paths = os.listdir('img')
    image_paths = [f'img/{x}' if x in prizes else f'hidden_img/{x}' for x in image_paths]

    collage = create_collage(image_paths)
    cv2.imwrite(f'collage_{user_id}.png', collage)

    with open(f'collage_{user_id}.png', 'rb') as photo:
        bot.send_photo(user_id, photo, caption="Твой коллаж с призами!")
    
    os.remove(f'collage_{user_id}.png')
