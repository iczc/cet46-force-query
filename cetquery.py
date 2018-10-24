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
