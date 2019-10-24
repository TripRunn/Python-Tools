# Author:TripRunn
# 图片下载器

import json
import os
import sys
import time
import requests
from urllib import request

keyword = input("图片关键词：")
start = input("图片起始位置：")
lens = input("想要下载的图片个数：")
start = int(start)
lens = sum = int(lens)
num = 0
bar = ""

dirpath = os.path.join(os.getcwd(), keyword)
isExists = os.path.exists(dirpath)
if not isExists:
    os.mkdir(dirpath)
    print(dirpath + " 目录创建成功")

while True:
    api = "https://pic.sogou.com/pics?query={0}&mode=1&start={1}&len={2}" \
          "&reqType=ajax&reqFrom=result&tn=0".format(keyword, start, lens)
    r = requests.get(api)
    items = json.loads(r.text)['items']
    count = 0
    for item in items:
        pic_url = item['pic_url']
        suff = pic_url.split("/")[-1]
        if '.' in suff:
            path = r"{0}\{1}".format(dirpath, suff)
        else:
            path = r"{0}\{1}.jpg".format(dirpath, suff)

        try:
            request.urlretrieve(pic_url, path)
            num += 1
            bar = bar + "■"

            os.system('cls')
            print("图片下载（{0}/{1}）".format(num, sum))
            print(bar)
            if num < lens:
                print("\n正在下载： " + pic_url)
        except Exception as e:
            count += 1
            # print(e)
    if count != 0:
        start = start + lens
        lens = count
    else:
        break

print("\n10秒后自动关闭...")
time.sleep(10)