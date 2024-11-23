import s_taper
from s_taper.consts import *

scheme = {
    'user_id': INT + KEY,
    'name': TEXT,
    'type': TEXT,
    'hp': INT,
    'damage': INT,
    'level': INT,
    'exp': INT
}
db = s_taper.Taper('users', 'data.db').create_table(scheme)
heroes = {
    "муха": (50, 20),
    "комар": (45, 25),
    "овод": (60, 15),
    "пчела": (70, 13)
}
scheme2 = {
    'user_id': INT + KEY,
    'food': TEXT
}
heal = s_taper.Taper('heal','data.db').create_table(scheme2)