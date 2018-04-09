import requests
import time as t
import csv
import datetime as dt
from datetime import datetime, date, time, timedelta

token = '' #вставить свой токен


def get_wall(owner_id, token):
    print('Время запуска', datetime.strftime(datetime.now(), "%H:%M:%S"))

    post_data = []  # пустой список

    # отправка запроса к хранимой процедуре, которая делает запрос на первые 2500 постов
    r = requests.post(
        'https://api.vk.com/method/execute.Vk_wallGet?owner_id=' + str(owner_id) + '&post_count=' + str(
            2500) + '&offset=' + str(0) + '&access_token=' + token).json()

    response = r['response']

    # добавляем в список данные о первых 2500 постах
    post_data.extend(response[1])
    print('Количество собранных постов:', len(post_data))
    post_count = response[0]  # количество постов на стене

    # если количество постов на стене больше чем 2500, то запускается цикл, который будет работать до тех пор, пока не соберёт все данные

    if post_count > 2500:
        print('Количество постов в сообществе больше 2500.')
        for offset in range(2500, post_count, 2500):
            max_count = offset + 2500

            r = requests.post('https://api.vk.com/method/execute.Vk_wallGet?owner_id='
                              + str(owner_id) + '&post_count=' + str(max_count)
                              + '&offset=' + str(offset) + '&access_token=' + token).json()

            response = r['response']

            post_count = response[0]

            post_data.extend(response[1])

            print('Количество собранных постов:', len(post_data))
            t.sleep(
                0.35)  # можно вместо ожидания попробовать потом писать в csv,чтобы не тратить .35 на простое ожидание

    else:
        print('Количество постов в сообществе меньше 2500.\nЗакончен сбор данных. \nИтого собрано постов:',
              len(post_data))

    # записываем все данные в csv

    # открываем csv и пишем название столбцов
    with open('post_data' + str(owner_id) + '.csv', 'w', newline='') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(['date'] + ['time'] + ['owner_id'] + ['post_id'] +
                            ['len_text'] + ['likes_count'] + ['repost_count'] + ['comments_count'])

    print('Данные записаны')

    for i in range(0, len(post_data)):
        # здесь нет никакой информации о медиаобъектах

        post_date = dt.datetime.fromtimestamp(  # функция преобразования
            int(post_data[i]['date'])
        ).strftime('%Y-%m-%d')  # фортма преобразования Год-Месяц Час-Минута-Секунда

        post_time = dt.datetime.fromtimestamp(  # функция преобразования
            int(post_data[i]['date'])
        ).strftime('%H:%M:%S')  # фортма преобразования Год-Месяц Час-Минута-Секунда

        comments_count = post_data[i]['comments']['count']  # количество комментариев
        post_id = post_data[i]['id']  # id поста в сообществе

        likes_count = post_data[i]['likes']['count']  # количество лайков

        repost_count = post_data[i]['reposts']['count']  # количество репостов

        len_text = len(post_data[i]['text'])  # длина текста

        with open('post_data' + str(owner_id) + '.csv', 'a', newline='') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            datawriter.writerow([post_date] + [post_time] + [owner_id] + [post_id] +
                                [len_text] + [likes_count] + [repost_count] + [comments_count])

    print('Закончена запись в csv.')
    print('Данные собраны в', datetime.strftime(datetime.now(), "%H:%M:%S"))

#Анализ данных

import pandas as pd


df = pd.read_csv('post_data'+str(owner_id)+'.csv', parse_dates=True, delimiter=';', index_col='date')

df.head()

#сводные данные по длине текста постов, числу лайков, репостов, комментов

df['len_text'].describe()

df['likes_count'].describe()

df['likes_count'][0:100].describe()

df['repost_count'][0:100].describe()

df['comments_count'][0:100].describe()

post_time = pd.to_datetime(df.time) # сообщаем панде, что у нас там даты-время

#визуализируем все, строим графики, линии, плотики

%matplotlib inline

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#для лайков

like = df['likes_count']

plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика

plt.title('Like count by date')
plt.xlabel('date') #подпись оси x
plt.ylabel('count likes') #подпись оси y
plt.grid()
plt.plot(like,'.') #что рисуем и в какой форме: точка и др.

like_n = df[df['likes_count'] < 2000 ]['likes_count'][0:800] # 350 - это граница отсечения

%matplotlib inline

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

like = df['likes_count']

plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика

plt.title('Like count by date')
plt.xlabel('date') #подпись оси x
plt.ylabel('count likes') #подпись оси y
plt.grid()
plt.plot(like_n,'.') #что рисуем и в какой форме: точка и др.

# для репостов
%matplotlib inline

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

repost = df['repost_count']

plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика

plt.title('Repost count by date')
plt.xlabel('date') #подпись оси x
plt.ylabel('repost count') #подпись оси y
plt.grid()
plt.plot(repost,'.') #что рисуем и в какой форме: точка и др.

repost_n = df[df['repost_count'] < 400 ]['repost_count'] # 100 - это граница отсечения, выбрасываем выбросы хихи

%matplotlib inline

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

repost = df['repost_count']

plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика

plt.title('Repost count by date')
plt.xlabel('date') #подпись оси x
plt.ylabel('repost count') #подпись оси y
plt.grid()
plt.plot(repost_n,'.') #что рисуем и в какой форме: точка и др.

#для комментов

%matplotlib inline

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

comment = df['comments_count']

plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика

plt.title('Comments count by date')
plt.xlabel('date') #подпись оси x
plt.ylabel('comment count') #подпись оси y
plt.grid()
plt.plot(comment,'.') #что рисуем и в какой форме: точка и др.

comment_n = df[df['comments_count'] < 500 ]['comments_count'] # 80 - это граница отсечения, выбрасываем выбросы

%matplotlib inline

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

comment = df['comments_count']

plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика
plt.title('Comments count by date')
plt.xlabel('date') #подпись оси x
plt.ylabel('comment count') #подпись оси y
plt.grid()
plt.plot(comment_n,'.') #что рисуем и в какой форме: точка и др.

#анализируем виральность, отношение лайков и шеров

virus = like/repost

%matplotlib inline

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

comment = df['comments_count']

plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика

plt.title('Like / repost')
plt.xlabel('date') #подпись оси x
plt.ylabel('like/repost') #подпись оси y
plt.grid()
plt.plot(virus,'.') #что рисуем и в какой форме: точка и др.

virus_n = virus[virus < 50]


%matplotlib inline

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика

plt.title('Like / repost')
plt.xlabel('date') #подпись оси x
plt.ylabel('like/repost') #подпись оси y
plt.grid()
plt.plot(virus_n,'.') #что рисуем и в какой форме: точка и др.

%matplotlib inline

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика

plt.title('Like / repost')
plt.xlabel('date') #подпись оси x
plt.ylabel('like/repost') #подпись оси y
plt.grid()
plt.plot(virus_n,'-') #что рисуем и в какой форме: точка и др.

#анализируем время публикации

post_time = pd.to_datetime(df.time) # сообщаем панде, что у нас там даты-время
plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика
plt.plot(post_time, '.')

post_time_n = post_time[post_time > '07:30:00']

post_time = pd.to_datetime(df.time) # сообщаем панде, что у нас там даты-время
plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика
plt.plot(post_time_n, '.')


post_time_n = post_time[post_time < '07:30:00']


post_time = pd.to_datetime(df.time) # сообщаем панде, что у нас там даты-время
plt.figure(num=1, figsize=(17, 6)) #размер отрисованного графика
plt.plot(post_time_n, '.')



