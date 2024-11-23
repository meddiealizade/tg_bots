from telebot.types import Message, ReplyKeyboardMarkup as rkm

from config import TOKEN
import telebot
import random

bot = telebot.TeleBot(TOKEN)

words = ['камень', 'алмаз', 'бриллиант', 'золото', 'медь', 'бирюза', 'хризолит', 'сапфир', 'изумруд', 'гранат',
         'песок', 'земля', 'корень', 'агат', 'гравий', 'окаменелость', 'трава', 'семена', 'зерна', 'стекло', 'кость',
         'уголь', 'глина', 'мрамор', 'древесный уголь', 'обсидиан']


@bot.message_handler(['start'])
def start(m: Message):
    kb = rkm()
    kb.row('КОПАТЬ')
    bot.send_message(m.chat.id, 'Здравствуй! Это бот магазина товаров для дома "Яблочко", у тебя есть шанс '
                                'выиграть промокод на скидку в магазине с помощью бота!'
                                'Для этого жми на кнопку "копать"!', reply_markup=kb)


@bot.message_handler(content_types=['text'])
def text(m: Message):
    if m.text == 'КОПАТЬ':
        word = random.choice(words)
        bot.send_message(m.chat.id, f'Поздравляю! Тебе выпал случайный ресурс: {word}')
        promo = random.randint(1, 100)
        print(promo)
        if promo in range(1, 6):
            bot.send_message(m.chat.id, f'Тебе сегодня везёт! Вот промокод на скидку в магазине: SuperPromo2024')


bot.infinity_polling()
