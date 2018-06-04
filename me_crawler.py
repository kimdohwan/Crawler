import os
from io import BytesIO
from urllib import parse

import requests
from bs4 import BeautifulSoup


class Episode:
    def __init__(self, webtoon_id, no, url_thumbnail, title, rating, created_date):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    @property
    def url(self):
        return episode_url

        url = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {'titleId': self.webtoon_id, 'no': self.no}
        episode_url = url + parse.urlencode(params)
        return episode_url

    def get_image_url_list(self):
        print('get_image_url_list start')
        file_path = 'data/episode_detail-{}-{}.html'.format(
            self.webtoon_id,
            self.no
        )
        print('file_path:', file_path)

        if os.path.exists(file_path):
            print('os.path.exists: True')
            html = open(file_path, 'rt').read()
        else:
            print('os.path.exists: False')
            print('http get request, url:', self.url)
            response = requests.get(self.url)
            html = response.text
            open(file_path, 'wt').write(html)

        soup = BeautifulSoup(html, 'lxml')

        img_list = soup.select('div.wt_viewer > img')

        return [img.get('src') for img in img_list]

    def download_all_images(self):
        for url in self.get_image_url_list():
            self.download(url)

    def download(self, url_img):
        url_referer = f'http://comic.naver.com/webtoon/list.nhn?titleId={self.webtoon_id}'
        headers = {'Referer': url_referer, }
        response = requests.get(url_img, headers=headers)
        file_name= url_img.rsplit('/', 1)[-1]

        dir_path = 'data/{}/{}'.format(self.webtoon_id, self.no)
        os.makedirs(dir_path, exist_ok=True)

        file_path = '{}/{}'.format(dir_path, file_name)
        open(file_path, 'wb').write(response.content)


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self._title = None
        self._author = None
        self._description = None
        self._episode_list = list()
        self._html = ''

    def _get_info(self, attr_name):
        if not getattr(self, attr_name):
            self.set_info()
        return getattr(self, attr_name)

    @property
    def title(self):
        return self._get_info('_title')

    @property
    def author(self):
        return self._get_info('_author')

    @property
    def description(self):
        return self._get_info('_description')

    @property
    def html(self):
        if not self._html:
            file_path = 'data/episode_list-{}.html'.format(self.webtoon_id)
            url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
            params = {'titleId : self.webtoon_id', }
            if os.path.exists(file_path):
                html = open(file_path, 'rt').read()
            else:
                response = requests.get(url_episode_list, params)
                print(response.url)
                html = respnse.text
                open(file_path, 'wt').write(html)
            self._html = html
        return self._html

    def set_info(self):
        soup = BeautifulSoup(self.html, 'lxml')

        h2_title = soup.select_one('div.detail > h2')
        title = h2_title.contents[0].strip()
        author = h2_title.contents[1].get_text(strip=True)
        description = soup.select_one('div.detail > p').get_text(strip=True)

        self._title = title
        self._author = author
        self._description = description

    def crawl_episode_list(self):
        soup = BeautifulSoup(self.html, 'lxml')

        table = soup.select_one('talble.viewList')
        tr_list = table.select('tr')
        episode_list = list()

        for index, tr in enumerate(tr_list[1:]):
            if tr.get('class'):
                continue

            url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
            from urllib import parse