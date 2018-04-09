import requests
import time as t
import csv
from datetime import datetime, date, time, timedelta

token = 'вставить токен'

def write_txt(members_list, owner_id):
    a = open('members_club'+str(owner_id)+'.txt', 'w')
    for i in members_list:
        a.write(str(i)+'\n') #писать мож
    a.close()


def get_members_list_id(owner_id):
    print('начал работать в:', datetime.strftime(datetime.now(), "%H:%M:%S"))

    members_list = []  # изначально пустой список участников

    # первый запрос на 25000, чтобы получить первые 25000 и количество участников группы
    r = requests.post('https://api.vk.com/method/execute.VK_members?group_id=' +
                      str(owner_id) + '&offset=' + str(0) + '&count=' + str(25000) + '&access_token=' + token).json()[
        'response']
    members_count = r[0]  # количество участников

    print('Количество участников в сообществе:', members_count)

    members_list.extend(r[1])  # вносим первые 25000 ID

    if members_count > 25000:
        print('В сообществе больше 25000 участников. запускаем цикл')
        for offset in range(25000, members_count, 25000):
            count = offset + 25000

            r = requests.post('https://api.vk.com/method/Vk_members?group_id=' +
                              str(owner_id) + '&offset=' + str(offset) + '&count=' + str(
                count) + '&access_token=' + token).json()['response']

            members_list.extend(r[1])  # вносим все последующие ID пачками по 25000 ID


            # t.sleep(.35) #задержки между запросом --- ВАЖНО: если будут возникать проблемы - расскоментировать
        print('закончил сбор ID')
    else:
        print('В сообществе меньше 25000 участников. закончил сбор ID')

    print(len(members_list))
    write_txt(members_list, owner_id)  # записываем по 25000 ID
    print('Данные успешно записаны')
    print('закончил работать в:', datetime.strftime(datetime.now(), "%H:%M:%S"))

#Подставьте в скобки ID сообщества, из которого нужно собрать ID участников

