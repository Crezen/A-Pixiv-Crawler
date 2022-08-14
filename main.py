import sys

from catch_pixiv.catch_picture import catch_pics
from catch_pixiv.get_header import get_header
from catch_pixiv.get_urls_user import get_user

mode = 0
author_name = "Seseren"     # 作者id
key_tag = ''                # 关键词标签
end_num = sys.maxsize       # 要获取的作品数量
file_path = "E:\\pixiv\\Seseren\\"  # 图片存放地址
sleep_time = 2              # 爬虫休眠间隔
header = get_header()       # 获取请求头

if mode == 0:
	get_user(author_name, end_num, sleep_time, header)
	string = input('已获取图片链接，是否要开始下载： Yes/No')
	if string == 'Yes':
		catch_pics(sleep_time, header, file_path)
