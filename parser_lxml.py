from urllib.request import urlopen
from datetime import datetime
import lxml.html as html
import json

target_url = 'https://habr.com/'

def load_page(url):
    return  html.parse(urlopen(url)).getroot()

def get_file_name():    
    return '%s.json' % datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")

def save_data(data):
    with open(get_file_name(), 'w', encoding='utf-8') as file_json:
        json.dump(data, file_json, ensure_ascii = False)
    file_json.close()

def parse_habr(url):    
    page_data = load_page(url)
    articles = []
    article_urls = page_data.xpath('//h2[@class="post__title"]/a/@href')

    for item in article_urls:
        print('# ************************************************************* #')
        print(item)
        print('#----------------------------------------#')
        post_data = load_page(item)

        header = post_data.xpath('//span[@class="post__title-text"]/text()')
        print('     Header : %s' % header)

        text = post_data.xpath('//div[contains(@class,"post__text")]//text()')
        print('     Text : %s' % text)

        images = post_data.xpath('//div[contains(@class,"post__text")]//img/@src')
        print('     Images :')
        for img in images:
            print('         %s' % img)

        articles.append({
            "header": header[0],
            "text": ''.join(text),
            "images": [{"img": img} for img in images]
            })

    return articles

def main():
    save_data(parse_habr(target_url))

if __name__ == '__main__':
    main()