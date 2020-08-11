import time as t
import csv
import datetime as dt
from datetime import datetime, date, time, timedelta
import requests
import itertools
%matplotlib inline

token = 'вставить токен'

q = 'vinci' #без знака # только одно слово.

with open(q + '.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    datawriter.writerow(['date'] + ['owner_id'] + ['post_id'] + ['likes'] +
                        ['reposts'] + ['comments'] +

                        ['coordinates'] +
                        # не трогать, не работает.
                        # ['place_country']+['city']+['address']+['coordinates']+
                        # ['place_id']+['latitude']+['longitude']+
                        # ['created']+['updated']+['checkins']+

                        ['post_type'] +
                        ['platform'] + ['platform_type'])

i = 0
while True:

    if i == 0:
        b = datetime.now()  # текущее время

        end_time = 1475508828  # int(t.mktime(b.timetuple())) #подставить unix-время если требуется сбор с определённого момента

        print('Собираем посты с:', end_time, dt.datetime.fromtimestamp(  # функция преобразования
            int(end_time)
        ).strftime('%Y-%m-%d %H:%M:%S'))

        i = 1

    else:
        end_time = r[0]  # возвращает Vk конец периода поиска

    r = requests.post('https://api.vk.com/method/execute.Vk_search_post?q=' + str(q)
                      + '&end_time=' + str(end_time)
                      + '&access_token=' + token).json()['response']
    # print('крайнее время, должно совпадать',r[0])


    # print(len(r[1])) - сколько постов собрано за раз



    # print(time_start)

    for i in r[1]:

        date = i['date']  # дата поста

        owner_id = i['owner_id']  # создатель поста
        post_id = i['id']  # id поста

        likes = i['likes']['count']  # количество лайков
        reposts = i['reposts']['count']  # количество репостов
        comments = i['comments']['count']  # количество комментариев
        geo = i.setdefault('geo', None)

        if geo == None:
            coordinates = None
        else:
            '''
            place_id = i['geo']['place'].setdefault('id',None)
            latitude = geo['place'].setdefault('latitude',None) #широта места
            longitude = geo['place'].setdefault('longitude',None) #долгота места
            created= geo['place'].setdefault('created',None) # дата создания места
            updated= geo['place'].setdefault('updated',None) # дата обновления информации о месте
            checkins= geo['place'].setdefault('checkins',None) #количество чекинов в этом месте
            place_name = i['geo'].setdefault('title',None)
            country = i['geo'].setdefault('country',None)
            city = i['geo'].setdefault('city',None)
            address = i['geo'].setdefault('address',None)

            '''
            coordinates = geo.setdefault('coordinates', None)  # координаты пользователя

        post_type = i['post_type']

        platform = i['post_source'].setdefault('platform', 'direct')
        platform_type = i['post_source'].setdefault('type', None)
        platform_url = i['post_source'].setdefault('url', None)

        with open(str(q) + '.csv', 'a', newline='', encoding='UTF-8') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            datawriter.writerow([date] + [owner_id] + [post_id] + [likes] +
                                [reposts] + [comments] +

                                # [geo]+
                                [coordinates] +

                                # не трогать - не работает
                                # [country]+[city]+[address]+
                                # [place_id]+[latitude]+[longitude]+
                                # [created]+[updated]+[checkins]+


                                [post_type] +
                                [platform] + [platform_type])
    print('собрали посты до:', r[0], dt.datetime.fromtimestamp(  # функция преобразования
        int(r[0])
    ).strftime('%Y-%m-%d %H:%M:%S'))
    t.sleep(30)

import numpy as np
import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

df = pd.read_csv(str(q)+'.csv', delimiter=';', encoding='UTF-8',error_bad_lines=False, parse_dates=True)

df.head()

# удалим дубликаты. возможны будут если перезаписывать файл

df.drop_duplicates() #удалит дубликаты если перезаписывали файл
df['date'] = pd.to_datetime(df['date'],unit='s')

#группируем по дням


group_by_day = df.set_index('date').groupby(pd.TimeGrouper('D')).count()
group_by_day.head()

#рисуем график динамики

plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика

plt.title('Date')
plt.xlabel('date') #подпись оси x
plt.ylabel('count post per day') #подпись оси y
plt.grid()
plt.plot(group_by_day['owner_id'],label=str(q)) #что рисуем и в какой форме: точка и др.

plt.legend()

platform = df.groupby(df['platform']).count()
platform

platform_sort = platform.sort_values(['platform_type'],ascending=0)

plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика
plt.grid()
platform_sort['platform_type'].plot(kind='bar')
