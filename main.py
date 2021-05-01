import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json
import datetime
from Messages import *
import random
import logging

logging.basicConfig(filename='Bot.log', filemode='a', format='[%(levelname)s]:[%(message)s]', encoding='utf-8',
                    level=logging.INFO)


def log_add(s, t=0):
    if t == 0 and False:
        logging.info(f'{datetime.datetime.now().strftime("%d-%b-%y %H:%M:%S")}] - [' + s)
    elif t == 1:
        logging.warning(f'{datetime.datetime.now().strftime("%d-%b-%y %H:%M:%S")}] - [' + s)
    else:
        logging.error(f'{datetime.datetime.now().strftime("%d-%b-%y %H:%M:%S")}] - [' + s)


with open('apiid.txt') as f:
    API, ID = f.read().split(':')
vk_ses = vk_api.VkApi(token=API)
vk_lp = VkBotLongPoll(vk_ses, ID)

DataBase = dict()
DataBase_edited = False
Message_Data = dict()
MessagesCounter = 0
v_kname = dict()
StartedFrom = datetime.datetime
LastRequest = datetime.datetime
LastRequest2 = datetime.datetime
LastRequest3 = datetime.datetime

LastRequest4 = datetime.datetime


# database methods
def get_db():
    global DataBase
    DataBase = list()
    with open('users.json', 'r', encoding='utf-8') as _f:
        DataBase = json.load(_f)


def set_db():
    global DataBase
    if DataBase_edited:
        open('users.json', 'w', encoding='utf-8').close()
        with open('users.json', 'w', encoding='utf-8') as _f:
            json.dump(DataBase, _f, ensure_ascii=False)


# checkers
def check_credit(uid) -> int:
    return DataBase[uid]['credit']


def check_warn(uid) -> int:
    return DataBase[uid]['warn']


def check_banned(uid) -> dict:
    return DataBase[uid]['ban']


def check_name(uid) -> str:
    return DataBase[uid]['name']


def check_name_uid(name) -> str:
    if name == 'serj':
        return '-1'
    for i in DataBase.keys():
        if DataBase[i]['name'] == name:
            return i
    return '-1'


def check_perm(uid) -> str:
    return DataBase[uid]['perm']


# register
def register(uid):
    global DataBase
    global DataBase_edited
    uname = v_kname['first'][0] + v_kname['last']
    uname = uname[:32]
    if not format_checker('name', uname):
        uname = 'serj'
    DataBase[uid] = {'name': uname, 'perm': '0', 'credit': 0, 'warn': 0, 'ban': 0}
    DataBase_edited = True


def unregister(uid):
    global DataBase
    global DataBase_edited
    DataBase.pop(uid)
    DataBase_edited = True


# setters
def set_ban(uid, data):
    global DataBase
    global DataBase_edited
    DataBase[uid]['ban'] = data
    DataBase_edited = True


def set_name(uid, data):
    global DataBase
    global DataBase_edited
    DataBase[uid]['name'] = data
    DataBase_edited = True


def set_perm(uid, data):
    global DataBase
    global DataBase_edited
    DataBase[uid]['perm'] = data
    DataBase_edited = True


def set_warn(uid, data):
    global DataBase
    global DataBase_edited
    DataBase[uid]['warn'] = data
    DataBase_edited = True


def set_credit(uid, data):
    global DataBase
    global DataBase_edited
    DataBase[uid]['credit'] = data
    DataBase_edited = True


def delay() -> bool:
    if check_perm(Message_Data['User_id']) == '*':
        return True
    global LastRequest
    if datetime.datetime.now() - LastRequest < datetime.timedelta(seconds=1):
        return False
    else:
        LastRequest = datetime.datetime.now()
        return True


def delay2() -> bool:
    global LastRequest2
    if check_perm(Message_Data['User_id']) == '*':
        return True
    if datetime.datetime.now() - LastRequest2 < datetime.timedelta(minutes=10):
        return False
    else:
        LastRequest2 = datetime.datetime.now()
        return True


def delay3() -> bool:
    if check_perm(Message_Data['User_id']) == '*':
        return True
    global LastRequest3
    if datetime.datetime.now() - LastRequest3 < datetime.timedelta(seconds=15):
        return False
    else:
        LastRequest3 = datetime.datetime.now()
        return True


def delay4() -> bool:
    if check_perm(Message_Data['User_id']) == '*':
        return True
    global LastRequest4
    if datetime.datetime.now() - LastRequest4 < datetime.timedelta(seconds=5):
        return False
    else:
        LastRequest4 = datetime.datetime.now()
        return True


def format_checker(oid, data) -> bool:
    if oid == 'name':
        if sum([1 for i in data if i != "'" and i != '"']) == len(data) and 0 < len(data) <= 32:
            if data == 'serj':
                return True
            else:
                for i in DataBase.keys():
                    if DataBase[i]['name'] == data:
                        return False
                return True
        else:
            return False
    elif oid == 'perm':
        if data in {'*', '0'}:
            return True
        else:
            return False
    elif oid == 'ban':
        if data in {0, 1}:
            return True
        else:
            return False
    elif oid == 'credit':
        if type(data) == int and 0 < data < 999999999:
            return True
        else:
            return False
    elif oid == 'warn':
        if type(data) == int and 4 > data >= 0:
            return True
        else:
            return False


def up_time():
    return datetime.datetime.now() - StartedFrom


# bot
def send(message):
    vk_ses.method(method='messages.send',
                  values={'chat_id': Message_Data['Chat_id'], 'message': message, 'random_id': 0})


def conf_ban(uid):
    _id = int(uid)
    vk_ses.method(method='messages.removeChatUser',
                  values={'chat_id': Message_Data['Chat_id'], 'user_id': _id})


def send_default(uid):
    send(random.choice(MessagesDict['default']).format(check_name(uid)))


def send_delay_error(uid):
    send(random.choice(MessagesDict['delay']))


def send_user_error(uid):
    send(random.choice(MessagesDict['user_error']).format(check_name(uid)))


def send_bot_error(uid):
    send(random.choice(MessagesDict['bot_error']))


def send_banned(uid):
    send(random.choice(MessagesDict['banned']).format(check_name(uid)))


def send_unbanned(uid):
    send(random.choice(MessagesDict['unbanned']).format(check_name(uid)))


def send_access_error(uid):
    send(random.choice(MessagesDict['access_error']).format(check_name(uid)))


def send_success(uid):
    send('{}, '.format(check_name(uid)) + random.choice(MessagesDict['success']))


def send_unsuccess(uid):
    send(random.choice(MessagesDict['unsuccess']).format(check_name(uid)))


def send_negative(uid):
    send(random.choice(MessagesDict['negative']))


def send_credit_add(uid):
    send(random.choice(MessagesDict['credit_add']) + f'[id{uid}|`]')


def send_warn_add(uid):
    send(random.choice(MessagesDict['warn_add']).format(check_name(uid)))


def send_credit_rd(uid):
    send(random.choice(MessagesDict['credit_rd']) + f'[id{uid}|`]')


def send_warn_rd(uid):
    send(random.choice(MessagesDict['warn_rd']).format(check_name(uid)))


def send_paste():
    send(random.choice(MessagesDict['paste']))


def send_all_notice():
    send(random.choice(MessagesDict['all_notice']))


def send_help(uid):
    send(random.choice(MessagesDict['help']) + f'[id{uid}|`]')


def send_info(uid):
    send(f'[id{uid}|' + MessagesDict['info_other'][0].format(check_name(uid), uid,
                                                             check_perm(uid),
                                                             check_credit(uid),
                                                             check_warn(uid),
                                                             check_banned(uid)) + ']')


def send_debug():
    bans = 0
    admins = 0
    for i in DataBase.keys():
        if check_banned(i):
            bans += 1
        if check_perm(i) == '*':
            admins += 1
    send(
        MessagesDict['debug'][0].format(up_time(), len(DataBase), bans, admins, LastRequest, VER, MessagesCounter))


def send_ban_list():
    send(MessagesDict['ban_list'][0])
    for i in DataBase.keys():
        if check_banned(i):
            send(f'[id{i}|' + MessagesDict['ban_list'][1].format(check_name(i), i, check_name(check_banned(i)[3]),
                                                                 check_banned(i)[2]) + ']')


def send_user_list():
    send(MessagesDict['user_list'][0])
    for i in DataBase.keys():
        send(f'[id{i}|' + MessagesDict['user_list'][1].format(check_name(i), i) + ']')


def send_credit_list():
    send(MessagesDict['credit_list'][0])
    for i in DataBase.keys():
        if check_credit(i) != 0:
            send(f'[id{i}|' + MessagesDict['credit_list'][1].format(check_name(i), i, check_credit(i)) + ']')


def send_warn_list():
    send(MessagesDict['warn_list'][0])
    for i in DataBase.keys():
        if check_warn(i) > 0:
            send(f'[id{i}|' + MessagesDict['warn_list'][1].format(check_name(i), i, check_warn(i)) + ']')


def ban(uid):
    send_banned(uid)
    set_ban(uid, 1)
    conf_ban(uid)


def unban(uid):
    send_unbanned(uid)
    set_ban(uid, 0)


def send_test():
    send_default(Message_Data['User_id'])
    send_delay_error(Message_Data['User_id'])
    send_user_error(Message_Data['User_id'])
    send_bot_error(Message_Data['User_id'])
    send_banned(Message_Data['User_id'])
    send_unbanned(Message_Data['User_id'])
    send_access_error(Message_Data['User_id'])
    send_success(Message_Data['User_id'])
    send_unsuccess(Message_Data['User_id'])
    send_negative(Message_Data['User_id'])
    send_credit_add(Message_Data['User_id'])
    send_warn_add(Message_Data['User_id'])
    send_credit_rd(Message_Data['User_id'])
    send_warn_rd(Message_Data['User_id'])
    send_all_notice()
    send_help(Message_Data['User_id'])
    send_info(Message_Data['User_id'])
    send_debug()
    send_ban_list()
    send_user_list()
    send_credit_list()
    send_warn_list()
    send('The testing is completed, no errors detected')


def req_admin(req) -> str:
    if check_perm(Message_Data['User_id']) == '*':
        return req
    else:
        return 'access_error'


def if_bot_request() -> bool:
    return NAME_L in Message_Data['Message'].lower()


def message_parser() -> dict:
    if 'маяк' in Message_Data['Message'].lower() or 'ping' in Message_Data['Message'].lower():
        return {'Type': req_admin('ping'), 'User_id': Message_Data['User_id']}
    elif 'гениталий' in Message_Data['Message'].lower() or 'сосаль' in Message_Data['Message'].lower() or 'цаль' in \
            Message_Data['Message'].lower() or 'genetaly' in Message_Data['Message'].lower():
        return {'Type': 'Genetaly', 'User_id': Message_Data['User_id']}
    elif '/hack' in Message_Data['Message'].lower() or '/взлом' in Message_Data['Message'].lower():
        return {'Type': 'hack', 'User_id': Message_Data['User_id']}
    elif 'няша сосешь' in Message_Data['Message'].lower() or 'няша нахуй' in Message_Data[
        'Message'].lower() or 'няша сосёшь' in Message_Data['Message'].lower() or 'няша соси' in Message_Data[
        'Message'].lower() or 'няша пососи' in Message_Data['Message'].lower() or 'няша хуй' in Message_Data[
        'Message'].lower() or 'няша функционал' in Message_Data['Message'].lower():
        return {'Type': 'sucky', 'User_id': Message_Data['User_id']}
    elif 'setname' in Message_Data['Message'].lower() or 'сетнейм' in Message_Data['Message'].lower():
        if Message_Data['Reply']['Exist']:
            tmp = Message_Data['Reply']['User_id']
        else:
            tmp = Message_Data['User_id']
        tmp2 = Message_Data['Message'][len(NAME_L) + len(' сетнейм '):]
        if not format_checker('name', tmp2):
            return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
        if tmp in DataBase.keys():
            return {'Type': req_admin('set_name'), 'User_id': tmp, 'Name': tmp2,
                    'Admin_id': Message_Data['User_id']}
        else:
            return {'Type': req_admin('bot_error'), 'User_id': Message_Data['User_id']}
    elif 'setperm' in Message_Data['Message'].lower() or 'сетперм' in Message_Data['Message'].lower():
        if Message_Data['Reply']['Exist']:
            tmp = Message_Data['Reply']['User_id']
        else:
            tmp = Message_Data['User_id']
        tmp2 = Message_Data['Message'][len(NAME_L) + len(' сетперм '):]
        if not format_checker('perm', tmp2):
            return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
        if tmp in DataBase.keys():
            return {'Type': req_admin('set_perm'), 'User_id': tmp, 'Perm': tmp2,
                    'Admin_id': Message_Data['User_id']}
        else:
            return {'Type': req_admin('bot_error'), 'User_id': Message_Data['User_id']}
    elif 'добавь' in Message_Data['Message'].lower():
        if Message_Data['Reply']['Exist']:
            tmp = Message_Data['Reply']['Message']
            tmp = str(tmp).replace('\n', ' ')
            tmp = str(tmp).replace('\t', ' ')
            if tmp not in paste:
                return {'Type': req_admin('pasteadd'), 'User_id': Message_Data['User_id'], 'Paste': tmp}
            else:
                return {'Type': req_admin('user_error'), 'User_id': Message_Data['User_id']}
        if len(Message_Data['Message'].lower()) > len(NAME_L) + len(' добавь'):
            tmp = Message_Data['Message'][len(NAME_L) + len(' добавь '):]
            tmp = str(tmp).replace('\n', ' ')
            tmp = str(tmp).replace('\t', ' ')
            if tmp not in paste:
                return {'Type': req_admin('pasteadd'), 'User_id': Message_Data['User_id'], 'Paste': tmp}
            else:
                return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
        else:
            return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
    elif 'инфо' in Message_Data['Message'].lower() or 'инфа' in Message_Data['Message'].lower():
        if Message_Data['Reply']['Exist']:
            tmp = Message_Data['Reply']['User_id']
            if tmp in DataBase.keys():
                return {'Type': 'info', 'User_id': tmp}
            else:
                return {'Type': 'bot_error', 'User_id': Message_Data['User_id']}
        if len(Message_Data['Message'].lower()) > len(NAME_L) + len(' инфо'):
            tmp = Message_Data['Message'][len(NAME_L) + len(' инфо '):]
            if not str(tmp).isnumeric():
                tmp = check_name_uid(tmp)
            if tmp != '-1' and tmp in DataBase:
                return {'Type': 'info', 'User_id': tmp}
            else:
                return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
        return {'Type': 'info', 'User_id': Message_Data['User_id']}
    elif 'лист' in Message_Data['Message'].lower():
        if 'all' in Message_Data['Message'].lower() or 'база' in Message_Data['Message'].lower():
            return {'Type': req_admin('List_all'), 'User_id': Message_Data['User_id']}
        elif 'петухи' in Message_Data['Message'].lower() or 'бан' in Message_Data['Message'].lower():
            return {'Type': req_admin('List_ban'), 'User_id': Message_Data['User_id']}
        elif 'варн' in Message_Data['Message'].lower():
            return {'Type': 'List_warn', 'User_id': Message_Data['User_id']}
        elif 'кредит' in Message_Data['Message'].lower():
            return {'Type': 'List_credit', 'User_id': Message_Data['User_id']}
        else:
            return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
    elif 'тест' in Message_Data['Message'].lower():
        return {'Type': req_admin('Test'), 'User_id': Message_Data['User_id']}
    elif 'хелп' in Message_Data['Message'].lower() or 'помощь' in Message_Data['Message'].lower():
        return {'Type': 'help', 'User_id': Message_Data['User_id']}
    elif 'дебаг' in Message_Data['Message'].lower() or 'debug' in Message_Data['Message'].lower():
        return {'Type': req_admin('debug'), 'User_id': Message_Data['User_id']}
    elif 'анварн' in Message_Data['Message'].lower():
        if Message_Data['Reply']['Exist']:
            tmp = Message_Data['Reply']['User_id']
            if tmp in DataBase.keys() and check_perm(tmp) != '*':
                return {'Type': req_admin('warn_rd'), 'User_id': tmp}
            else:
                return {'Type': req_admin('bot_error'), 'User_id': Message_Data['User_id']}
        if len(Message_Data['Message'].lower()) > len(NAME_L) + len(' анварн'):
            tmp = Message_Data['Message'][len(NAME_L) + len(' анварн '):]
            if not str(tmp).isnumeric():
                tmp = check_name_uid(tmp)
            if tmp != '-1' and tmp in DataBase:
                if check_perm(tmp) != '*':
                    return {'Type': req_admin('warn_rd'), 'User_id': tmp}
                else:
                    return {'Type': req_admin('unsuccess'), 'User_id': tmp}
            else:
                return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
        else:
            return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
    elif 'варн' in Message_Data['Message'].lower():
        if Message_Data['Reply']['Exist']:
            tmp = Message_Data['Reply']['User_id']
            if tmp in DataBase.keys() and check_perm(tmp) != '*':
                print(tmp)
                return {'Type': req_admin('warn_add'), 'User_id': tmp}
            else:
                return {'Type': req_admin('bot_error'), 'User_id': Message_Data['User_id']}
        if len(Message_Data['Message'].lower()) > len(NAME_L) + len(' варн'):
            tmp = Message_Data['Message'][len(NAME_L) + len(' варн '):]
            if not str(tmp).isnumeric():
                tmp = check_name_uid(tmp)
            if tmp != '-1' and tmp in DataBase:
                if check_perm(tmp) != '*':
                    return {'Type': req_admin('warn_add'), 'User_id': tmp}
                else:
                    return {'Type': req_admin('unsuccess'), 'User_id': tmp}
            else:
                return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
        else:
            return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
    elif 'анбан' in Message_Data['Message'].lower():
        if Message_Data['Reply']['Exist']:
            tmp = Message_Data['Reply']['User_id']
            if tmp in DataBase.keys() and check_perm(tmp) != '*':
                print(tmp)
                return {'Type': req_admin('unbanned'), 'User_id': tmp}
            else:
                return {'Type': req_admin('bot_error'), 'User_id': Message_Data['User_id']}
        if len(Message_Data['Message'].lower()) > len(NAME_L) + len(' анбан'):
            tmp = Message_Data['Message'][len(NAME_L) + len(' анбан '):]
            if not str(tmp).isnumeric():
                tmp = check_name_uid(tmp)
            if tmp != '-1' and tmp in DataBase:
                if check_perm(tmp) != '*':
                    return {'Type': req_admin('unbanned'), 'User_id': tmp}
                else:
                    return {'Type': req_admin('unsuccess'), 'User_id': tmp}
            else:
                return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
        else:
            return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
    elif 'бан' in Message_Data['Message'].lower():
        if Message_Data['Reply']['Exist']:
            tmp = Message_Data['Reply']['User_id']
            if tmp in DataBase.keys() and check_perm(tmp) != '*':
                print(tmp)
                return {'Type': req_admin('banned'), 'User_id': tmp}
            else:
                return {'Type': req_admin('bot_error'), 'User_id': Message_Data['User_id']}
        if len(Message_Data['Message'].lower()) > len(NAME_L) + len(' бан'):
            tmp = Message_Data['Message'][len(NAME_L) + len(' бан '):]
            if not str(tmp).isnumeric():
                tmp = check_name_uid(tmp)
            if tmp != '-1' and tmp in DataBase:
                if check_perm(tmp) != '*':
                    return {'Type': req_admin('banned'), 'User_id': tmp}
                else:
                    return {'Type': req_admin('unsuccess'), 'User_id': tmp}
            else:
                return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
        else:
            return {'Type': 'user_error', 'User_id': Message_Data['User_id']}
    return {'Type': 'default', 'User_id': Message_Data['User_id']}


def if_auto_warn():
    lst = ['@all', 'морген топ', 'морген класс', 'фараох топ', 'фараох класс', 'фараон топ', 'фараон класс',
           'фара топ', 'фара класс', 'моргерштерн топ', 'моргерштерн класс', 'моргенштерн топ', 'моргенштерн класс',
           'morgenshtren топ', 'morgenshtren класс', 'morgershtren топ', 'morgershtren класс', 'pharaon топ',
           'pharaon класс',
           'pharaoh топ', 'pharaoh класс']
    if any([i in Message_Data['Message'].lower() for i in lst]) and '' != req_admin(''):
        send_negative(Message_Data['User_id'])
        send_warn_add(Message_Data['User_id'])
        set_warn(Message_Data['User_id'], check_warn(Message_Data['User_id']) + 1)
        log_add('Auto-Warn-Guard', 1)
    elif 'функционал' in Message_Data['Message'].lower() and 'функциональность' not in Message_Data[
        'Message'].lower() and delay3():
        send(
            'Понимаешь ли в чём дело, функционал - это математическая функция или главный герой романа Сергея Лукьяненко "Черновик". То, что ты подразумеваешь под этим словом, называется функциональность. Или какие-то новые правила русского языка придумали? Я не знаю. Я... Просто мои полномочия всё...')
    if Message_Data['Reply']['Exist'] and any(
            [i in Message_Data['Message'].lower() for i in ['+', 'да согл', 'слит']]) and Message_Data['Reply'][
        'User_id'] != Message_Data['User_id'] and delay4():
        set_credit(Message_Data['Reply']['User_id'], check_credit(Message_Data['Reply']['User_id']) + 1)
        send_credit_add(Message_Data['Reply']['User_id'])
    if Message_Data['Reply']['Exist'] and any(
            [i in Message_Data['Message'].lower() for i in ['-', 'пошел нахуй', 'не согл']]) and Message_Data['Reply'][
        'User_id'] != Message_Data['User_id'] and check_credit(Message_Data['User_id']) >= check_credit(
            Message_Data['Reply']['User_id']) and delay4():
        set_credit(Message_Data['Reply']['User_id'], check_credit(Message_Data['Reply']['User_id']) - 1)
        send_credit_rd(Message_Data['Reply']['User_id'])


def main_loop():
    global Message_Data
    global MessagesCounter
    global StartedFrom
    global LastRequest
    global LastRequest2
    global LastRequest3
    global LastRequest4
    global v_kname
    log_add('Bot Started')

    LastRequest4 = datetime.datetime.now()
    LastRequest3 = datetime.datetime.now()
    LastRequest2 = datetime.datetime.now()
    LastRequest = datetime.datetime.now()
    StartedFrom = datetime.datetime.now()
    get_db()
    for i in DataBase.keys():
        set_credit(i, 0)
        set_warn(i, 0)
    set_db()

    for event in vk_lp.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message['from_id'] > 0:
            log_add('Executing started')
            Message_Data = {'User_id': str(event.message['from_id']), 'Chat_id': int(str(event.message['peer_id'])[-1]),
                            'Message': event.message['text'], 'Reply': {'Exist': False, 'User_id': '-1'}}
            if 'reply_message' in event.message and event.message['reply_message']['from_id'] > 0:
                Message_Data['Reply'] = {'Exist': True, 'User_id': str(event.message['reply_message']['from_id']),
                                         'Message': str(event.message['reply_message']['text'])}
            get_db()
            v_kname = vk_ses.method(method='users.get', values={'user_ids': int(Message_Data['User_id'])})[0]
            v_kname = {'last': v_kname['last_name'], 'first': v_kname['first_name']}
            if not (Message_Data['User_id'] in DataBase):
                register(Message_Data['User_id'])
                log_add('Registered')
            log_add(f'{v_kname["first"]} {v_kname["last"]} id{Message_Data["User_id"]}' +
                    f' aka {check_name(Message_Data["User_id"])} sent in {Message_Data["Chat_id"]} ' +
                    f'- [{Message_Data["Message"]}, Reply User_id:{Message_Data["Reply"]["User_id"]}]')
            if_auto_warn()
            if not check_banned(Message_Data['User_id']):
                if DataBase[Message_Data['User_id']]['warn'] >= 3:
                    ban(Message_Data['User_id'])
                    set_warn(Message_Data['User_id'], 0)
                    log_add('Auto-Ban (warn overflow)')
                else:
                    if delay() and if_bot_request():
                        log_add('Bot_Request detected')
                        parsed = message_parser()
                        if parsed['Type'] == 'default':
                            send_default(parsed['User_id'])
                            log_add('default Successful')
                        elif parsed['Type'] == 'Genetaly':
                            send(
                                f'@id181693538 ( пингую гениталия сосаля ) @id646897493 (и его педальную) @id202197700 ( бригаду. по просьбе {check_name(parsed["User_id"])}а )')
                            log_add('User_Ping(Tsal) Successful')
                        elif parsed['Type'] == 'hack':
                            if delay2():
                                send(f'{check_name(parsed["User_id"])}, Шалость удалась!')
                                send(f'[id{parsed["User_id"]}|' + MessagesDict['info_other'][0].format(
                                    check_name(parsed["User_id"]), parsed["User_id"],
                                    '*', '999', '0', check_banned(parsed["User_id"])) + ']')
                                send_bot_error(parsed['User_id'])
                                send_bot_error(parsed['User_id'])
                                send_bot_error(parsed['User_id'])
                                send(f'[id{parsed["User_id"]}|' + MessagesDict['info_other'][0].format(
                                    'глупый какер', parsed["User_id"], '0', '-1', '999', '1') + ']')
                                send_credit_rd(parsed['User_id'])
                            else:
                                send('...')
                            log_add('/Hack Successful')
                        elif parsed['Type'] == 'info':
                            send_info(parsed['User_id'])
                            log_add('info Successful')
                        elif parsed['Type'] == 'pasteadd':
                            with open('paste.txt', 'a', encoding='utf-8') as _f:
                                _f.write('\n' + parsed['Paste'])
                            paste.append(parsed['Paste'])
                            send_success(parsed['User_id'])
                            log_add('Pastadd Successful')
                        elif parsed['Type'] == 'sucky':
                            if delay3() or check_perm(parsed['User_id']) == '*':
                                send_paste()
                            else:
                                send('Ты блять сосешь да? Фаллос шоп ходячий...')
                            log_add('Sucky Successful')
                        elif parsed['Type'] == 'debug':
                            send_debug()
                            log_add('Debug Successful')
                        elif parsed['Type'] == 'Test':
                            send_test()
                            log_add('Test Successful')
                        elif parsed['Type'] == 'List_all':
                            send_user_list()
                            log_add('List Successful')
                        elif parsed['Type'] == 'List_warn':
                            send_warn_list()
                            log_add('List Successful')
                        elif parsed['Type'] == 'List_ban':
                            send_ban_list()
                            log_add('List Successful')
                        elif parsed['Type'] == 'List_credit':
                            send_credit_list()
                            log_add('List Successful')
                        elif parsed['Type'] == 'help':
                            send_help(parsed['User_id'])
                            log_add('Help Successful')
                        elif parsed['Type'] == 'set_name':
                            set_name(parsed['User_id'], parsed['Name'])
                            send_success(parsed['Admin_id'])
                            log_add(f'Name Set Successful id:{parsed["User_id"]} name:{parsed["Name"]}')
                        elif parsed['Type'] == 'set_perm':
                            set_perm(parsed['User_id'], parsed['Perm'])
                            send_success(parsed['Admin_id'])
                            log_add(f'Perms Set Successful id:{parsed["User_id"]} name:{parsed["Perm"]}')
                        elif parsed['Type'] == 'warn_add':
                            send_warn_add(parsed['User_id'])
                            set_warn(parsed['User_id'], check_warn(parsed['User_id']) + 1)
                            log_add('Warn Successful')
                        elif parsed['Type'] == 'warn_rd':
                            send_warn_rd(parsed['User_id'])
                            set_warn(parsed['User_id'], max(0, check_warn(parsed['User_id']) - 1))
                            log_add('Unwarn Successful')
                        elif parsed['Type'] == 'banned':
                            ban(parsed['User_id'])
                            log_add('Ban Successful')
                        elif parsed['Type'] == 'unbanned':
                            unban(parsed['User_id'])
                            log_add('Unban Successful')
                        elif parsed['Type'] == 'ping':
                            send_all_notice()
                            log_add('Ping Successful')
                        elif parsed['Type'] == 'access_error':
                            log_add('Access_Error', 1)
                            send_access_error(parsed['User_id'])
                        elif parsed['Type'] == 'bot_error':
                            log_add('Bot_Error', 1)
                            send_bot_error(parsed['User_id'])
                        elif parsed['Type'] == 'user_error':
                            send_user_error(parsed['User_id'])
                            log_add('User_Error', 1)
                        elif parsed['Type'] == 'unsuccess':
                            send_unsuccess(parsed['User_id'])
                            log_add('Failure', 1)
                    elif not delay() and if_bot_request():
                        log_add('delay_error')
                        send_delay_error(Message_Data['User_id'])
            else:
                send_negative(Message_Data['User_id'])
                ban(Message_Data['User_id'])
                log_add('Auto-Ban', 1)
            log_add('Executed successfully')
            set_db()
            MessagesCounter += 1


main_loop()
