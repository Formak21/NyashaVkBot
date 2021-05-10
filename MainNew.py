import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json
import logging
import random
from datetime import *

with open('apiid.txt') as f:
    API, ID = f.read().split(':')
vk_ses = vk_api.VkApi(token=API)
vk_lp = VkBotLongPoll(vk_ses, ID)

with open('paste.txt', 'r', encoding='utf-8') as _f:
    paste = _f.read().split('\n')

VER = '2.0.0 BETA'
NAME_U = 'Няша'
NAME_L = 'няша'
MAX_WARN = 3
DEFAULT_NAME = 'serj'
Error = '-1-1'
Database = {}
DatabaseEdited = False
MessageData = {'Type': str(), 'User_id': str(), 'Message': str(), 'Attachment': str(),
               'Reply': {'Exist': bool(), 'Type': str(), 'User_id': str(), 'Message': str(),
                         'Attachment': str()},
               'Name': {'First': str(), 'Last': str(), 'Name': str()}}
UpFrom = datetime.now()
LastRequest = {'0': {'default': {'Time': datetime.now(), 'Delay': timedelta(seconds=2)},
                     'hack': {'Time': datetime.now(), 'Delay': timedelta(minutes=2)},
                     'paste': {'Time': datetime.now(), 'Delay': timedelta(seconds=15)},
                     'rating': {'Time': datetime.now(), 'Delay': timedelta(seconds=5)}},
               '*': {'default': {'Time': datetime.now(), 'Delay': timedelta(seconds=0)},
                     'hack': {'Time': datetime.now(), 'Delay': timedelta(seconds=0)},
                     'paste': {'Time': datetime.now(), 'Delay': timedelta(seconds=0)},
                     'rating': {'Time': datetime.now(), 'Delay': timedelta(seconds=0)}}
               }
MessageCounter = 0
Parsed = {'Type': str(),
          'Data': {'User_id': str(), 'Name': str(), 'Perm': str(), 'Credit': int(), 'Warn': int(),
                   'Ban': int(), 'Data': str()}}

logging.basicConfig(filename='NewBot.log', filemode='a', format='[%(levelname)s]:[%(message)s]', level=logging.INFO)


def log_add(s, t=0):
    if t == 0 and False:
        logging.info(f'{datetime.now().strftime("%d-%b-%y %H:%M:%S")}] - [' + s)
    elif t == 1:
        logging.warning(f'{datetime.now().strftime("%d-%b-%y %H:%M:%S")}] - [' + s)
    else:
        logging.error(f'{datetime.now().strftime("%d-%b-%y %H:%M:%S")}] - [' + s)


def get_db():
    global Database
    Database = list()
    with open('newusers.json', 'r', encoding='utf-8') as f:
        Database = json.load(f)


def set_db():
    global Database
    if DatabaseEdited:
        open('newusers.json', 'w', encoding='utf-8').close()
        with open('newusers.json', 'w', encoding='utf-8') as f:
            json.dump(Database, f, ensure_ascii=False)


def paste_updater(tmp):
    tmp = str(tmp).replace('\n', ' ')
    tmp = str(tmp).replace('\t', ' ')
    paste.append(tmp)
    with open('paste.txt', 'a', encoding='utf-8') as f:
        f.write('\n' + tmp)


def vk_name_get(uid):
    name = vk_ses.method(method='users.get', values={'user_ids': int(uid)})[0]
    return {'first': name['first_name'], 'last': name['last_name']}


def id_check(name):
    global Parsed
    if name != DEFAULT_NAME:
        for i in Database.keys():
            if Database[i]['name'] == name:
                return i
    Parsed['Type'] = 'user_error'
    return Error


def name_check(uid):
    register(uid)
    return Database[uid]['Name']


def name_set(uid, data):
    global Database
    global DatabaseEdited
    global Parsed
    register(uid)
    if format_check('Name', data):
        Database[uid]['Name'] = data
        DatabaseEdited = True
        return True
    Parsed['Type'] = 'user_error'
    return False


def perm_check(uid):
    register(uid)
    return Database[uid]['Perm']


def perm_set(uid, data):
    global Database
    global DatabaseEdited
    global Parsed
    register(uid)
    if format_check('Perm', data):
        Database[uid]['Perm'] = data
        DatabaseEdited = True
        return True
    Parsed['Type'] = 'user_error'
    return False


def ban_check(uid):
    register(uid)
    return Database[uid]['Ban']


def ban_set(uid, data):
    global Database
    global DatabaseEdited
    global Parsed
    register(uid)
    if format_check('Ban', data):
        Database[uid]['Ban'] = data
        DatabaseEdited = True
        return True
    Parsed['Type'] = 'user_error'
    return False


def warn_check(uid):
    register(uid)
    return Database[uid]['Warn']


def warn_set(uid, data):
    global Database
    global DatabaseEdited
    global Parsed
    register(uid)
    if format_check('Warn', data):
        Database[uid]['Warn'] = data
        DatabaseEdited = True
        return True
    Parsed['Type'] = 'user_error'
    return False


def credit_check(uid):
    register(uid)
    return Database[uid]['Credit']


def credit_set(uid, data):
    global Database
    global DatabaseEdited
    global Parsed
    register(uid)
    if format_check('Credit', data):
        Database[uid]['Credit'] = data
        DatabaseEdited = True
        return True
    Parsed['Type'] = 'user_error'
    return False


def request_check(uid):
    register(uid)
    return Database[uid]['Request']


def request_set(uid, data):
    global Database
    global DatabaseEdited
    register(uid)
    Database[uid]['Request'] = data


def register(uid):
    global Database
    global DatabaseEdited
    if uid not in Database.keys():
        name = vk_name_get(uid)
        name = name['first'][0] + name['last']
        name = name[:64]
        if not format_check('Name', name):
            name = DEFAULT_NAME
        Database[uid] = {'Name': name, 'Perm': '0', 'Credit': 0, 'Warn': 0,
                         'Ban': 0, 'Requests': 0, 'Ver': VER}
        DatabaseEdited = True


def format_check(reqtype, data):
    global Parsed
    datatypes = {'Perm': {'0', '1', '2', '3', '*'}, 'Ban': {0, 1}}
    if reqtype == 'Ban' and data in datatypes['Ban']:
        return True
    elif reqtype == 'Perm' and data in datatypes['Perm']:
        return True
    elif reqtype == 'Warn' and 0 <= data <= MAX_WARN:
        return True
    elif reqtype == 'Credit' and -1000000 <= data <= 1000000:
        return True
    elif reqtype == 'Name' and 0 < len(data) <= 64 and all([i.isalpha() or i.isnumeric() for i in data]) and all(
            [Database[i]['Name'] != data for i in Database.keys()]):
        return True
    else:
        Parsed['Type'] = 'user_error'
        return False


def delay_check(reqtype='default'):
    global LastRequest
    global Parsed
    perm = perm_check(MessageData['User_id'])
    if perm not in LastRequest.keys():
        perm = '0'
    if datetime.now() - LastRequest[perm][reqtype]['Time'] <= LastRequest[perm][reqtype]['Delay']:
        LastRequest[perm][reqtype]['Time'] = datetime.now()
        return True
    Parsed['Type'] = 'delay_error'
    return False


def f(n):
    if n <= 1:
        return 1
    return f(n - 1) * n


def up_time():
    return datetime.now() - UpFrom


def send(message='пустое сообщение', attachment=''):
    if attachment != '':
        vk_ses.method(method='messages.send',
                      values={'chat_id': MessageData['Chat_id'], 'message': message, 'attachment': attachment,
                              'random_id': 0})
    else:
        vk_ses.method(method='messages.send',
                      values={'chat_id': MessageData['Chat_id'], 'message': message, 'random_id': 0})


def conf_ban(uid):
    _id = int(uid)
    vk_ses.method(method='messages.removeChatUser',
                  values={'chat_id': MessageData['Chat_id'], 'user_id': _id})


print(f(5))