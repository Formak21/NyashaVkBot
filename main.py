import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from datetime import *
import random
import googletrans3
import googletrans4
import sys

# Service
Trnslt = {3: googletrans3.Translator(), 4: googletrans4.Translator()}
ID = "204008487"
API = "API_KEY"
vk_ses = vk_api.VkApi(token=API)
vk_lp = VkBotLongPoll(vk_ses, ID)

Ver = "3.3.3a0"
AdminIds = {492569185, 384341109}

# Flags
Flags = {
    'isDisabled': False
}

# Tags
Tags = {
    'BOT_NAME': {'Няша', 'Няшенька', 'Няшуля', 'няша', 'няшенька', 'няшуля', 'Nyasha', 'nyasha',
                 'nyashulya', 'Nyashulya', 'Nyashenka', 'nyashenka'},
    'Xi': {'Xi', 'xi', 'хи', 'Хи', 'Си', 'си'},
    'PasteGet': {'хуй', 'Хуй', 'Xyi', 'xyi', 'хой', 'Хой', 'huy', 'Huy'},
    'Xyi': {'Хуефик', 'хуефик', 'Хуефиц', 'хуефиц', 'Хуефицировать', 'хуефицировать',
            'Хуефикатор', 'хуефикатор', 'Хуефицируй', 'хуефицируй', 'Xiyefic', 'xiyefic',
            'Xiyefits', 'xiyefits', 'Xiyefik', 'xiyefik', 'Xiyeficator', 'xiyeficator',
            'Xiyefikator', 'xiyefikator', 'Xiyefitsiruy', 'xiyefitsiruy', 'Xiyefitsirovat', 'xiyefitsitovat',
            'Huyefic', 'huyefic', 'Huyefits', 'huyefits', 'Huyefik', 'huyefik', 'Huyeficator', 'huyeficator',
            'Huyefikator', 'huyefikator', 'Huyefitsiruy', 'huyefitsiruy', 'Huyefitsirovat', 'huyefitsitovat',
            'Хфц', 'хфц', 'Hfc', 'hfc', 'Xfc', 'xfc', 'Hfts', 'hfts', 'Xfts', 'xfts', 'Хфк', 'хфк'},
    'PasteAdd': {'Добавь', 'добавь', 'add', 'Add'},
    'PingGet': {'Маяк', 'маяк', 'Пинг', 'пинг', 'Алл', 'алл', 'Олл', 'олл', 'пидорасы', 'Пидорасы',
                'Mayak', 'mayak', 'Ping', 'ping', 'All', 'all', 'Pidorasi', 'pidorasi'},
    'HelpGet': {'Help', 'help', 'Хелп', 'хелп', 'Помощь', 'помощь', 'Хэлп', 'хэлп'},
    'Debug': {'Debug', 'debug', 'Дебаг', 'дебаг', 'Дэбаг', 'дэбаг'},
    'Enable': {'En', 'en', 'Эн', 'Ен', 'ен', 'эн', 'вкл', 'Вкл', 'Enable', 'enable', 'Включить', 'включить'},
    'Disable': {'Dis', 'dis', 'Диз', 'диз', 'выкл', 'Выкл', 'Disable', 'disable', 'Выключить', 'выключить'},
    'Restart': {'restart', 'Restart', 'Рестарт', 'рестарт'}
}

# Messages
BotMessages = {
    'user_error': ['Ты еблан.', 'Ты утюг ебаный.', 'Ты тупой.', 'Ты мудак.', 'Ты долбаеб.', 'Ты еблоид.', 'Отстань.',
                   'Отъебись.', 'Исчезни, уеба.', 'Ты туп как депутат.'],
    'ping_messages': ['Pinging @all [127.0.0.1] with 32 bytes of data:', ''],
    'delay': ['Подожди ты уеба...', 'Кулдаун блять, уебище.', 'Не так быстро, мудень.', 'Жди бля, уебок.',
              'Хули ты такой быстрый? Как вода блять в унитазе.'],
    'help_message': '',
    'debug_message': '',
    'success': ['Выполнено.', 'Готово.', 'Сделано.', 'Успех.', 'Обработала.', 'Всё сделала.']
}

# Long Messages
with open('Data/paste.txt', 'r', encoding='utf-8') as _f:
    paste = _f.read().split('\n')
with open('Data/alf.txt', 'r', encoding='utf-8') as _f:
    BotMessages['ping_messages'][1] = _f.read()
with open('Data/help.txt', 'r', encoding='utf-8') as _f:
    BotMessages['help_message'] = _f.read()
with open('Data/debug.txt', 'r', encoding='utf-8') as _f:
    BotMessages['debug_message'] = _f.read()

# Timings
Timings = {
    'Global': {'Request': datetime.now(), 'Delay': timedelta(seconds=1)},
    'PasteGet': {'Request': datetime.now(), 'Delay': timedelta(seconds=5)},
    'Xi': {'Request': datetime.now(), 'Delay': timedelta(seconds=5)},
    'Xyi': {'Request': datetime.now(), 'Delay': timedelta(seconds=5)},
    'PingGet': {'Request': datetime.now(), 'Delay': timedelta(minutes=5)},
    'HelpGet': {'Request': datetime.now(), 'Delay': timedelta(seconds=10)}
}
Started = datetime.now()

# Counter
Counter = {
    'Global': 0,
    'PasteGet': 0,
    'PingGet': 0,
    'HelpGet': 0,
    'Xi': 0,
    'Xyi': 0,
    'ExceptionFalls': 0
}

# Global vars
message = dict()


def isUser(id_or_message_tmp) -> bool:
    if type(id_or_message_tmp) == dict:
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
    for i in message_tmp['attachments']:
        if i['type'] in attachments:
            attachments[i['type']].add(i['type'] + str(i[i['type']]['owner_id']) + '_' + str(i[i['type']]['id']))
        else:
            attachments[i['type']] = {i['type'] + str(i[i['type']]['owner_id']) + '_' + str(i[i['type']]['id'])}
    return attachments


def returnVkName(id_or_message_tmp) -> str:
    if type(id_or_message_tmp) == dict:
        if 'from_id' in id_or_message_tmp.keys():
            return vk_ses.method(method='users.get', values={'user_ids': id_or_message_tmp['from_id']})[0][
                       'first_name'] + ' ' + \
                   vk_ses.method(method='users.get', values={'user_ids': id_or_message_tmp['from_id']})[0]['last_name']
    return vk_ses.method(method='users.get', values={'user_ids': id_or_message_tmp})[0]['first_name'] + ' ' + \
           vk_ses.method(method='users.get', values={'user_ids': id_or_message_tmp})[0]['last_name']


def returnConfMembers() -> dict:
    return vk_ses.method(method='messages.getConversationMembers', values={'peer_id': message['peer_id']})


def returnChatId(chat_id_or_message_tmp) -> int:
    if type(chat_id_or_message_tmp) == dict:
        if 'peer_id' in chat_id_or_message_tmp:
            return chat_id_or_message_tmp['peer_id'] - 2000000000
        return 1
    return chat_id_or_message_tmp - 2000000000


def callChecker(message_tmp) -> bool:
    for j in Tags['BOT_NAME']:
        if j in message_tmp['text']:
            return True
    return False


def sendMessage(text_tmp, attachment_tmp=''):
    if len(attachment_tmp):
        vk_ses.method(method='messages.send',
                      values={'peer_id': message['peer_id'], 'message': text_tmp, 'attachment': attachment_tmp,
                              'random_id': 0})
    else:
        vk_ses.method(method='messages.send',
                      values={'peer_id': message['peer_id'], 'message': text_tmp, 'random_id': 0})


def checkTimings(request_type) -> bool:
    delay = datetime.now() - Timings[request_type]['Request'] > Timings[request_type]['Delay']
    isAdmin = message['from_id'] in AdminIds
    if delay or isAdmin:
        Timings[request_type]['Request'] = datetime.now()
        return True
    if random.choice([True, False, False]):
        sendMessage(random.choice(BotMessages['delay']))
    return False


def xiTranslator(text_tmp, ver=3) -> str:
    if len(text_tmp) > 3000:
        text_tmp = text_tmp[:3001]
    # print(text_tmp)
    translated = Trnslt[ver].translate(text_tmp, dest='zh-tw').text
    # print(translated)
    translated = Trnslt[ver].translate(translated, dest='en').text
    # print(translated)
    translated = Trnslt[ver].translate(translated, dest='zh-tw').text
    # print(translated)
    return Trnslt[ver].translate(translated, dest='ru').text


def xyiTranslator(text_tmp) -> str:
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
    if len(text_tmp) > 4095:
        text_tmp = text_tmp[:4095]
    return text_tmp


def sendPaste():
    tmp = random.choice(paste)
    if len(tmp) > 4095:
        while len(tmp) > 4095:
            sendMessage(tmp[:4095])
            tmp = tmp[4095:]
    sendMessage(tmp)


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


def getPingText() -> list:
    members = returnConfMembers()['items']
    letterID = 0
    text = ''
    for member in members:
        if not isUser(member['member_id']):
            continue
        if letterID < len(BotMessages['ping_messages'][1]):
            letter = BotMessages['ping_messages'][1][letterID]
        else:
            letter = '_'
        text += '[id' + str(member['member_id']) + '|' + letter + ']'
        letterID += 1
    if letterID < len(BotMessages['ping_messages'][1]):
        text += BotMessages['ping_messages'][1][letterID:]
    text = [text]
    while len(text[-1]) > 4095:
        text.append(text[-1][4095:])
        text[-2] = text[-2][:4095]
    return text


while True:
    try:
        for event in vk_lp.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                message = event.message
                if isTextExist(message) and callChecker(message):
                    if Flags['isDisabled'] and not (message['from_id'] in AdminIds):
                        continue

                    Counter['Global'] += 1
                    if not checkTimings('Global'):
                        continue
                    preparsed = message['text'].split(' ')

                    # Xi
                    if len(preparsed) > 1 and preparsed[0] in Tags['BOT_NAME'] and preparsed[1] in Tags[
                        'Xi'] and checkTimings('Xi'):
                        # check googletrans ver
                        ver = 3
                        if len(preparsed) > 2 and preparsed[2] in {'3', '4'}:
                            ver = int(preparsed[2])
                            preparsed.remove(preparsed[2])

                        if len(preparsed) > 2:
                            preparsed = ' '.join(preparsed[2:])
                            sendMessage(xiTranslator(preparsed, ver))
                        elif isReplyExist(message):
                            preparsed = message['reply_message']['text']
                            sendMessage(xiTranslator(preparsed, ver))
                        else:
                            sendMessage(random.choice(BotMessages['user_error']))
                        Counter['Xi'] += 1
                        continue

                    # Xyi
                    if len(preparsed) > 1 and preparsed[0] in Tags['BOT_NAME'] and preparsed[1] in Tags[
                        'Xyi'] and checkTimings('Xyi'):
                        if len(preparsed) > 2:
                            preparsed = ' '.join(preparsed[2:])
                            sendMessage(xyiTranslator(preparsed))
                        elif isReplyExist(message):
                            preparsed = message['reply_message']['text']
                            sendMessage(xyiTranslator(preparsed))
                        else:
                            sendMessage(random.choice(BotMessages['user_error']))
                        Counter['Xyi'] += 1
                        continue

                    # PasteGet
                    if len(preparsed) > 1 and preparsed[0] in Tags['BOT_NAME'] and preparsed[1] in Tags[
                        'PasteGet'] and checkTimings('PasteGet'):
                        sendPaste()
                        Counter['PasteGet'] += 1
                        continue

                    # PasteAdd
                    if len(preparsed) > 1 and preparsed[0] in Tags['BOT_NAME'] and preparsed[1] in Tags['PasteAdd'] and \
                            message['from_id'] in AdminIds:
                        if len(preparsed) > 2:
                            preparsed = ' '.join(preparsed[2:])
                        elif isReplyExist(message):
                            preparsed = message['reply_message']['text']
                        else:
                            sendMessage(random.choice(BotMessages['user_error']))
                            continue
                        if appendPaste(preparsed):
                            sendMessage(random.choice(BotMessages['success']))
                        else:
                            sendMessage(random.choice(BotMessages['user_error']))
                        continue

                    # PingGet
                    if len(preparsed) > 1 and preparsed[0] in Tags['BOT_NAME'] and preparsed[1] in Tags[
                        'PingGet'] and checkTimings('PingGet'):
                        sendMessage(BotMessages['ping_messages'][0])
                        for i in getPingText():
                            sendMessage(i)
                        Counter['PingGet'] += 1
                        continue

                    # Help
                    if len(preparsed) > 1 and preparsed[0] in Tags['BOT_NAME'] and preparsed[1] in Tags[
                        'HelpGet'] and checkTimings('HelpGet'):
                        sendMessage(BotMessages['help_message'].format(random.choice(list(Tags['BOT_NAME'])), Ver,
                                                                       random.choice(list(Tags['HelpGet'])),
                                                                       random.choice(list(Tags['Xi'])),
                                                                       random.choice(list(Tags['PasteGet'])),
                                                                       random.choice(list(Tags['Xyi'])),
                                                                       random.choice(list(Tags['PasteAdd'])),
                                                                       random.choice(list(Tags['PingGet'])),
                                                                       random.choice(list(Tags['Debug'])),
                                                                       random.choice(list(Tags['Enable'])),
                                                                       random.choice(list(Tags['Disable'])),
                                                                       random.choice(list(Tags['Restart']))))
                        Counter['HelpGet'] += 1
                        continue

                    # Debug
                    if len(preparsed) > 1 and preparsed[0] in Tags['BOT_NAME'] and preparsed[1] in Tags['Debug'] and \
                            message[
                                'from_id'] in AdminIds:
                        sendMessage(BotMessages['debug_message'].format(Ver, Started, (datetime.now()-Started).seconds,
                                                                        len(paste), Counter['Global'],
                                                                        Counter['PasteGet'], Counter['PingGet'],
                                                                        Counter['HelpGet'], Counter['Xi'],
                                                                        Counter['Xyi'], Counter['ExceptionFalls'],
                                                                        len(AdminIds), int(Flags['isDisabled'])))
                        continue

                    # Restart
                    if len(preparsed) > 1 and preparsed[0] in Tags['BOT_NAME'] and preparsed[1] in Tags['Restart'] and \
                            message['from_id'] in AdminIds:
                        sendMessage(random.choice(BotMessages['success']))
                        raise Exception("Restart")

                    # Disable
                    if len(preparsed) > 1 and preparsed[0] in Tags['BOT_NAME'] and preparsed[1] in Tags['Disable'] and \
                            message[
                                'from_id'] in AdminIds:
                        Flags['isDisabled'] = True
                        sendMessage(random.choice(BotMessages['success']))
                        continue

                    # Enable
                    if len(preparsed) > 1 and preparsed[0] in Tags['BOT_NAME'] and preparsed[1] in Tags['Enable'] and \
                            message[
                                'from_id'] in AdminIds:
                        Flags['isDisabled'] = False
                        sendMessage(random.choice(BotMessages['success']))
                        continue
    except Exception:
        if str(sys.exc_info()[1]) == 'Restart':
            print('Hard Restarting...')
            raise Exception('Restart')
        Counter['ExceptionFalls'] += 1
        print('Exception, restarting.',  sys.exc_info(), sep='\n')
