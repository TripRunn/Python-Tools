# Author:TripRunn
import requests
import re
import json
import xlrd
import xlwt
import time
import random
from fake_useragent import UserAgent


def read_excel():
    """
    读取excel文件中的A列，从A2到最后
    :return:list, 需要拓展的关键词列表
    """
    path = r'C:\Users\Admin\Desktop\脚本控制拓指数关键词.xlsx'  # 文件路径
    x1 = xlrd.open_workbook(path, encoding_override="utf-8")
    sheet1 = x1.sheet_by_name("待拓词")  # excel工作表名字
    nrows = sheet1.nrows  # 读总行数
    words = sheet1.col_values(0, 1, nrows)  # 取第一列 第二行到最后一行
    return words


def write_excel(dic):
    """
    将获取到的下拉框和相关搜索中的词写入excel
    :dic: dict, key为待拓展的关键词，value为对应的拓展结果
    """
    i = 1
    print("--------------开始写入excel---------")
    try:
        workbook = xlwt.Workbook()  # 新建文件
        sheet = workbook.add_sheet('1')
        sheet.write(0, 0, "指数关键词")
        sheet.write(1, 0, "拓词结果")
        for key in dic:
              rows = len(dic[key]) + 1
              sheet.write(0, i, key)
              for row in range(1, rows):
                    sheet.write(row, i, dic[key][row-1])
              i += 1
        workbook.save('脚本拓词结果.xlsx')
        print("--------------成功写入excel文件---------")
    except Exception as e:
        print("--------------写入文件失败-----------")
        print(e)


def fetch_dropdown_related():
    """
    取搜索下拉框的内容 以及 相关搜索的内容
    :word: 搜索关键词
    """
    words = read_excel()
    ua = UserAgent()
    dic = {}
    url_related = 'http://www.baidu.com/s'
    for i in range(0, len(words)):
        # 取下拉框词
        url_dropdown = 'https://www.baidu.com/sugrec?prod=pc&wd={}'.format(words[i])
        print('\n-----------{}下拉词----------'.format(words[i]))
        print('正在查找中...\n')
        r = requests.get(url_dropdown)
        word_dict = json.loads(r.text)
        wordlist = []
        for list1 in word_dict['g']:
            wordlist.append(list1['q'])
            print(list1['q'])

        # 取相关搜索词
        print('\n-----------{}相关搜素词----------'.format(words[i]))
        print('正在查找中...\n')
        payload = {'wd': '{}'.format(words[i])}
        time.sleep(random.uniform(1, 2))
        header = {'User-Agent': ua.random}
        r = requests.get(url_related, params=payload, headers=header)
        ze = r'<div id="rs"><div class="tt">相关搜索</div><table cellpadding="0">(.+?)</table></div>'
        xgss = re.findall(ze, r.text, re.S)
        xgze = r'<th><a href="(.+?)">(.+?)</a></th>'
        sj = re.findall(xgze, str(xgss), re.S)
        for x in sj:
            print(x[1])
            wordlist.append(x[1])
        dic[words[i]] = wordlist
    write_excel(dic)


if __name__ == '__main__':
      fetch_dropdown_related()
