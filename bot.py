import telebot
from database import DatabaseManager

bot = telebot.TeleBot('ВАШ_ТОКЕН')
db = DatabaseManager('database.db')

@bot.message_handler(commands=['rating'])
def handle_rating(message):
    res = db.get_rating()
    res_lines = [f'| @{x[0]:<11} | {x[1]:<11}|\n{"_"*26}' for x in res]
    res_text = '\n'.join(res_lines)
    res_text = f'|USER_NAME    |COUNT_PRIZE|\n{"_"*26}\n' + res_text
    bot.send_message(message.chat.id, res_text)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    prize_id = int(call.data)
    user_id = call.from_user.id

    if db.get_winners_count(prize_id) < 3:
        added = db.add_winner(user_id, prize_id)
        if added:
            img_path = f'img/{prize_id}.png'
            try:
                with open(img_path, 'rb') as photo:
                    bot.send_photo(user_id, photo, caption="Поздравляем! Ты получил картинку!")
            except FileNotFoundError:
                bot.send_message(user_id, "Ошибка: картинка не найдена!")
        else:
            bot.send_message(user_id, "Ты уже получил картинку!")
    else:
        bot.send_message(user_id, "К сожалению, ты не успел получить картинку! Попробуй в следующий раз :)")

bot.polling(none_stop=True)
