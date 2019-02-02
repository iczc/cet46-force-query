import base64
import requests

from hashlib import md5


class RuokuaiClient:

    def __init__(self, username, password):
        self.username = username
        self.password = md5(password.encode('utf-8')).hexdigest()

        self.base_params = {
            'username' : self.username,
            'password' : self.password,
            'softid'   : '114907',
            'softkey'  : '7037c966fa8d4f908f3e855fc03e5796'
        }
        
        self.headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'api.ruokuai.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

    def get_user_info(self):
        params = {'username': self.username, 'password': self.password}
        response = requests.post('http://api.ruokuai.com/info.json', data=params, headers=self.headers)
        return response.json()

    def upload_image(self, image_path, typeid='3040', timeout=60):
        params = {
            'typeid' : typeid,
            'timeout': timeout,
            'image': ''
        }
        params.update(self.base_params)
        with open(image_path, 'rb') as f:
            image = f.read()
            base64_data = base64.b64encode(image)
        params['image'] = base64_data
        response = requests.post('http://api.ruokuai.com/create.json', data=params, headers=self.headers)
        return response.json()

    def report_error(self, image_id):
        params = {
            'id': image_id,
        }
        params.update(self.base_params)
        response = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return response.json()
