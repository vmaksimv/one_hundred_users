from fast_bitrix24 import Bitrix
import json
# import pandas as pd

# webhook = "https://xiaolong.bitrix24.ru/rest/180/vfjliozqyo1s0krz/"     # вебхук от старого портала Б24
webhook = "https://bx24.xiaolong-group.com/rest/180/odcohdzspj99o4yb/"     # вебхук от нового портала Б24
b = Bitrix(webhook)

PARAMS = {'select': ['ID'], 'filter': {'ACTIVE': True}}
response = b.get_all('user.get', params=PARAMS)
out_response = json.dumps(response, ensure_ascii=False)
out = []
for i in json.loads(out_response):
    out.append('ID : {0}'.format(i['ID']))
out_data = []
for i in range(len(out)):
    l = out[i]
    l = l.replace('ID :', '')
    l = l.replace(' ', '')
    l = l.split(',')
    out_data.append(l)

id_list = [int(item[0]) for item in out_data]
# print(id_list)
# df_out_data = pd.DataFrame(out_data)
# df_out_data = df_out_data.rename(columns={0: 'id_user'})
# df_out_data = df_out_data['id_user'].astype('int')


for i in id_list:
    id_user = i

    # webhook = "https://xiaolong.bitrix24.ru/rest/180/pv9a7p55w1f6oo3s/"     # вэбхук для старого портала
    webhook = "https://bx24.xiaolong-group.com/rest/180/odcohdzspj99o4yb/"      # вэбхук для нового портала
    c = Bitrix(webhook)

    string = '''Изменения в работе старого облачного портала Битрикс24. Changes in the operation of the old Bitrix24 cloud portal.
                  \nС 26.06.2023 работа этого облачного портала Битрикс24 больше работать не будет;
                  \nПросьба перейти на работу в новый коробочный портал Битрикс24 по адресу https://bx24.xiaolong-group.com
                  \nИнструкция для входа в новый портал доступна по ссылке: https://docs.google.com/document/d/1nN...sp=sharing;
                  \n--------------------------------------------------------------------------------------------------------------
                  \nFrom 06/26/2023, this Bitrix24 cloud portal will no longer work.
                  \nPlease go to work in the new Bitrix24 boxed portal at https://bx24.xiaolong-group.com
                  \nInstructions for entering the new portal are available at the link: https://docs.google.com/document/d/1nN...sp=sharing;'''

    PARAMS_MSG = {'DIALOG_ID': id_user, 'MESSAGE': string}
    response_msg = c.call('im.message.add', PARAMS_MSG)

# <a href="https://www.example.com">sample</a>
