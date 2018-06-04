import requests

response = requests.get('https://comic.naver.com/webtoon/weekday.nhn')
print(response.status_code)
print(response.text)

f = open('weekday.html', 'wt')
f.write(response.text)
f.close()


with open('weekday.html', 'wt') as f:
    f.write(response.text)
