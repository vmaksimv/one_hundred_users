from fast_bitrix24 import Bitrix
import json
import pandas as pd
import datetime
import time
import requests

current_datetime = datetime.datetime.now().date()
today_datetime = str(current_datetime)

URL = 'https://isdayoff.ru/' + today_datetime       # внешний сервис, рабочий календарь на 2023 год
response = requests.get(URL)

if response.text == '0':        # если 0, то день рабочий

    '''Блок из 4х строк кода высчитывает разницу от текущего времени до 23:00, переводит эту разницу в секунды'''

    current_time = datetime.datetime.now().time()
    target_time = datetime.time(23, 0)
    time_difference = datetime.datetime.combine(datetime.date.today(), target_time) - datetime.datetime.combine(datetime.date.today(), current_time)
    delay_seconds = time_difference.total_seconds()

    sum_active_users = 0

    active_users = []
    users_list = []

    webhook = "https://xiaolong.bitrix24.ru/rest/180/vfjliozqyo1s0krz/"
    b = Bitrix(webhook)

    PARAMS = {'filter': {'ACTIVE': True}}
    response = b.get_all('user.get', params=PARAMS)     # получаю перечень работающих сотрудников
    out_response = json.dumps(response, ensure_ascii=False)

    for user in json.loads(out_response):
        active_users.append('ID : {0}, LAST_LOGIN : {1}, IS_ONLINE : {2}, UF_DEPARTMENT : {3}'.format(user['ID'], user['LAST_LOGIN'], user['IS_ONLINE'], user['UF_DEPARTMENT']))

    for i in range(len(active_users)):
        l = active_users[i]
        l = l.replace('ID :', '')
        l = l.replace('LAST_LOGIN :', '')
        l = l.replace('IS_ONLINE :', '')
        l = l.replace('UF_DEPARTMENT :', '')
        l = l.replace(' ', '')
        l = l.split(',')
        users_list.append(l)

    df_active_users = pd.DataFrame(users_list)
    df_active_users = df_active_users.rename(columns={0: 'id_user', 1: 'last_activity', 2: 'status_online', 3: 'department'})
    df_active_users = df_active_users[['id_user', 'last_activity', 'status_online', 'department']]

    df_active_users['last_activity'] = pd.to_datetime(df_active_users['last_activity'], format='%Y-%m-%dT%H:%M:%S', exact=False)
    df_active_users['last_activity'] = df_active_users['last_activity'].dt.date
    df_active_users['last_activity'] = pd.to_datetime(df_active_users['last_activity'], format='%Y-%m-%d')

    df_active_users['department'] = [item.strip('[]') for item in df_active_users['department']]
    df_active_users['department'] = df_active_users['department'].astype('int')

    df_active_users = df_active_users.query('last_activity in @today_datetime')     # активный пользователи за текущий день

    sum_active_users = len(df_active_users)     # получаю количество авторизованных пользователей в текущий день

    if sum_active_users < 100:
        print(f'Количество пользователей равно {sum_active_users}. Есть резерв.' + ' ' + today_datetime)
    else:
        webhook = "https://xiaolong.bitrix24.ru/rest/180/8rphp03jqrtw73ta/"
        c = Bitrix(webhook)

        PARAMS_MSG = {'USER_ID': 180,
                    'POST_TITLE': 'Превышен порог свободных лицензий',
                    'POST_MESSAGE': 'Внимание! Недостаточно свободных лицензий',
                    'DEST': ['SG60']}

        response_msg = c.call('log.blogpost.add', PARAMS_MSG)       # отправляю уведомление о превышении порога в 100 пользователей

        webhook_user = "https://xiaolong.bitrix24.ru/rest/180/vfjliozqyo1s0krz/"
        u = Bitrix(webhook_user)

        PARAMS_NO_ACTIVE = {'ID': [128, 130, 102, 122, 216, 116, 276, 448, 398], 'ACTIVE': 'N'}
        response_no_active = u.call('user.update', PARAMS_NO_ACTIVE)        # меняю статус уволен у группы сотрудников

        time.sleep(delay_seconds)       # задержка выполнения кода до 23:00

        webhook_user = "https://xiaolong.bitrix24.ru/rest/180/vfjliozqyo1s0krz/"
        u = Bitrix(webhook_user)

        PARAMS_NO_ACTIVE = {'ID': [128, 130, 102, 122, 216, 116, 276, 448, 398], 'ACTIVE': 'Y'}
        response_active = u.call('user.update', PARAMS_NO_ACTIVE)        # меняю статус принят на работу у группы сотрудников

        print(f'Был превышен порог в 100 пользователей. Части сотрудникам был присвоен статус Уволен' + ' ' + today_datetime)

else:
    print('Сегодня выходной' + ' ' + today_datetime)

