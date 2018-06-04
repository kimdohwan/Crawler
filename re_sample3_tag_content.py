import re
p = re.compile(r'<[^/]*?>(.*?)</.*?>)', re,DOTALL)
html = open('re_tag_example.html', 'rt').read()

result = re.findall(p, html)
for item in result:
    print(item)
