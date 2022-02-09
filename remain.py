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

# Tags
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

# Messages
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
    'help_message': '',
    'debug_message': '',
    'info_message': ''
}

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

# AdminIds
AdminIds = {492569185, 384341109, 551709213}
BannedIds = {}

# Ver
Ver = "3.4.0a2_5"

# Flags
Flags = {
    'isDisabled': False
}

# Timings
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
Started = datetime.now()

# Counters
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

# Limits
Limits = {
    'XiGet': {'Request': 3000, 'Answer': 4095},
    'XyiGet': {'Request': 3000, 'Answer': 4095},
    'CrazyGet': {'Request': 4000, 'Answer': 4095},
    'LeetGet': {'Request': 4000, 'Answer': 4095},
    'PasteGet': {'Request': 0, 'Answer': 4095},
    'PingGet': {'Request': 0, 'Answer': 4095}
}

# Global vars
message = dict()


# Vk Funcs


def isUser(id_or_message_tmp) -> bool:
    if type(id_or_message_tmp) != int:
        return 'from_id' in id_or_message_tmp.keys() and id_or_message_tmp['from_id'] >= 0
    return id_or_message_tmp >= 0


def isReplyExist(message_tmp) -> bool:
    return 'reply_message' in message_tmp.keys()


def isTextExist(message_tmp) -> bool:
    return 'text' in message_tmp.keys() and len(message_tmp['text'])


def howManyForwards(message_tmp) -> int:
    if 'fwd_messages' in message_tmp.keys():
        return len(message_tmp['fwd_messages'])
    return 0


def howManyAttachments(message_tmp) -> int:
    if 'attachments' in message_tmp.keys():
        return len(message_tmp['attachments'])
    return 0


def returnAttachmentIds(message_tmp) -> dict:
    attachments = dict()
    for data in message_tmp['attachments']:
        if data['type'] in attachments:
            attachments[data['type']].add(data['type'] + str(data[data['type']]['owner_id']) + '_' +
                                          str(data[data['type']]['id']))
        else:
            attachments[data['type']] = {data['type'] + str(data[data['type']]['owner_id']) + '_' +
                                         str(data[data['type']]['id'])}
    return attachments


def returnVkName(id_or_message_tmp) -> str:
    if type(id_or_message_tmp) == dict:
        if 'from_id' in id_or_message_tmp.keys():
            return vk_ses.method(method='users.get', values={'user_ids': id_or_message_tmp['from_id']})[0][
                       'first_name'] + ' ' + \
                   vk_ses.method(method='users.get', values={'user_ids': id_or_message_tmp['from_id']})[0]['last_name']
    return vk_ses.method(method='users.get', values={'user_ids': id_or_message_tmp})[0]['first_name'] + ' ' + \
           vk_ses.method(method='users.get', values={'user_ids': id_or_message_tmp})[0]['last_name']


def returnVkGroupName(id_or_message_tmp) -> str:
    if type(id_or_message_tmp) == dict:
        if 'from_id' in id_or_message_tmp.keys():
            return vk_ses.method(method='groups.getById', values={'group_id': id_or_message_tmp['from_id']})[0]['name']
    return vk_ses.method(method='groups.getById', values={'group_ids':  id_or_message_tmp})[0]['name']


def returnConfMembers() -> dict:
    return vk_ses.method(method='messages.getConversationMembers', values={'peer_id': message['peer_id']})


def sendMessage(text_tmp, attachment_tmp=''):
    if len(attachment_tmp):
        vk_ses.method(method='messages.send',
                      values={'peer_id': message['peer_id'], 'message': text_tmp, 'attachment': attachment_tmp,
                              'random_id': 0})
    else:
        vk_ses.method(method='messages.send',
                      values={'peer_id': message['peer_id'], 'message': text_tmp, 'random_id': 0})


# Bot Funcs

def checkTimings(request_type) -> bool:
    Delay = datetime.now() - Timings[request_type]['Request'] > Timings[request_type]['Delay']
    isAdmin = message['from_id'] in AdminIds
    if Delay or isAdmin:
        Timings[request_type]['Request'] = datetime.now()
        return True
    if random.choice([True, False, False]):
        sendMessage(random.choice(BotMessages['delay_message']))
    return False


def appendPaste(text_tmp) -> bool:
    text_tmp = text_tmp.replace('\n', ' ')
    text_tmp = text_tmp.replace('\t', ' ')
    text_tmp = text_tmp.replace('  ', ' ')
    if text_tmp not in paste:
        paste.append(text_tmp)
        with open('Data/paste.txt', 'a', encoding='utf-8') as __f:
            __f.write('\n' + text_tmp)
        return True
    return False


def getPasteText() -> list:
    tmp = [random.choice(paste)]
    while len(tmp[-1]) > Limits['PasteGet']['Answer']:
        tmp.append(tmp[-1][Limits['PasteGet']['Answer']:])
        tmp[-2] = tmp[-2][:Limits['PasteGet']['Answer']]
    return tmp


def getPingText() -> list:
    members = returnConfMembers()['items']
    letterID = 0
    text = ''
    for member in members:
        if not isUser(member['member_id']):
            continue
        if letterID < len(BotMessages['ping_message'][1]):
            letter = BotMessages['ping_message'][1][letterID]
        else:
            letter = '_'
        text += '[id' + str(member['member_id']) + '|' + letter + ']'
        letterID += 1
    if letterID < len(BotMessages['ping_message'][1]):
        text += BotMessages['ping_message'][1][letterID:]
    text = [text]
    while len(text[-1]) > Limits['PingGet']['Answer']:
        text.append(text[-1][Limits['PingGet']['Answer']:])
        text[-2] = text[-2][:Limits['PingGet']['Answer']]
    return text


def getXiText(text_tmp, tver=3) -> str:
    if len(text_tmp) > Limits['XiGet']['Request']:
        text_tmp = text_tmp[:Limits['XiGet']['Request'] + 1]
    text_tmp = Translators[tver].translate(text_tmp, dest='zh-tw').text
    text_tmp = Translators[tver].translate(text_tmp, dest='en').text
    text_tmp = Translators[tver].translate(text_tmp, dest='zh-tw').text
    text_tmp = Translators[tver].translate(text_tmp, dest='ru').text
    if len(text_tmp) > Limits['XiGet']['Answer']:
        text_tmp = text_tmp[:Limits['XiGet']['Answer'] + 1]
    return text_tmp


def getXyiText(text_tmp) -> str:
    if len(text_tmp) > Limits['XyiGet']['Request']:
        text_tmp = text_tmp[:Limits['XyiGet']['Request'] + 1]
    dic = {'а': 'хуя', 'е': 'хуе', 'ё': 'хуё',
           'и': 'хуи', 'о': 'хуё', 'у': 'хую',
           'э': 'хуе', 'ю': 'хую', 'я': 'хуя', 'ы': 'хуи',
           'a': 'huya', 'e': 'huye', 'i': 'huyi', 'o': 'huyo',
           'u': 'huyu'}
    text_tmp = [k.split(' ') for k in text_tmp.split('\n')]
    for k in text_tmp:
        for _i in range(len(k)):
            for j in range(len(k[_i])):
                if k[_i][j].lower() in dic.keys():
                    upperflag = k[_i][0].isupper()
                    residualtext = ''
                    if j + 1 < len(k[_i]):
                        residualtext = k[_i][j + 1:]
                    k[_i] = dic[k[_i][j].lower()] + residualtext
                    if upperflag:
                        k[_i] = k[_i].capitalize()
                    break
    text_tmp = '\n'.join([' '.join(k) for k in text_tmp])
    if len(text_tmp) > Limits['XyiGet']['Answer']:
        text_tmp = text_tmp[:Limits['XyiGet']['Answer'] + 1]
    return text_tmp


def getLeetText(text_tmp) -> str:
    if len(text_tmp) > Limits['LeetGet']['Request']:
        text_tmp = text_tmp[:Limits['LeetGet']['Request'] + 1]
    from leet import dic
    text_tmp = text_tmp.lower()
    text_tmp = list(text_tmp)
    for k in range(len(text_tmp)):
        if text_tmp[k] in dic:
            text_tmp[k] = random.choice(list(dic[text_tmp[k]]))
    text_tmp = ' '.join(text_tmp)
    if len(text_tmp) > Limits['LeetGet']['Answer']:
        text_tmp = text_tmp[:Limits['LeetGet']['Answer'] + 1]
    return text_tmp


def getCrazyText(text_tmp) -> str:
    if len(text_tmp) > Limits['CrazyGet']['Request']:
        text_tmp = text_tmp[:Limits['CrazyGet']['Request'] + 1]
    UpLetter = True
    text_tmp = text_tmp.lower()
    text_tmp = list(text_tmp)
    for k in range(len(text_tmp)):
        if text_tmp[k].isalpha():
            if UpLetter:
                text_tmp[k] = text_tmp[k].upper()
                UpLetter = False
            else:
                UpLetter = True
    text_tmp = ''.join(text_tmp)
    if len(text_tmp) > Limits['CrazyGet']['Answer']:
        text_tmp = text_tmp[:Limits['CrazyGet']['Answer'] + 1]
    return text_tmp


while True:
    try:
        for event in vk_lp.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                message = event.message

                if not isTextExist(message):
                    continue
                if Flags['isDisabled'] and not (message['from_id'] in AdminIds):
                    continue

                # Split by ' ' for parsing requests
                preparsed = message['text'].split(' ')

                if preparsed[0].lower() not in Tags['Bot']:
                    continue
                Counters['Global'] += 1
                if not checkTimings('Global'):
                    continue
                if len(preparsed) == 1:
                    if random.choice([True, False, False, False]):
                        sendMessage(random.choice(list(BotMessages['global_message'])))
                    continue

                # Computing Functions

                # XiGet
                if preparsed[1].lower() in Tags['XiGet'] and checkTimings('XiGet'):
                    Counters['XiGet'] += 1
                    print('XiGet')
                    # check googletrans ver
                    ver = 3
                    if len(preparsed) > 2 and preparsed[2] in {'3', '4'}:
                        ver = int(preparsed[2])
                        preparsed.remove(preparsed[2])

                    if len(preparsed) > 2:
                        preparsed = ' '.join(preparsed[2:])
                        sendMessage(getXiText(preparsed, ver))
                    elif isReplyExist(message) and isTextExist(message['reply_message']):
                        preparsed = message['reply_message']['text']
                        sendMessage(getXiText(preparsed, ver))
                    else:
                        sendMessage(random.choice(BotMessages['user_error_message']))
                    continue

                # XyiGet
                if preparsed[1].lower() in Tags['XyiGet'] and checkTimings('XyiGet'):
                    Counters['XyiGet'] += 1
                    print('XyiGet')
                    if len(preparsed) > 2:
                        preparsed = ' '.join(preparsed[2:])
                        sendMessage(getXyiText(preparsed))
                    elif isReplyExist(message) and isTextExist(message['reply_message']):
                        preparsed = message['reply_message']['text']
                        sendMessage(getXyiText(preparsed))
                    else:
                        sendMessage(random.choice(BotMessages['user_error_message']))
                    continue

                # CrazyGet
                if preparsed[1].lower() in Tags['CrazyGet'] and checkTimings('CrazyGet'):
                    Counters['CrazyGet'] += 1
                    print('CrazyGet')
                    if len(preparsed) > 2:
                        preparsed = ' '.join(preparsed[2:])
                        sendMessage(getCrazyText(preparsed))
                    elif isReplyExist(message) and isTextExist(message['reply_message']):
                        preparsed = message['reply_message']['text']
                        sendMessage(getCrazyText(preparsed))
                    else:
                        sendMessage(random.choice(BotMessages['user_error_message']))
                    continue

                # LeetGet
                if preparsed[1].lower() in Tags['LeetGet'] and checkTimings('LeetGet'):
                    Counters['LeetGet'] += 1
                    print('LeetGet')
                    if len(preparsed) > 2:
                        preparsed = ' '.join(preparsed[2:])
                        sendMessage(getLeetText(preparsed))
                    elif isReplyExist(message) and isTextExist(message['reply_message']):
                        preparsed = message['reply_message']['text']
                        sendMessage(getLeetText(preparsed))
                    else:
                        sendMessage(random.choice(BotMessages['user_error_message']))
                    continue

                # PasteGet
                if preparsed[1].lower() in Tags['PasteGet'] and checkTimings('PasteGet'):
                    Counters['PasteGet'] += 1
                    print('PasteGet')
                    for i in getPasteText():
                        sendMessage(i)
                    continue

                # PasteAdd
                if preparsed[1].lower() in Tags['PasteAdd'] and message['from_id'] in AdminIds:
                    Counters['PasteAdd'] += 1
                    print('PasteAdd')
                    if len(preparsed) > 2:
                        preparsed = ' '.join(preparsed[2:])
                    elif isReplyExist(message) and isTextExist(message['reply_message']):
                        preparsed = message['reply_message']['text']
                    else:
                        sendMessage(random.choice(BotMessages['user_error_message']))
                        continue
                    if appendPaste(preparsed):
                        sendMessage(random.choice(BotMessages['success_message']))
                    else:
                        sendMessage(random.choice(BotMessages['user_error_message']))
                    continue

                # PingGet
                if preparsed[1].lower() in Tags['PingGet'] and checkTimings('PingGet'):
                    Counters['PingGet'] += 1
                    print('PingGet')
                    sendMessage(BotMessages['ping_message'][0])
                    for i in getPingText():
                        sendMessage(i)
                    continue

                # HelpGet
                if preparsed[1].lower() in Tags['HelpGet'] and checkTimings('HelpGet'):
                    Counters['HelpGet'] += 1
                    print('HelpGet')
                    sendMessage(BotMessages['help_message'].format(Ver))
                    continue

                # DebugGet
                if preparsed[1].lower() in Tags['DebugGet'] and message['from_id'] in AdminIds:
                    print('DebugGet')
                    sendMessage(BotMessages['debug_message'].format(
                        Ver, Started.strftime('%d.%m.%Y в %H:%M:%S'), (datetime.now() - Started).seconds, len(paste),
                        str(Counters['Global']), str(Counters['XiGet']), str(Counters['CrazyGet']),
                        str(Counters['PasteGet']), str(Counters['XyiGet']), str(Counters['PasteAdd']),
                        str(Counters['PingGet']), str(Counters['HelpGet']), str(Counters['LeetGet']),
                        str(int(not (datetime.now() - Timings['Global']['Request'] > Timings['Global']['Delay']))),
                        str(int(not (datetime.now() - Timings['XiGet']['Request'] > Timings['XiGet']['Delay']))),
                        str(int(not (datetime.now() - Timings['CrazyGet']['Request'] > Timings['CrazyGet']['Delay']))),
                        str(int(not (datetime.now() - Timings['PasteGet']['Request'] > Timings['PasteGet']['Delay']))),
                        str(int(not (datetime.now() - Timings['XyiGet']['Request'] > Timings['XyiGet']['Delay']))),
                        str(int(not (datetime.now() - Timings['PingGet']['Request'] > Timings['PingGet']['Delay']))),
                        str(int(not (datetime.now() - Timings['HelpGet']['Request'] > Timings['HelpGet']['Delay']))),
                        str(int(not (datetime.now() - Timings['LeetGet']['Request'] > Timings['LeetGet']['Delay']))),
                        str(Counters['ExceptionFalls']), str(len(AdminIds)), str(int(Flags['isDisabled']))))
                    continue

                # InfoGet
                if preparsed[1].lower() in Tags['InfoGet'] and message['from_id'] in AdminIds:
                    print('InfoGet')
                    username_tmp = '-'
                    id_tmp = message['from_id']
                    type_tmp = isUser(message['from_id'])
                    if type_tmp:
                        username_tmp = returnVkName(id_tmp)
                    if isReplyExist(message):
                        id_tmp = message['reply_message']['from_id']
                        username_tmp = '-'
                        type_tmp = isUser(id_tmp)
                        if type_tmp:
                            username_tmp = returnVkName(id_tmp)
                        else:
                            username_tmp = returnVkGroupName(id_tmp)
                    sendMessage(BotMessages['info_message'].format(['Group', 'User'][type_tmp], username_tmp,
                                                                   str(id_tmp), str(int(id_tmp in AdminIds))))
                    continue

                # EnableSet
                if preparsed[1].lower() in Tags['EnableSet'] and message['from_id'] in AdminIds:
                    print('EnableSet')
                    Flags['isDisabled'] = False
                    sendMessage(random.choice(BotMessages['success_message']))
                    continue

                # DisableSet
                if preparsed[1].lower() in Tags['DisableSet'] and message['from_id'] in AdminIds:
                    print('DisableSet')
                    Flags['isDisabled'] = True
                    sendMessage(random.choice(BotMessages['success_message']))
                    continue

                # RestartGet
                if preparsed[1].lower() in Tags['RestartGet'] and message['from_id'] in AdminIds:
                    print('RestartGet')
                    sendMessage(random.choice(BotMessages['success_message']))
                    raise Exception("Restart")

    except Exception:
        if str(sys.exc_info()[1]) == 'Restart':
            print('Hard Restarting...', datetime.now())
            raise Exception('Restart')
        Counters['ExceptionFalls'] += 1
        print('Exception, restarting.',  str(datetime.now().strftime('%d.%m.%Y-%H:%M:%S')), sys.exc_info(), sep='\n')
