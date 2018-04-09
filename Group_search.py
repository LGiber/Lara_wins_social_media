import requests
import time as t
import csv
from datetime import datetime, date, time, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame

#Ссылка для получения токена: https://oauth.vk.com/authorize?client_id=5453402&display=page&redirect_uri=http://localhost&scope=&response_type=token&v=5.53

token = 'вставьте сюда токен, полученный по ссылке выше'


def search_groups():
    print('начал работу в:', datetime.strftime(datetime.now(), "%H:%M:%S"))
    q = str(input('Введите поисковый запрос:'))
    type_group = str(
        input('Введите тип сообществ. page, group, event.\nОставьте пустым, чтобы вернул все типы сообществ:'))
    sort = 0

    r = requests.post('https://api.vk.com/method/execute.VK_search_groups?q=' +
                      str(q) + '&sort=' + str(sort) + '&type=' + str(type_group) + '&access_token=' + token).json()[
        'response']

    count_groups = r[0]

    name = []
    id = []
    type = []
    screen_name = []

    # создаем пустой словарь, в который будем помещать информацию по каждой группе, для последующего импорта во frame
    data_list = {'name': name,
                 'screen_name': screen_name,
                 'id': id,
                 'type': type}

    for i in r[1]:
        name.append(i['name'])
        screen_name.append('https://vk.com/' + str(i['screen_name']))
        id.append(i['id'])
        type.append(i['type'])

    frame = DataFrame(data_list)
    print('обработал данные в:', datetime.strftime(datetime.now(), "%H:%M:%S"))
    print('Запускайте последовательно блоки ниже')
    return frame, count_groups


frame, count_groups = search_groups()
print ('Найдено сообществ:',count_groups)

frame.to_csv('example.csv') #запишет все данные в csv файл

frame.head() #покажет первые 5 сообществ

frame['screen_name'][0:10] #покажет 10 сообществ. можно регулировать. + ссылки кликабельны