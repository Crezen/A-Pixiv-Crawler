from catch_pixiv.crawler import PixivCrawler, get_cookie

mode = 0
author_name = "Seseren"     # 作者id
key_tag = ''                # 关键词标签
end_num = 10                # 要获取的作品数量
file_path = "E:\\pixiv\\"   # 图片存放地址

cookie = get_cookie()

crawler = PixivCrawler()
crawler.login(cookie)
lists = crawler.get('user', 'ek121')
crawler.close()

# if mode == 0:
# 	get_user(author_name, end_num, sleep_time, header)
# 	string = input('已获取图片链接，是否要开始下载： Yes/No\n')
# 	if string == 'Yes':
# 		catch_pics(sleep_time, header, file_path)

# 'https://www.pixiv.net/ajax/illust/100466994/ugoira_meta?lang=zh'
