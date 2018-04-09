import requests
import time as t
import csv
from datetime import datetime, date, time, timedelta
import random

def write_txt(members_list):
    a = open('members_club_list'+str(random.randint(0, 999999))+'.txt', 'a') #добавлено случайное число, чтобы выгрузки не совпадали
    for i in members_list:
        a.write(str(i)+'\n') #писать мож
    a.close()

    def get_members_list_id(owner_id):
        members_list = []  # изначально пустой список участников

        # первый запрос на 25000, чтобы получить первые 25000 и количество участников группы
        r = requests.post('https://api.vk.com/method/execute.Vk_members?group_id=' +
                          str(owner_id) + '&offset=' + str(0) + '&count=' + str(
            25000) + '&access_token=' + token).json()['response']
        members_count = r[0]  # количество участников

        print('В сообществе', owner_id, 'участников :', members_count)

        members_list.extend(r[1])  # вносим первые 25000 ID

        if members_count > 25000:
            print('В сообществе', owner_id, 'больше 25000 участников')
            for offset in range(25000, members_count, 25000):
                count = offset + 25000

                r = requests.post('https://api.vk.com/method/execute.Vk_members?group_id=' +
                                  str(owner_id) + '&offset=' + str(offset) + '&count=' + str(
                    count) + '&access_token=' + token).json()['response']

                members_list.extend(r[1])  # вносим все последующие ID пачками по 25000 ID


                # t.sleep(.35) #задержки между запросом --- ВАЖНО: если будут возникать проблемы - расскоментировать
            print('закончили сбор ID для', owner_id)
        else:
            print('В сообществе меньше 25000 участников. закончили сбор ID для', owner_id)

        return members_list


def get_list_club_id(list_club):
    print('Начало работы:', datetime.strftime(datetime.now(), "%H:%M:%S"))
    b = []
    for i in list_club:
        b.extend(get_members_list_id(i))

    write_txt(b)  # записываем сразу все ID из сообществ, указанных в списке
    print('Данные успешно записаны')
    print('Работы выполнена в', datetime.strftime(datetime.now(), "%H:%M:%S"))

    list_club = ["publ.id 1", "publ.id 2"]  # список id сообществ, из которых нужно собрать участников
    % time
    get_list_club_id(list_club)

    