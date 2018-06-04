from bs4 import BeautifulSoup
html = open('data.weekday.html', 'rt').read()
soup = BeautifulSoup(html, 'lxml')

div_content = soup.find('div', id = 'content')
div_list_area = div_content.find('div', class_='list')
div_c