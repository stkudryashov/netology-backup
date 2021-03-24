import requests
from pprint import pprint

vk = 'token'
yandex = 'token'


class VkBackup:
    url = 'https://api.vk.com/method/'

    def __init__(self, token: str, version: str):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

    def get_photos(self, album):
        photos_url = self.url + 'photos.get'
        photos_params = {'album_id': album, 'extended': 1, 'photo_sizes': 1}
        response = requests.get(photos_url, params={**self.params, **photos_params})
        pprint(response.json()['response']['items'])


class YaUploader:
    url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_url(self, yandex_path: str):
        get_url = self.url + 'resources/upload'
        headers = self.get_headers()
        params = {'path': yandex_path, 'overwrite': True}
        response = requests.get(get_url, headers=headers, params=params)
        return response.json()['href']

    def upload(self, yandex_path: str, local_path: str):
        upload_url = self._get_upload_url(yandex_path)
        response = requests.put(upload_url, data=open(local_path, 'rb'))
        return response.status_code


if __name__ == '__main__':
    uploader = YaUploader(yandex)
    vk_backup = VkBackup(vk, '5.130')

    vk_backup.get_photos('profile')
