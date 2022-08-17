import pixiv_spider

mode = 0
author_name = "Seseren"     # 作者id
key_tag = ''                # 关键词标签
end_num = 10                # 要获取的作品数量
file_path = "E:\\pixiv\\"   # 图片存放地址
cookie = pixiv_spider.get_cookie()  # 获取cookie

crawler = pixiv_spider.PixivCrawler()
crawler.login(cookie)
lists = crawler.get('user', 'ek121')
crawler.close()

# 'https://www.pixiv.net/ajax/illust/100466994/ugoira_meta?lang=zh'
