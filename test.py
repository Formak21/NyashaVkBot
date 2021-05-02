import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json
import datetime

with open('apiid.txt') as f:
    API, ID = f.read().split(':')
vk_ses = vk_api.VkApi(token=API)
vk_lp = VkBotLongPoll(vk_ses, ID)

VER = '0.1.1 ALPHA'
chat = int()
users = list()
messageid = int()
n = 0
DateTimeStartup = datetime.datetime
LastMessageDt = datetime.datetime


def Mdelay() -> int:
    global LastMessageDt
    if datetime.datetime.now() - LastMessageDt < datetime.timedelta(seconds=1):
        return 1
    else:
        LastMessageDt = datetime.datetime.now()
        return 0


def Mformat(text) -> bool:
    if text.isalpha() and len(text) < 24:
        return True
    else:
        return False


def get_perms(uid) -> str:
    return {i['id']: i['perms'] for i in users}[uid]


def get_name(uid) -> str:
    return {i['id']: i['name'] for i in users}[uid]


def get_db():
    global users
    users = []
    with open('users.json') as _f:
        users = json.load(_f)


def set_db():
    global users
    open('users.json', 'w').close()
    with open('users.json', 'w') as _f:
        json.dump(users, _f)
    users = []


def message_parser(message, uid) -> list:
    global users
    if 'няша' in message.lower():
        if Mdelay() == 1:
            send(f'@id{uid} (жди.)')
            return [-1]
        if message[:12] == 'Няша СетИмя ':
            tmp = message[12:].split()
            return [1, uid, tmp[0], tmp[1]]
        elif message[:10] == 'Няша СетПерм ':
            tmp = message[10:].split()
            return [2, uid, tmp[0], tmp[1]]
        elif 'Няша бан нахой' in message:
            return [3, uid, message[17:].split()[0], message[16:].split()[1]]
        elif 'ты же всем отвечаешь да?' in message.lower():
            return [4, uid, message]
        elif 'маяк' in message.lower():
            return [5, uid, message]
        elif 'няша инфо' in message.lower()[:10]:
            if len(message.lower()) < 11:
                return [6, uid, uid]
            else:
                return [6, uid, message.lower()[11:]]
        elif 'нахуй' in message.lower():
            return [7, uid, message]
        elif 'eblan' in message:
            return [8, uid, message]
        elif 'хуй' in message:
            return [9, uid, message]
        elif 'дебаг' in message:
            return [10, uid, message]
        elif 'помощь' in message.lower() or 'faq' in message.lower() or 'хелп' in message.lower() or 'help' in message.lower():
            return [11, uid, message]
        elif 'Няша унбан нахой ' == message[:19]:
            return [12, uid, message[18:]]
        elif 'Няша бдлист' in message:
            return [13, uid]
        elif 'Няша петухи' in message:
            return [14, uid]

        else:
            return [0, uid, message]
    else:
        return [0, uid, message]


def send(message):
    global users
    global chat
    global messageid
    vk_ses.method(method='messages.send',
                  values={'chat_id': chat, 'message': message, 'random_id': 0})


def db_check(uid) -> bool:
    global users
    if uid not in [i['id'] for i in users]:
        print(f'Added to db - {uid}')
        users.append(
            {'id': str(uid), 'perms': '0', 'name': '-', 'credit': 0, 'warn': 0, 'ban': False,
             'bdate': '-',
             'ida': '-', 'breason': ''})
        return True
    else:
        return False


def warn_check(uid):
    global users
    return users[[i for i in range(len(users)) if users[i]['id'] == uid][0]]['warn']


def ban_check(uid):
    global users
    return users[[i for i in range(len(users)) if users[i]['id'] == uid][0]]['ban']


def credit_check(uid):
    global users
    return users[[i for i in range(len(users)) if users[i]['id'] == uid][0]]['credit']


def id_check(uid) -> int:
    global users
    k = [i for i in range(len(users)) if users[i]['id'] == uid]
    if len(k):
        return k[0]
    else:
        return -1


def ban(parsed) -> bool:
    global users
    if get_perms(parsed[1]) == '*':
        k = id_check(parsed[2])
        print(k)
        if k != -1:
            users[k]['ban'] = True
            users[k]['bdate'] = str(LastMessageDt)
            users[k]['ida'] = parsed[1]
            users[k]['breason'] = parsed[3]
            users[k]['warn'] = 0
            users[k]['credit'] = 0
            users[k]['perms'] = '0'
            send(f'@id{parsed[1]}, Петух забанен')
            vk_ses.method(method='messages.removeChatUser',
                          values={'chat_id': chat, 'user_id': parsed[2]})
            return True
        else:
            send(f'@id{parsed[1]}, Ты еблан?')
            return False
    else:
        send(f'@id{parsed[1]}, Пошел нахуй петушок')
        return False


def unban(parsed) -> bool:
    global users
    if get_perms(parsed[1]) == '*':
        k = id_check(parsed[2])
        if k != -1:
            users[k]['ban'] = False
            users[k]['bdate'] = '-'
            users[k]['ida'] = '-'
            users[k]['breason'] = '-'
            send(f'@id{parsed[1]}, Помни, петухи не исправляются.')
            return True
        else:
            send(f'@id{parsed[1]}, Ты еблан?')
            return False
    else:
        send(f'@id{parsed[1]}, Пошел нахуй петушок')
        return False


def bdlist(parsed):
    if get_perms(parsed[1]) == '*':
        for i in users:
            info([None, None, i['id']])
    else:
        send(f'@id{parsed[1]} (У тебя прав нет, идиот)')
        return False


def banned(parsed):
    if get_perms(parsed[1]) == '*':
        for i in users:
            if i['ban']:
                info([None, None, i['id']])
    else:
        send(f'@id{parsed[1]} (У тебя прав нет, идиот)')
        return False


def warn(parsed):
    pass


def edit_name(parsed) -> bool:
    global users
    global chat
    global messageid
    if get_perms(parsed[1]) == '*' or parsed[1] == parsed[2]:
        k = id_check(parsed[2])
        if k != -1 and Mformat(parsed[3]):
            users[k]['name'] = parsed[3]
            send(f'@id{parsed[1]} (Готово)')
            print(f'Edited by {parsed[1]}, name {parsed[2]} to {parsed[3]} in db')
            return True
        else:
            send(f'@id{parsed[1]} (Ты тупой нахуй?)')
            return False
    else:
        send(f'@id{parsed[1]} (У тебя прав нет, идиот)')
        return False


def edit_perms(parsed) -> bool:
    global users
    global chat
    global messageid
    if get_perms(parsed[1]) == '*':
        k = id_check(parsed[2])
        if k != -1 and (parsed[3] in {'*', '0'}):
            users[k]['perms'] = parsed[3]
            send(f'@id{parsed[1]} (Готово)')
            print(f'Edited by {parsed[1]}, name {parsed[2]} to {parsed[3]} in db')
            return True
        else:
            send(f'@id{parsed[1]} (Ты тупой нахуй?)')
            return False
    else:
        send(f'@id{parsed[1]} (Псина, куда полез?!)')
        return False


def eblan(parsed):
    send(
        f'@id{parsed[1]} (bolshoy brat vsegda sledit za toboy) eto znachit chto ya mogu vtorngutsya v tvou lichnuu jizn i ispolzovat vse toboy skazanoe protiv tebya \n-retardbot')


def mayak(parsed):
    if get_perms(parsed[1]) == '*':
        send('Вставай, проклятьем заклеймённый, Весь мир голодных и рабов! @all @all @all')
        send('Боженька зовет вас, через вашу милую Няшу @online @online @online')
    else:
        send(f'@id{parsed[1]} (Милый, А НЕ ПОЙТИ ЛИ БЫ ТЕБЕ НАХУЙ?)')


def info(parsed):
    k = id_check(parsed[2])
    if parsed[2] == parsed[1]:
        send(
            f'@id{parsed[1]} (Ваше имя: {get_name(parsed[1])}). Ваши права: {get_perms(parsed[1])}, Ваш id: {parsed[1]}\n Бан:{ban_check(parsed[2])}\n Соц Рейтинг:{credit_check(parsed[2])}\n Варны:{warn_check(parsed[2])}\n Причина Бана:{users[k]["breason"]}\n Дата Бана:{users[k]["bdate"]}')
    else:
        if k == -1:
            send('Сбой')
            return
        send(
            f'@id{parsed[2]} (Имя: {get_name(parsed[2])}). Права: {get_perms(parsed[2])}, id: {parsed[2]}\n Бан:{ban_check(parsed[2])}\n Соц Рейтинг:{credit_check(parsed[2])}\n Варны:{warn_check(parsed[2])}\n Причина Бана:{users[k]["breason"]}\n Дата Бана:{users[k]["bdate"]}')


def debuginfo(parsed):
    send(f'''@id{parsed[1]} (Время работы:{datetime.datetime.now() - DateTimeStartup}, 
Размер Базы Данных:{len(users)}, 
Количество Админов:{sum([1 for i in users if i["perms"] == "*"])}, 
Сообщений Обработанно: {n}, Забаненых: {sum([1 for i in users if i["ban"]])},
Последний реквест {LastMessageDt})''')


def da(parsed):
    send(f'@id{parsed[1]} (Да.)')


def huy(parsed):
    send(f'@id{parsed[1]} (жди нахуй.)')


def nahuy(parsed):
    if get_perms(parsed[1]) == '*':
        send(f'@id{parsed[1]} (Хозяин, ну почему же вы так со мной, я же хорошая девочка...)')
    else:
        send(f'@id{parsed[1]} (Я тебе ща бан дам нахуй, холопище)')


def help(parsed):
    send(f'@id{parsed[1]} (Ты серьезно настолько туп, что не можешь запомнить 3 команды?)')


def default(parsed):
    if 'Няша' in parsed[2]:
        send(f'@id{parsed[1]} (Ась, мой сладенький?)')
    elif 'няша' in parsed[2]:
        send(f'@id{parsed[1]} (Чё, тебе?)')


def main_loop() -> int:
    global users
    global chat
    global messageid
    global n
    global DateTimeStartup
    global LastMessageDt
    DateTimeStartup = datetime.datetime.now()
    LastMessageDt = datetime.datetime.now()
    for event in vk_lp.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
            print(event.message)
            messageid = event.message['conversation_message_id']
            chat = int(str(event.message['peer_id'])[-1])
            get_db()
            users_edited = db_check(str(event.message['from_id']))
            if ban_check(str(event.message['from_id'])):
                ban([None, ID, event.message['from_id'], 'АВТОБАН'])
            else:
                parsed = message_parser(event.message['text'], str(event.message['from_id']))
                print(parsed, event.message['text'])
                if parsed[0] == 0:
                    default(parsed)
                elif parsed[0] == 1:
                    users_edited = (edit_name(parsed) or users_edited)
                elif parsed[0] == 2:
                    users_edited = (edit_perms(parsed) or users_edited)
                elif parsed[0] == 3:
                    users_edited = (ban(parsed) or users_edited)
                elif parsed[0] == 4:
                    da(parsed)
                elif parsed[0] == 5:
                    mayak(parsed)
                elif parsed[0] == 6:
                    info(parsed)
                elif parsed[0] == 7:
                    nahuy(parsed)
                elif parsed[0] == 8:
                    eblan(parsed)
                elif parsed[0] == 9:
                    huy(parsed)
                elif parsed[0] == 10:
                    debuginfo(parsed)
                elif parsed[0] == 11:
                    help(parsed)
                elif parsed[0] == 12:
                    users_edited = (unban(parsed) or users_edited)
                elif parsed[0] == 13:
                    bdlist(parsed)
                elif parsed[0] == 14:
                    banned(parsed)
                if users_edited:
                    set_db()
            n += 1
    return 0


main_loop()
