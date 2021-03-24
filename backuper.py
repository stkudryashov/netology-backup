import requests
from pprint import pprint


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
        return response.json()['response']['items']


class YaUploader:
    url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def upload_from_url(self, yandex_path: str, photo_url: str):
        upload_url = self.url + 'resources/upload'
        upload_params = {'path': yandex_path, 'url': photo_url}
        response = requests.post(upload_url, headers=self.get_headers(), params=upload_params)
        return response


if __name__ == '__main__':
    uploader = YaUploader(yandex)
    vk_backup = VkBackup(vk, '5.130')
    photos = vk_backup.get_photos('profile')
    uploader.upload_from_url('VK', photos[0]['sizes'][-1]['url'])
