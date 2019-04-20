import requests
import shutil
import lxml.html as parser
import json
import string
import os
import hashlib

def decode(data):
    return ''.join(x for x in data if x in string.printable).strip()

url = 'https://www.mobilluck.com.ua/katalog/mobila/pages_{}_15.html'
img_storage = 'E:\\Unsorted\\education\\labs\\пошук_і_попередня_підготовка_даних\\3\\images'
pages_cnt = 2
data = []

os.makedirs(img_storage, exist_ok=True)

for page_i in range(1, pages_cnt, 1):
    print('\r Page: {}/{}'.format(page_i, pages_cnt), end='\r')
    response = requests.get(url.format(page_i))
    html = response.text
    root = parser.fromstring(html)
    items = root.cssselect('.ico_zindex')

    try:
        for i, item in enumerate(items):
            img_url = 'https:{}'.format(item.cssselect('.ccitem2 > .ccitem2t > table tr > td:first-child > a > img')[0].get('data-original'))
            price = decode(item.cssselect('.cci2_newprice')[0].text)
            info = decode(item.cssselect('.cci2_mdl > a')[0].get('title'))
            

            extBegIndex = img_url.rfind('.')
            ext = '.jpg'
            if extBegIndex != -1:
                ext = img_url[extBegIndex:]
            img_name = hashlib.md5(img_url.encode('utf-8')).hexdigest() + ext

            r = requests.get(img_url, stream=True)
            if r.status_code == 200:
                with open(os.path.join(img_storage, img_name), 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f) 

            data.append({
                'img_url': img_url,
                'img_path': os.path.join(img_storage, img_name),
                'info': info,
                'price': price
            })
    except Exception as e:
        print('Error in item #{}:{}'.format(i, e))
with open('res.json', 'w') as fp:
    json.dump(data, fp)