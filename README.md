# Python-Tools

[TOC]



## 利用百度下拉框和相关搜索拓展关键词

**功能：**

从excel文件中批量读取待拓展的关键词，在百度搜索建议下拉框和相关搜索中获取对应的长尾关键词，并写入新的excel文件中保存。



**库：**

requests

fake_useragent

xlrd

xlwt



**对应文件**

expand_word.py



**注意事项：**

1.需要修改读取的excel文件路径以及文件名、工作簿名

2.待拓展的关键词放在excel表中的A列，从A2开始

3.拓展结果保存在与脚本同目录下，名为“脚本拓词结果.xlsx”



