import codecs
import configparser
import os

from urllib.request import urlretrieve
from cetquery import CetQuery


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
