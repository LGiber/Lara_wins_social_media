#получить список ID пользователей, которые состоят сразу в 3-х сообществах
# Получить токен: https://oauth.vk.com/authorize?client_id=5453402&display=page&redirect_uri=http://localhost&scope=&response_type=token&v=5.53


token = ''

#вставить в ковычки токен

import requests
import time as t
import csv
from datetime import datetime, date, time, timedelta
import random


def get_members_list_id(owner_id):
    members_list = []  # изначально пустой список участников

    # первый запрос на 25000, чтобы получить первые 25000 и количество участников группы
    r = requests.post('https://api.vk.com/method/execute.Vk_getClub_members?group_id=' +
                      str(owner_id) + '&offset=' + str(0) + '&count=' + str(25000) + '&access_token=' + token).json()[
        'response']
    members_count = r[0]  # количество участников

    print('В сообществе', owner_id, 'участников :', members_count)

    members_list.extend(r[1])  # вносим первые 25000 ID

    if members_count > 25000:
        print('В сообществе', owner_id, 'больше 25000 участников. запускает цикл')
        for offset in range(25000, members_count, 25000):
            count = offset + 25000

            r = requests.post('https://api.vk.com/method/execute.Vk_getClub_members?group_id=' +
                              str(owner_id) + '&offset=' + str(offset) + '&count=' + str(
                count) + '&access_token=' + token).json()['response']

            members_list.extend(r[1])  # вносим все последующие ID пачками по 25000 ID


            # t.sleep(.35) #задержки между запросом --- ВАЖНО: если будут возникать проблемы - расскоментировать
        print('закончил сбор ID для')
    else:
        print('В сообществе меньше 25000 участников. закончил сбор ID для')

    return members_list

#Запускаем функцию для каждого сообщества.

#%time - для вывода времени, за которое выполняется функция

%time "name 1" = get_members_list_id("id1")
%time " name 2" = get_members_list_id("id2")
%time "name 3"= get_members_list_id("id3")

count = len("name 1" + "name 2" + "name 3")
count

uniq_3 = set("name 1") | set("name 2") | set("name 3")
len(groups_3)

groups_3 = set("name 1") & set("name 2") & set("name 3")
len(groups_3)


with open('3 группы.csv', 'w', newline='') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            datawriter.writerow(groups_3)