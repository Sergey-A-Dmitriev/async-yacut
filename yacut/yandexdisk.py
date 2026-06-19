import asyncio
import os
import urllib

import aiohttp
from dotenv import load_dotenv

load_dotenv()
DISK_TOKEN = os.environ.get('DISK_TOKEN')
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
REQUEST_DOWNLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


async def async_upload_files_to_yandexdisk(files):
    """Ассинхронная функция создания и запуска задач загрузки файлов."""
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[upload_file_and_get_url(session, file) for file in files])


async def upload_file_and_get_url(session, file):
    """Асинхронная функция загрузки изображений и получения ссылок."""
    async with session.get(
            REQUEST_UPLOAD_URL,
            headers=AUTH_HEADERS,
            params={
                'path': 'app:/{}'.format(file.filename),
                'overwrite': 'True'},
    ) as response:
        upload_url = (await response.json())['href']
    async with session.put(data=file.read(), url=upload_url) as response:
        location = urllib.parse.unquote(response.headers['Location'])
    location = location.replace('/disk', '')
    async with session.get(
            REQUEST_DOWNLOAD_URL,
            headers=AUTH_HEADERS,
            params={'path': location, },
    ) as response:
        download_url = (await response.json())['href']
    return dict(filename=file.filename, url=download_url)