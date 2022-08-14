import requests
from fake_useragent import UserAgent


def get_header():
	"""获取请求头"""
	# 从cookie.txt中获取cookie
	file = open('catch_pixiv\\cookie.txt', 'r')
	cookie = file.readline()
	file.close()

	# 检验cookie是否失效
	header = {
		'User-Agent': str(UserAgent().random),
		'cookie': cookie,
		'referer': "https://www.pixiv.net/"
	}
	response = requests.get('https://www.pixiv.net/', headers=header)

	# 若登录不成功，网页中将包含’page-cool-index‘词段,则需重新输入cookie
	if response.text.find('page-cool-index') != -1:
		cookie = input('cookie已失效，请重新输入：')
		with open('catch_pixiv\\cookie.txt', 'w') as file:
			file.writelines(cookie)
		header = {
			'User-Agent': str(UserAgent().random),
			'cookie': cookie,
			'referer': "https://www.pixiv.net/"
		}
	response.close()
	return header
