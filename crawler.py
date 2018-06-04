import os
from urllib import parse
import requests
from bs4 import BeautifulSoup


class Episode:
    def __init__(self, webtoon_id, no, url_thumbnail,
                 title, rating, created_date):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    @property
    def url(self):
        """
        self.webtoon_id, self.no 요소를 사용하여
        실제 에피소드 페이지 URL을 리턴
        :return:
        """
        url = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {
            'titleId': self.webtoon_id,
            'no': self.no,
        }

        episode_url = url + parse.urlencode(params)
        return episode_url

    def download_all_images(self):
        for url in self.get_image_url_list():
            self.download(url)

    def download(self, url_img):
        # 서버에서 거부하지 않도록 http헤더 중 'Referer'항목을 채워서 요청
        url_referer = f'http://comic.naver.com/list.nhn?titleId={self.webtoon_id}'
        headers = {
            'Referer': url_referer,
        }
        response = requests.get(url_img, headers=headers)
        # 이미지url에서 이미지명을 가져옴
        file_name = url_img.rsplit('/', 1)[-1]

        # 이미지가 저장될 파일 경로,폴더가 없으면 생성해준다
        dir_path = f'data/{self.webtoon_id}/{self.no}'
        os.makedirs(dir_path, exist_ok=True)

        file_path = f'{dir_path}/{file_name}'
        open(file_path, 'wb').write(response.content)

    def get_image_url_list(self):
        print('1')
        file_path = 'data/episode_detail-{}-{}.html'.format(self.webtoon_id, self.no)
        if os.path.exists:
            html = open(file_path, 'rt').read()
            print('file_path', file_path)
        else:
            response = requests.get(self.url)
            html = response.text
            open(file_path, 'wt').write(html)
    #     if not self.img_url_list:
    #         file_path = 'data/episode_detail-{}-{}.html'.format(self.webtoon_id, self.no)
    #         img_url_list = 'https://comic.naver.com/webtoon/detail.nhn'
    #         params = {
    #             'titleId': self.webtoon_id,
    #         }
    #         if os.path.exists(file_path):
    #             img_url_list = open(file_path, 'rt').read()
    #         else:
    #             response = requests.get(img_url_list, params)
    #             img_url_list = response.text
    #             open(file_path, 'wt').write(html)
    #
    #         self.img_url_list = img_url_list
    #     return self.img_url_list
    #
    # def set_img_url(self):
    #     soup = BeautifulSoup(self.img_url_list, 'lxml')
    #
    #     divimg = soup.select_one('div.wt_viewer > img')
    #     img_url_list


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
        # 인스턴스에게 title 속성값이 존재하면 그걸 리턴
        # 없으면 set_info()호출 후 인스턴스의title값을 리턴
        if not self._title:
            self.set_info()
        return self._title
# 밑에 적은 내 코드가 안되는 이유를 생각해보자(강사님한테 질문 했음)
        # if self.title:
        #     return self.title
        # else:
        #     self.set_info()
        #     return self.title

    @property
    def author(self):
        if not self._author:
            self.set_info()
        return self._author

    @property
    def description(self):
        if not self._description:
            self.set_info()
        return self._description

    # 클래스 안에 크롤링 하는 함수를 넣어서 클래스를 만드는 순간 웹툰이 생성
    # 그리고 self를 넣어서 webtoon_id를 따로 넣어줄 필요가 없게된다.
    @property
    def get_html(self):
        # get_html의 결과 문자열을 인스턴스가 갖고 있을 수 있도록 설정
        # 1.인스턴스가 html을 갖고있지않을 경우
        #   인스턴스의 html속성을 데이터할당
        # 2.갖고있다면
        #   인스턴스의 html속성을 리턴
        if not self._html:
            # HTML파일을 저장하거나 불러올 경로
            file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
            # HTTP요청을 보낼 주소
            url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
            # HTTP요청시 전달할 GET Parameters
            params = {
                'titleId': self.webtoon_id,
            }
            # -> 'http://com....nhn?titleId=703845

            # HTML파일이 로컬에 저장되어 있는지 검사
            if os.path.exists(file_path):
                # 저장되어 있다면, 해당 파일을 읽어서 html변수에 할당
                html = open(file_path, 'rt').read()
            else:
                # 저장되어 있지 않다면, requests를 사용해 HTTP GET요청
                response = requests.get(url_episode_list, params)
                print(response.url)
                # 요청 응답객체의 text속성값을 html변수에 할당
                html = response.text
                # 받은 텍스트 데이터를 HTML파일로 저장
                open(file_path, 'wt').write(html)
            self._html = html
        return self._html

    def set_info(self):
        soup = BeautifulSoup(self._html, 'lxml')

        h2_title = soup.select_one('div.detail > h2')
        title = h2_title.contents[0].strip()
        author = h2_title.contents[1].get_text(strip=True)
        # div.detail > p (설명)
        description = soup.select_one('div.detail > p').get_text(strip=True)

        self._title = title
        self._author = author
        self._description = description

    def crawl_episode_list(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        # 만약 if 문을 통과하지 못하면 html을 호출못할 수도 있다

        # 파일 저장안해도 되는 경우
        # 파일 저장하지 않고 실행하고 싶다면 위의 코드를 주석처리후 사용할것!
        # url = 'http://comic.naver.com/webtoon/list.nhn'
        # params = {
        #     "titleId": webtoon_id
        # }
        # response = requests.get(url, params)
        # print(response.url)
        # soup = BeautifulSoup(response.text, 'lxml')

        # 에피소드 목록을 담고 있는 table
        table = soup.select_one('table.viewList')

        # table내의 모든 tr요소 목록
        tr_list = table.select('tr')

        # list를 리턴하기 위해 선언
        # for문을 다 실행하면 episode_lists 에는 Episode 인스턴스가 들어가있음
        episode_list = list()

        # 첫 번째 tr은 thead의 tr이므로 제외, tr_list의 [1:]부터 순회
        for index, tr in enumerate(tr_list[1:]):
            # 에피소드에 해당하는 tr은 클래스가 없으므로,
            # 현재 순회중인 tr요소가 클래스 속성값을 가진다면 continue
            if tr.get('class'):
                continue

            # 현재 tr의 첫 번째 td요소의 하위 img태그의 'src'속성값
            url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
            # 현재 tr의 첫 번째 td요소의 자식   a태그의 'href'속성값
            from urllib import parse
            url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
            query_string = parse.urlsplit(url_detail).query
            query_dict = parse.parse_qs(query_string)
            # print(query_dict)
            no = query_dict['no'][0]

            # 현재 tr의 두 번째 td요소의 자식 a요소의 내용
            title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
            # 현재 tr의 세 번째 td요소의 하위 strong태그의 내용
            rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
            # 현재 tr의 네 번째 td요소의 내용
            created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)

            # 매 에피소드 정보를 Episode 인보스턴스로 생성
            # new_episode = Episode 인스턴스
            new_episode = Episode(
                webtoon_id=self.webtoon_id,
                no=no,
                url_thumbnail=url_thumbnail,
                title=title,
                rating=rating,
                created_date=created_date,
            )

            # episode_lists Episode 인스턴스들 추가
            episode_list.append(new_episode)

        self._episode_list = episode_list

    @property
    def episode_list(self):
        if not self._episode_list:
            self.crawl_episode_list()
        return self._episode_list


if __name__ == '__main__':
    webtoon1 = Webtoon(703845)
    print(webtoon1.title)
    print(webtoon1.author)
    print(webtoon1.description)
    for episode in webtoon1._episode_list:
        print(episode.title)
