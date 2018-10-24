import codecs
import configparser
import os
import time

from cetquery import CetQuery
from captcha.ruokuai import RuokuaiClient


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
    room_lower = config['room_lower']
    room_upper = config['room_upper']
    seat_lower = config['seat_lower']
    seat_upper = config['seat_upper']

    room_id    = int(room_lower)
    room_upper = int(room_upper)
    seat_id    = int(seat_lower)
    seat_upper = int(seat_upper)

    ruokuai = RuokuaiClient(config['api_username'], config['api_password'])

    while True:
        user_id = prefix + "%03d" % room_id + "%02d" % seat_id
        print(user_id)
        cet = CetQuery(user_id, user_name)
        captcha_path = cet.get_captcha()
        ruokuai_result = ruokuai.upload_image(captcha_path)
        captcha = ruokuai_result['Result']
        # captcha = input("input captcha\n")
        data = cet.get_result(captcha)

        if '结果为空' in data:
            print('not found')
            seat_id += 1
        elif '验证码错误' in data:
            ruokuai.report_error(ruokuai_result['Id'])
            print('captcha error')
            continue
        elif 'z' in data:
            print('found it!')
            print(data)
            break

        if seat_id > seat_upper:
            room_id += 1
            seat_id = int(seat_lower)
            if room_id > room_upper:
                break
        time.sleep(1)


if __name__ == '__main__':
    search()
