from flask import render_template, flash, redirect, session
from app import app
from .forms import LoginForm
import html
import cgi
import v2
import sys
import codecs
import time
import vk
print("Content-Type: text/html")
print()

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
auth1 = v2.VKAuth()
auth1.auth()
at = auth1.get_token()

session = vk.Session(access_token=at)
api = vk.API(session)

city_name = 'Шостка'

#school_num = "школа"
school_num = 'школа 5'

UA_CID = api.database.getCountries(code='UA')[0]['cid']
CITY = api.database.getCities(country_id=UA_CID, q=city_name)
nc = 0
#print_dic(CITY[nc])
#print 'найдено городов =>', len(CITY)

CITY_ID = CITY[nc]['cid']

SCHOOL =  api.database.getSchools(q=school_num,city_id=CITY_ID)
#print 'найдено школ =>', SCHOOL[0]
#print_dic(SCHOOL[1])
SCHOOL_ID = SCHOOL[1]['id']

users = api.users.search(count=10,city=CITY_ID, country=UA_CID, age_from=14, age_to=18, school_year=2017, school = SCHOOL_ID, fields = "photo_100,last_seen,photo_id,has_mobile,universities")
print("""<!DOCTYPE HTML>
        <html>
       
        <head>
            <meta charset="utf-8">
            <title>Vkbot</title>
            <link rel= "stylesheet" type= "text/css" href= "./css.css">
        </head>
        <body>
	<div id ='header'>
	<p id='top'>Имя пользователя<p>
	</div>
	<div id='content'>""")
for u in users:
    if type(u) is not int:
       print("""<div class ='photo'>{}</div>""".format ('<img src='+str(u['photo_100'])+ ' alt=''>'))
       print("""<div id ='info'><p id= 'user_name'>{}</p></div>""".format(''+str(u['first_name'])+ ' '+str(u['last_name'])+ ''))
#dragon= api.users.get(user_ids=u['uid'],fields = 'photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, wall_comments, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me')
       #len((u['universities']))
print("""</div></body></html>""")

