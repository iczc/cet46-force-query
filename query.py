import codecs
import configparser
import os
import random
import re
import requests
import tempfile

from urllib.request import urlretrieve


class CetQuery:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name
        self.cet_session = requests.Session()
        self.cet_session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
        self.cet_session.headers.update({'Referer': 'http://cet.neea.edu.cn/cet/'})
    
    def get_captcha(self):
        captcha_url = 'http://cache.neea.edu.cn/Imgs.do?c=CET&ik={}&t={}'.format(self.user_id, random.random())
        response_captcha = self.cet_session.get(captcha_url)
        image_url = re.findall(r'"(.*?)"', response_captcha.text)[0]
        captcha_path = 'code.png' # debug
        # captcha_path = tempfile.NamedTemporaryFile().name
        urlretrieve(image_url, captcha_path)
        return captcha_path
    
    def get_result(self, captcha):
        query_url = 'http://cache.neea.edu.cn/cet/query'
        post_data = {'data': '', 'v': ''}
        cet_rank = self.user_id[9]
        test_date = self.user_id[6:9]
        if cet_rank == '1':
            rank_str = 'CET4_' + test_date + '_DANGCI'
        elif cet_rank == '2':
            rank_str = 'CET6_' + test_date + '_DANGCI'
        post_data['data'] = rank_str + ',' + self.user_id + ',' +self.user_name
        post_data['v'] = captcha
        response_query = self.cet_session.post(query_url, post_data)
        data = re.findall(r'"(.*?)"', response_query.text)[0]
        return data


def get_config(filename):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {}
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    config.readfp(codecs.open(config_file, 'r', 'utf-8-sig'))
    return config['DEFAULT']

def search():
    config = get_config('config.ini')
    user_name  = config['user_name']
    prefix     = config['prefix']
    room_id    = config['room_id']
    seat_lower = config['seat_lower']
    seat_upper = config['seat_upper']

    room_id = int(room_id)
    seat_id = int(seat_lower)
    seat_upper = int(seat_upper)

    while True:
        user_id = prefix + "%03d" % room_id + "%02d" % seat_id
        print(user_id)
        cet = CetQuery(user_id, user_name)
        captcha_path = cet.get_captcha()
        captcha = input("captcha\n")
        data = cet.get_result(captcha)

        if '结果为空' in data:
            print('not found')
            seat_id += 1
        if '验证码错误' in data:
            print('captcha error')
            continue
        if 'z' in data:
            print('found it!')
            print(data)
            break
        if seat_id > seat_upper:
            room_id += 1
            seat_id = int(seat_lower)
            if room_id > 300:
                break


if __name__ == '__main__':
    search()
