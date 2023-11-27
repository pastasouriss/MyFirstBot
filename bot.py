import telebot
import sqlite3
from telebot import types

bot=telebot.TeleBot('6737241380:AAHc8kNCyVs3FPgdzKRqYv14TKCJoez6sqw')
name=''
omgreview=''

@bot.message_handler(commands=['start'])
def menu(message):  
        conn=sqlite3.connect('reviews.sql')
        cur=conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), review VARCHAR(1000))')
        conn.commit()
        cur.close()
        conn.close()
        markup= types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1=types.KeyboardButton('Написать отзыв')
        markup.row(but1)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Напишите Ваш отзыв здесь :)',reply_markup=markup)
        bot.register_next_step_handler(message,on_click)
def on_click(message):
    global name
    if message.text == 'Написать отзыв':
        bot.send_message(message.chat.id, 'Как Вас зовут?')
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.chat.id, f'Спасибо, {name}! А теперь выскажите свое мнение о нас :)')
    bot.register_next_step_handler(message, user_review)
def user_review(message):
      global omgreview
      omgreview=message.text
      bot.send_message(message.chat.id,'Спасибо!')
      conn=sqlite3.connect('reviews.sql')
      cur=conn.cursor()
      cur.execute("INSERT INTO users(name,review) VALUES ('%s','%s')"%(name,omgreview))
      conn.commit()
      cur.close()
      conn.close()
      markup=types.InlineKeyboardMarkup()
      but1=types.InlineKeyboardButton('Все отзывы',callback_data='users')
      markup.row(but1)
      bot.send_message(message.chat.id,'Ваш отзыв отправлен!',reply_markup=markup)
      bot.register_next_step_handler(message, on_click)



@bot.callback_query_handler(func=lambda callback:True)
def cbm(callback):
        conn=sqlite3.connect('reviews.sql')
        cur=conn.cursor()
        cur.execute('SELECT * FROM users')
        users=cur.fetchall()
        info=''
        for el in users:
             info+=f'Имя: {el[1]}\nОтзыв: {el[2]}\n\n\n' 
        cur.close()
        conn.close()
        bot.send_message(callback.message.chat.id,info)
bot.polling(none_stop=True)