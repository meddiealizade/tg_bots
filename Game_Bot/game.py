import time

from telebot.types import Message, ReplyKeyboardMarkup as rkm, ReplyKeyboardRemove as rkr, InlineKeyboardMarkup as ikm, \
    InlineKeyboardButton as ikb, CallbackQuery

from cfg import token
from data_base import *
import telebot
import asyncio

bot = telebot.TeleBot(token)
temp = {}
clear = rkr()


@bot.message_handler(commands=['start'])
def start(m: Message):
    if is_new_player(m):
        temp[m.chat.id] = {}
        reg_1(m)
    else:
        menu(m)


@bot.message_handler(commands=['menu'])
def menu(m: Message):
    txt = 'Что будешь делать?\n\n/home - пойти домой\n/square - на гл.улицу\n/stats - статистика'
    bot.send_message(m.chat.id, text=txt, reply_markup=clear)


@bot.message_handler(commands=['home'])
def home(m: Message):
    kb = rkm(resize_keyboard=True, one_time_keyboard=True)
    kb.row("пополнить ХП", "передохнуть")
    bot.send_message(m.chat.id, 'ты дома, выбирай чем хочешь заняться', reply_markup=kb)
    bot.register_next_step_handler(m, reg_4)


@bot.message_handler(commands=['addheal'])
def addheal(m: Message):
    id, food = heal.read('user_id', m.chat.id)
    print(food)
    food['кукумбер'] = [4, 14]
    heal.write([id, food])
    print('выдали нямням')

@bot.message_handler(commands=['stats'])
def stats(m: Message):
    player = db.read('user_id', m.chat.id)
    txt = f'Имя: {player[1]}\nРаса: {player[2]}\nЗдоровье: {player[3]}\nУрон: {player[4]}\nУровень: {player[5]}\nОпыт: {player[6]}'
    bot.send_message(m.chat.id, text=txt, reply_markup=clear)


def is_new_player(m: Message):
    players = db.read_all()
    for player in players:
        if player[0] == m.chat.id:
            return False
    return True


@bot.callback_query_handler(func=lambda call: True)
def callback(call: CallbackQuery):
    print(call.data)
    if call.data.startswith('food_'):
        a = call.data.split('_')
        eating(call.message, ft=a[1], hp=a[2])
        player = db.read('user_id', call.message.chat.id)
        bot.answer_callback_query(call.id, f'Здоровье восполнено, теперь у тебя {player[3]} hp')
        kb = ikm()
        _, food = heal.read("user_id", call.message.chat.id)
        if food == {}:
            bot.send_message(call.message.chat.id, "Кушать нечего, воспользуйся командой /addheal чтобы пополнить свои запасы)'",
                             reply_markup=clear)
            menu(call.message)
            return
        for key in food:
            kb.row(ikb(f"{key} {food[key][1]} hp - {food[key][0]} шт", callback_data=f"food_{key}_{food[key][1]}"))
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=kb)
    if call.data.startswith('sleep_'):
        b = call.data.split('_')
        t = int(b[1])/10*60
        asyncio.run(asyncio.sleep(t))
        sleeping(call.message, b[1])
        bot.delete_message(call.message.chat.id, call.message.message_id)
        menu(call.message)


def eat(msg: Message):
    kb = ikm()
    _, food = heal.read("user_id", msg.chat.id)
    if food == {}:
        bot.send_message(msg.chat.id, "Кушать нечего, воспользуйся командой /addheal чтобы пополнить свои запасы)'",
                         reply_markup=clear)
        menu(msg)
        return
    for key in food:
        if food[key][0] > 0:
            kb.row(ikb(f"{key} {food[key][1]} hp - {food[key][0]} шт", callback_data=f"food_{key}_{food[key][1]}"))
    bot.send_message(msg.chat.id, "Выбери что будешь есть:", reply_markup=kb)


def eating(msg, ft, hp):
    _, food = heal.read('user_id', msg.chat.id)
    player = db.read('user_id', msg.chat.id)
    if food[ft][0] == 1:
        del food[ft]
    else:
        food[ft][0] -= 1
    heal.write([msg.chat.id, food])

    player[3] += int(hp)
    db.write(player)
    print('Игрок сделал ням ням')


def sleep(m: Message):
    player = db.read('user_id', m.chat.id)
    low = int(heroes[player[2]][0]+((player[5]-1)*20))//2 - player[3]
    high = int(heroes[player[2]][0]+((player[5]-1)*20)) - player[3]
    kb = ikm()
    if low > 0:
        kb.row(ikb(f"Вздремнуть + {low}❤️", callback_data=f'sleep_{low}'))
    if high > 0:
        kb.row(ikb(f"Поспать + {high}❤️", callback_data=f'sleep_{high}'))
    if len(kb.keyboard) == 0:
        kb.row(ikb('Рано спать', callback_data='menu'))
    bot.send_message(m.chat.id, "Выбери сколько будешь спать:" , reply_markup=kb)

def sleeping(m: Message, hp):
    player = db.read('user_id', m.chat.id)
    player[3] += int(hp)
    db.write(player)
    print("Игрок сделал бай бай")


def reg_1(m: Message):
    txt = f"Привет!\nВведи свой ник)"
    bot.send_message(m.chat.id, txt)
    bot.register_next_step_handler(m, reg_2)


def reg_2(m: Message):
    temp[m.chat.id]['nick'] = m.text
    kb = rkm(True, True)
    for g in list(heroes):
        kb.row(g)
    bot.send_message(m.chat.id, 'Выбери за кого будешь играть:', reply_markup=kb)
    bot.register_next_step_handler(m, reg_3)


def reg_3(m: Message):
    temp[m.chat.id]["type"] = m.text
    hp, dmg = heroes[m.text]
    db.write([m.chat.id, temp[m.chat.id]["nick"], temp[m.chat.id]["type"], hp, dmg, 1, 0])
    heal.write([m.chat.id, {}])
    print("Пользователь добавлен в базу данных")
    bot.send_message(m.chat.id, text="Инициализация...")
    time.sleep(2)
    menu(m)


def reg_4(m: Message):
    if m.text == "пополнить ХП":
        eat(m)
    if m.text == 'передохнуть':
        sleep(m)


bot.infinity_polling()
