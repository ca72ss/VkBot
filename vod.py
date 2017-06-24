# -*- coding: utf-8 -*-

import sys
import codecs
import time
import vk
import time

def print_dic(dic):
    for keys, values in dic.items():
        print keys, '=>', values

# http://oauth.vk.com/authorize?client_id=5112190&display=page&scope=offline,messages,groups,friends&response_type=token&v=5.59
# http://oauth.vk.com/authorize?client_id=5112190&display=page&scope=notify,friends,photos,audio,video,docs,notes,pages,status,offers,questions,wall,groups,mail,messages,notifications,stats,ads,offline,nohttps&response_type=token&v=5.59



#city_name = "Лисичанск"
#city_name = "Северодонецк"
#city_name = "Рубежное"
#city_name = "Сватово"
#city_name = "Новопсков"

city_name = 'Харьков'

#school_num = "школа"
school_num = 'школа 105'

todo = 1

message = u"""Добрый день, %user_name%!
Приглашаем стать специалистом в области компьютерных и информационных технологий и получить качественное фундаментальное образование, которое востребовано за рубежом?
Тогда тебе к нам :)
приглашаем ознакомиться с нашими специальностями:
    – Информационные технологии проектирования
    – Компьютерная механика

Подробную информацию о специальностях Вы можете узнать на сайте кафедры http://web.kpi.kharkov.ua/dpm/ru/abiturientu/.
Если тебя заинтересовала эта информация:
1.   Добавляйся к нам  в группу https://vk.com/official_dpm для того чтобы своевременно получать актуальную информацию.
2.   Приходи на подкурсы в ХПИ
(http://www.kpi.kharkov.ua/ua/home/podkursi/)
 Успешное окончание покурсов гарантирует
10 ДОПОЛНИТЕЛЬНЫХ БАЛОВ
к баллам ЗНО при поступлении!!!
Возможно дистанционное обучение (http://blogs.kpi.kharkov.ua/DPK/page/page.aspx)
3.   Становись нашим студентом! """

short_text = u"%user_name%! Предлагаем стать специалистом в области компьютерных и информационных технологий? Добавляйся в друзья и вступай в группу https://vk.com/official_dpm"


session = vk.Session(access_token='123456789')
#session = vk.AuthSession(app_id='5112190',user_login='a_vodka@mail.ru', user_password='123456')
api = vk.API(session)
#print api.users.get(user_ids=1)

group_id = 80326633

UA_CID = api.database.getCountries(code='UA')[0]['cid']
CITY = api.database.getCities(country_id=UA_CID, q=city_name)
nc = 0
print_dic(CITY[nc])
print 'найдено городов =>', len(CITY)

CITY_ID = CITY[nc]['cid']

SCHOOL =  api.database.getSchools(q=school_num,city_id=CITY_ID)
print 'найдено школ =>', SCHOOL[0]
print_dic(SCHOOL[1])
SCHOOL_ID = SCHOOL[1]['id']



users = api.users.search(city=CITY_ID, country=UA_CID, age_from=14, age_to=18, school_year=2017, school = SCHOOL_ID)

i = 0

for u in users:
    if type(u) is not int:
        #print_dic(u)
        i+=1
        if i < 0:
            continue

        isSent =True
        try:
            if todo:
                #api.groups.invite(group_id=group_id, user_id=u['uid'])
		#print_dic(u)
                #api.messages.send(user_id=u['uid'], message=message.replace(u'%user_name%', u['first_name']), attachment='photo6235159_437838510')
		ud = api.users.get(user_ids=u['uid'], fields='last_seen,photo_id,has_mobile,universities,can_write_private_message,can_send_friend_request')[0]
		print_dic(ud)
		print api.photos.getById(photos=ud['photo_id'])
#		print ud['last_seen']['time']
		dt = time.time() - int(ud['last_seen']['time'])
		if dt > 30*24*3600:
			print "Nobody lives here"
			continue
		
		


		exit()

        except vk.exceptions.VkAPIError as e:
            sc = int(str(e)[0:str(e).index('.')])
            isSent = False
            if sc == 7:
                api.friends.add(user_id = u['uid'], text = short_text.replace('%user_name%', u['first_name']) )
            else:
                print e

        #    isSent = False

        print u['first_name'],'\t', u['last_name'], '\t', 'https://vk.com/id'+str(u['uid']), '\t', isSent

        time.sleep(5)