import telebot
from telebot.types import Message, ReplyKeyboardMarkup as rkm, InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb, \
    CallbackQuery
from config import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(m: Message):
    print(m.chat.id, m.from_user.full_name)
    bot.send_message(6507669890, text=f'{m.from_user.full_name}-ID:{m.chat.id}')
    bot.send_message(m.chat.id, text='Приветик, я бот💓💕')


@bot.message_handler(commands=['tell_me_about_yourself'])
def myau(m: Message):
    print(m.chat.id, m.from_user.full_name)
    bot.send_message(m.chat.id, text='Расскажи про себя) Как тебя зовут?')
    bot.register_next_step_handler(m, reg)

@bot.message_handler(commands=['help'])
def help(m: Message):
    kb = rkm(resize_keyboard=True, one_time_keyboard=True)
    kb.row('/start', '/help')
    kb.row('/tell_me_about_yourself', 'yoshkarola')
    bot.send_message(m.chat.id, 'viberi comandu', reply_markup=kb)

@bot.message_handler(commands=['buttons'])
def help(m: Message):
    kb = rkm(resize_keyboard=True, one_time_keyboard=True)
    kb.row('/aya', '/help')
    kb.row('/tell_me_about_yourself', '/gav')
    bot.send_message(m.chat.id, 'viberi comandu', reply_markup=kb)

@bot.message_handler(commands=['aya'])
def aya(m: Message):
    print(m.chat.id, m.from_user.full_name)
    bot.send_message(m.chat.id, text='perivet, kak ti?')
    bot.register_next_step_handler(m, keg)

def keg(m: Message):
    name = m.text
    bot.send_message(m.chat.id, text=f":p")
    bot.send_message(m.chat.id, text="klass")

@bot.message_handler(commands=['gav'])
def aya(m: Message):
    print(m.chat.id, m.from_user.full_name)
    bot.send_message(m.chat.id, text='ya sobaka, a ti?')
    bot.register_next_step_handler(m, keg1)

def keg1(m: Message):
    name = m.text
    bot.send_message(m.chat.id, text=f"frrrr")
    bot.send_message(m.chat.id, text="kringe")

@bot.message_handler(commands=['inline'])
def inline(m: Message):
    kb = ikm()
    kb.row(ikb('google', url='https://google.com'))
    kb.row(ikb('погода ', url='https://weather.com'))
    kb.row(ikb('для no english', url='https://translate.google.com'))
    kb.row(ikb('никогда не заходи', url='https://earth.google.com/'))
    kb.row(ikb('knopkarrr', callback_data='1_a'))
    bot.send_message(m.chat.id, text="viberi sait po bratski", reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def callback(call: CallbackQuery):
    print(call.__dict__)
    if call.data == '1_a':
        cat(call.message)

def reg(m: Message):
    name = m.text
    bot.send_message(m.chat.id, text=f"{name},классное имя! ;p")
    bot.send_message(m.chat.id, text="A skol'ko tebye let?")
    bot.register_next_step_handler(m, reg1, name)


def reg1(m: Message, name: str):
    age = m.text
    bot.send_message(m.chat.id, text=f"{name}, я думал тебе 8! ;)")


@bot.message_handler(commands=['myau'])
def cat(m: Message):
    print(m.chat.id, m.from_user.full_name)
    bot.send_message(m.chat.id, text='мяу^.^')
    bot.register_next_step_handler(m, reg2)


def reg2(m: Message):
    myau1 = m.text
    bot.send_message(m.chat.id, text=f"{myau1}, myau")
    bot.send_message(m.chat.id, text="Я умею мяукать;)myau")
    bot.register_next_step_handler(m, reg3, myau1)


def reg3(m: Message, myau1: str):
    myau2 = m.text
    bot.send_message(m.chat.id, text="мяу")
    bot.send_message(m.chat.id, text="гав")
    bot.send_message(m.chat.id, text="мяу")
    bot.send_message(m.chat.id, text=f"{myau2} гав")
    bot.send_message(m.chat.id, text=f"{myau1}, гав")
    bot.send_message(m.chat.id, text="а ещё гавкать:>")


@bot.message_handler(content_types=['text'])
def text(m: Message):
    if m.text == 'myau':
        bot.send_message(m.chat.id, 'выйди и зайди нормально, ещё дверью хлопать удумал ,фи')
    if len(m.text) > 10:
        bot.send_message(m.chat.id, 'перепечатай быстро!!!!!!!я слишком туп для таких длинных предложений;(')


@bot.message_handler(content_types=['audio'])
def audio(m: Message):
    aud = m.audio
    print(f"Бот получил аудио,мяу.\n"
          f"Продолжительность:{aud.duration // 60} мин. {aud.duration % 60} сек.\n"
          f'Исполнитель: {aud.performer}\n'
          f'Название: {aud.title}\n'
          f'Размер файла: {round(aud.file_size / 1024000, 2)} Мбайт')
    file_id = aud.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    download = bot.download_file(file_path)
    with open(f"{aud.performer} - {aud.title}.mp3", 'wb') as file:
        file.write(download)
    bot.reply_to(m, 'мяу🎀')


@bot.message_handler(content_types=['photo'])
def img(m: Message):
    image = m.photo
    print(f"Бот получил фоточку,мяу.\n")
    file_id = image[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    download = bot.download_file(file_path)
    with open(f"{image[-1].file_unique_id}.jpg", 'wb') as file:
        file.write(download)
    bot.reply_to(m, 'мяу🎀')


bot.infinity_polling()
