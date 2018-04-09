import requests
import time as t
import csv
import datetime as dt
from datetime import datetime, date, time, timedelta

token = 'вставить токен'

def get_post_activity(owner_id,post_id):
    print ('Начало работы в:',datetime.strftime(datetime.now(), "%H:%M:%S"))
    r = requests.post('https://api.vk.com/method/execute.Vk_get_object_activity?owner_id='+str(owner_id)+
                      '&post_id='+str(post_id)+'&type=post&access_token='+token).json()['response']

    user_id_like = []
    for i in r[0]:
        user_id_like.append(i['id'])

    user_id_comments = []
    for i in r[1]:
        user_id_comments.append(i['from_id'])
    print ('Работа завершена:',datetime.strftime(datetime.now(), "%H:%M:%S"))
    return user_id_like,user_id_comments


owner_id = -"id1" #id сообщества с минусом
post_id = "id2" #id поста
%time user_id_like, user_id_comments = get_post_activity(owner_id,post_id)

#лайки\репосты

a = open('post'+str(owner_id)+'-'+str(post_id)+'.txt', 'a')
for i in user_id_like:
    a.write(str(i)+'\n') #писать мож
a.close()
print ('Данные готовы')

#комментарии

a = open('post'+str(owner_id)+'-'+str(post_id)+'.txt', 'a')
for i in user_id_comments:
    a.write(str(i)+'\n') #писать мож
a.close()
print ('Данные готовы')

#лайки + репосты

a = open('post'+str(owner_id)+'-'+str(post_id)+'.txt', 'w')
for i in user_id_like:
    a.write(str(i)+'\n') #писать мож
for i in user_id_comments:
    a.write(str(i)+'\n') #писать мож
a.close()
print ('Данные готовы')

def():
    for i in range(1,30000000):
        a.write(str(i)+'\n') #писать мож
