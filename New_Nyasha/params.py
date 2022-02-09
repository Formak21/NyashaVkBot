import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from datetime import *
import random
import googletrans3
import googletrans4
import sys

# Service
with open('Data/API_KEY.txt', 'r', encoding='utf-8') as _f:
    ID, API = _f.read().splitlines()
vk_ses = vk_api.VkApi(token=API)
vk_lp = VkBotLongPoll(vk_ses, ID)



# Long Messages
with open('Data/paste.txt', 'r', encoding='utf-8') as _f:
    paste = _f.read().split('\n')
with open('Data/alf.txt', 'r', encoding='utf-8') as _f:
    BotMessages['ping_message'][1] = _f.read()
with open('Data/help.txt', 'r', encoding='utf-8') as _f:
    BotMessages['help_message'] = _f.read()
with open('Data/info.txt', 'r', encoding='utf-8') as _f:
    BotMessages['info_message'] = _f.read()
with open('Data/debug.txt', 'r', encoding='utf-8') as _f:
    BotMessages['debug_message'] = _f.read()

# Translators
Translators = {3: googletrans3.Translator(), 4: googletrans4.Translator()}


Info = {'started': datetime.now(), 'version': "3.5.0a", 'bot_name': 'Nyasha'}


Service = {'api_token': str(), 'bot_community_id': str(), 'translators': dict(), 'vk_session': None,
           'vk_longpoll': None}


Parameters = {'admin_ids': {492569185, 384341109, 551709213}, 'banned_ids': {}, 'is_disabled': False}


Tags = {
    'Bot': {'няша', 'няшенька', 'няшуля', 'nyasha', 'nyashulya', 'nyashenka', 'няшулечка', 'nyashulechka'},
    'XiGet': {'xi', 'хи', 'си', 'кси', 'кхи', 'si', 'ksi'},
    'CrazyGet': {'крз', 'крейзи', 'crazy', 'crz', 'krz', 'krazy', 'крэйзи'},
    'LeetGet': {'лит', 'лиит', 'леет', 'leet', 'elite', '1337'},
    'PasteGet': {'хуй', 'xyi', 'хой', 'huy'},
    'XyiGet': {'хуефик', 'хуефиц', 'хуефицировать', 'хуефикатор', 'хуефицируй',
               'xiyefic', 'xiyefits', 'xiyefik', 'xiyeficator', 'xiyefikator',
               'xiyefitsiruy', 'xiyefitsitovat', 'huyefic', 'huyefits', 'huyefik',
               'huyeficator', 'huyefikator', 'huyefitsiruy', 'huyefitsitovat',
               'хфц', 'hfc', 'xfc', 'hfts', 'xfts', 'хфк'},
    'PasteAdd': {'добавь', 'add', 'save', 'сохр', 'сохрани'},
    'PingGet': {'маяк', 'пинг', 'алл', 'олл', 'пидорасы', 'mayak', 'ping', 'all', 'pidorasi'},
    'HelpGet': {'help', 'хелп', 'помощь', 'хэлп', 'halp', 'plshalp', 'памагитипж', 'памагити'},
    'InfoGet': {'info', 'инфо', 'инфа', 'infa', 'чеэтозапидорасебучий'},
    'DebugGet': {'debug', 'дебаг', 'дэбаг'},
    'EnableSet': {'en', 'ен', 'эн', 'вкл', 'enable', 'включить'},
    'DisableSet': {'dis', 'диз', 'выкл', 'disable', 'выключить'},
    'RestartGet': {'restart', 'рестарт'}
}


BotMessages = {
    'global_message': ['Че надо?', 'Ась?', 'Что тебе нужно?', 'А?', 'Что?', 'Ну че?', 'Слушаю?'],
    'success_message': ['Выполнено.', 'Выполнила.', 'Готово.', 'Сделано.', 'Успех.', 'Обработала.',
                        'Всё сделала.', 'Сама справилась.'],
    'user_error_message': ['Ты еблан.', 'Ты утюг ебаный.', 'Ты тупой.', 'Ты мудак.', 'Ты долбаеб.',
                           'Ты еблоид.', 'Отстань.', 'Отъебись.', 'Исчезни, уеба.', 'Ты туп как депутат.',
                           'Пиздец... Как ты до своих лет то дожил?', 'Ох... Я ебала... Тупорылый бля...'],
    'delay_message': ['Подожди ты уеба...', 'Кулдаун блять, уебище.', 'Не так быстро, мудень.',
                      'Жди бля, уебок.', 'Хули ты такой быстрый? Как вода блять в унитазе.',
                      'ЯМЕТЕ КУДАСААИИ~!! АХхх~~~! Притормози Сенпай! Ну че, как подрочил, уебок?',
                      'Жди.'],
    'ping_message': ['Pinging @all [127.0.0.1] with 32 bytes of data:', ''],
    'help_message': [''],
    'debug_message': [''],
    'info_message': ['']
}


Timings = {
    'Global': {'Request': datetime.now(), 'Delay': timedelta(seconds=1)},
    'XiGet': {'Request': datetime.now(), 'Delay': timedelta(seconds=5)},
    'CrazyGet': {'Request': datetime.now(), 'Delay': timedelta(seconds=5)},
    'LeetGet': {'Request': datetime.now(), 'Delay': timedelta(seconds=5)},
    'PasteGet': {'Request': datetime.now(), 'Delay': timedelta(seconds=5)},
    'XyiGet': {'Request': datetime.now(), 'Delay': timedelta(seconds=5)},
    'PingGet': {'Request': datetime.now(), 'Delay': timedelta(minutes=5)},
    'HelpGet': {'Request': datetime.now(), 'Delay': timedelta(seconds=10)},
}


Counters = {
    'Global': 0,
    'XiGet': 0,
    'CrazyGet': 0,
    'LeetGet': 0,
    'PasteGet': 0,
    'XyiGet': 0,
    'PasteAdd': 0,
    'PingGet': 0,
    'HelpGet': 0,
    'ExceptionFalls': 0
}


Limits = {
    'XiGet': {'Request': 3000, 'Answer': 4095},
    'XyiGet': {'Request': 3000, 'Answer': 4095},
    'CrazyGet': {'Request': 4000, 'Answer': 4095},
    'LeetGet': {'Request': 4000, 'Answer': 4095},
    'PasteGet': {'Request': 0, 'Answer': 4095},
    'PingGet': {'Request': 0, 'Answer': 4095}
}


