import requests
import datetime

from vk_token import vk_token


class VkBackup:
    url = 'https://api.vk.com/method/'

    def __init__(self, token: str, version: str):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

    def get_photos(self, vk_album, owner_id=None, count=50):
        photos_url = self.url + 'photos.get'
        photos_params = {'owner_id': owner_id, 'album_id': vk_album, 'extended': 1, 'photo_sizes': 1, 'count': count}
        response = requests.get(photos_url, params={**self.params, **photos_params})
        return response.json()['response']['items']

    def get_user(self, profile_id):
        user_url = self.url + 'users.get'
        user_params = {'user_ids': profile_id}
        response = requests.get(user_url, params={**self.params, **user_params})
        return response.json()


class YaUploader:
    url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_folder(self, yandex_path: str):
        create_url = self.url + 'resources/'
        create_params = {'path': yandex_path}
        response = requests.put(create_url, headers=self.get_headers(), params=create_params)
        if response.status_code == 201:
            print(f'Папка {yandex_path} успешно создана')
        return response.status_code

    def upload_from_url(self, yandex_path: str, photo_url: str):
        upload_url = self.url + 'resources/upload'
        upload_params = {'path': yandex_path, 'url': photo_url}
        response = requests.post(upload_url, headers=self.get_headers(), params=upload_params)
        if response.status_code == 202:
            print(f'Фотография {yandex_path} загружается')
        return response.status_code


def create_backup_yandex(name: str, uploader: YaUploader, backuper: VkBackup, albums: list, user_id=None, count=50):
    print('\nНачалась загрузка файлов на Яндекс Диск')

    uploader.create_folder('VkBackup/')
    backup_folder = f'VkBackup/{name}/'
    uploader.create_folder(backup_folder)

    for album in albums:
        uploader.create_folder(backup_folder + album)
        photos = backuper.get_photos(album.lower(), user_id, count)

        for photo in photos:
            photo_path = f'VkBackup/{name}/{album}/{str(photo["likes"]["count"])}_{photo["date"]}.jpg'
            uploader.upload_from_url(photo_path, photo['sizes'][-1]['url'])

    print('Загрузка завершена')


if __name__ == '__main__':
    backup_name = datetime.datetime.isoformat(datetime.datetime.now(), sep='-')
    backup_name = backup_name.replace(':', '-').replace('.', '-')

    albums_list = ['Profile', 'Wall']
    vk_backuper = VkBackup(vk_token, '5.130')

    user_id = input('Введите id пользователя (оставьте пустым для своего профиля): ')

    if user_id == '':
        user_id = None

    try:
        user_response = vk_backuper.get_user(user_id)
        user_response = user_response['response']

        ya_token = input('Введите токен Яндекс Диска: ')
        ya_uploader = YaUploader(ya_token)

        create_backup_yandex(backup_name, ya_uploader, vk_backuper, albums_list, user_id)
    except KeyError:
        print('Некорректный id пользователя')
