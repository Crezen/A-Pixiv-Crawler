# 这是一个示例 Python 脚本。
import sys
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests import utils, HTTPError


def get_cookie(cookie_path='catch_pixiv\\cookie.txt'):
	file = open(cookie_path, 'r')
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

	response.close()
	return cookie


def default_header():
	"""
	:return: 返回一个缺省的header
	"""

	return {
		'User-Agent': str(UserAgent().random),
		'referer': "https://www.pixiv.net/"
	}


def get_soup(url, session, headers):
	"""
	:param url: str
	:param session: request.Session
	:param headers: Dictionary of HTTP Headers
	:return: BeautifulSoup of that url.Text
	"""

	try:
		response = session.get(url, headers=headers)
	except HTTPError:
		print('HTTPError')
		return []

	bs = BeautifulSoup(response.text, 'lxml')
	return bs


class PixivCrawler:
	def __init__(self):
		self.session = None
		self.url_list = None
		self.website = 'https://www.pixiv.net/'

	def login(self, cookie):
		"""
		:param cookie: str
		:return boolean 返回是否登录成功
		"""

		self.session = requests.session()
		utils.add_dict_to_cookiejar(self.session.cookies, {'HTTPSESSION': cookie})

		return True

	def user_uid(self, author_name, header=None):
		"""获取该作者的uid

		:param header: (optional) 爬虫的请求头
		:param author_name: str 作者的用户名称
		:return: str 返回作者的uid
		"""

		header = header if header is not None else default_header()
		url = "https://www.pixiv.net/search_user.php?nick=" + author_name + "&s_mode=s_usr"
		bs = get_soup(url, self.session, headers=header)
		find_uid = bs.find('a', {'target': '_blank'}, text=author_name)
		uid = find_uid['href'][7:]

		return uid

	def user_artwork(self, uid, header=None):
		"""获取该作者的全部作品的uid,并返回字典

		:param uid: 作者uid
		:param header: (optional) 爬虫请求头
		:return: dict 返回作者作品id的json字典
		"""
		header = header if header is not None else default_header()
		get_artwork_site = "https://www.pixiv.net/ajax/user/" + uid + "/profile/all?lang=zh"
		get_artwork = self.session.get(get_artwork_site, headers=header)
		json = get_artwork.json()
		artwork_ids = json['body']['illusts']

		return artwork_ids

	def origin_pic(self, uid, header=None):
		"""获取该图片的origin大图链接

		:param uid:
		:param header:
		:return:
		"""

		url_list = []
		site = self.website + "ajax/illust/" + uid + "/pages?lang=zh"
		header = header if header is not None else default_header()
		response = self.session.get(site, headers=header)
		json = response.json()
		for body in json["body"]:
			url = body['urls']['original']
			url_list.append(url)

		return url_list

	def get(self, mode: str, key_word: str, **kwargs):
		mode = mode.lower()
		match mode:
			case 'user':
				self.catch_user(key_word, **kwargs)
			case 'tags':
				self.catch_tags()
			case 'rank':
				self.catch_rank()
			case _:
				raise ValueError("mode参数为无效值")

	def catch_user(self, author_name, catch_num=None, sleep_time=None, header=None):
		"""将作者的url写入data.txt

		:param author_name: str 作者昵称
		:param catch_num: (optional) int 要爬取的作品数量，默认全部爬取
		:param sleep_time: (optional) int 爬虫的url访问时间间隔，默认为2s
		:param header: (optional) 爬虫的请求头
		:return: list(str): url_list 获取的作品大图url的列表
		"""

		catch_num = catch_num if catch_num is not None else sys.maxsize
		header = header if header is not None else default_header()
		sleep_time = sleep_time if sleep_time is not None else 2

		# 获取作者uid
		uid = self.user_uid(author_name, header=header)
		print('作者uid：' + uid)

		# 获取作者所有作品的id
		artwork_ids = self.user_artwork(uid, header=header)
		nums = len(artwork_ids)   # 获取作品数量
		print('共查找到' + str(nums) + '个作品')

		# 爬取所有图片大图的url
		url_list = []
		for i, artwork_id in enumerate(artwork_ids):
			if i >= min(catch_num, nums):
				break
			time.sleep(sleep_time)
			lists = self.origin_pic(artwork_id)
			url_list = url_list + lists
			print('catch ' + artwork_id + ' ' + str(len(lists)) + ' pics')
		print('已获取' + str(min(catch_num, nums)) + '个作品的url')

		return url_list

	def catch_tags(self):
		pass

	def catch_rank(self):
		pass

	def close(self):
		self.session.close()

# 获取post_key
# session = requests.session()
# response = session.get("https://accounts.pixiv.net/login?return_to=https%3A%2F%2F"
#                        "www.pixiv.net%2F&lang=zh&source=pc&view_type=page", headers=header)

# bs = BeautifulSoup(response.text, 'lxml')
# tt = bs.find('input', {'type': "hidden", 'id': "init-config"})
# get_tt = re.findall('"pixivAccount.tt":".*?"', tt['value'])
# tt = re.findall(':"[0-9a-z]*?"', get_tt[0])
# tt = tt[0][2:-1]
# data = {
# 	'login_id': '1228195163@qq.com',
# 	'password': 'zdy13694800161',
# 	'source': 'pc',
# 	'app_ios': '0',
# 	'ref': '',
# 	'return_to': 'https://www.pixiv.net/',
# 	'g_recaptcha_response': '',
#   # 暂未解决的reCAPTCHA验证
# 	'recaptcha_enterprise_score_token': '03ANYolqvGzzcOUYbcxz1f24ROABvsIacD-rFfEYad-B0KZZn29l_KlXrl8Z7aflwxStRKEO6_UwIr'
# 	                                    '3NnHKIWFvMkHa5rQe7yV4lmSRLcpnNdP8vx7Gil2pWsITBwpvd0pQWkKx9ksvya6Y-TYxgtRV-yTE4'
# 	                                    'JeeE0G_nLgEU6Uew-WKpdvwahYmw-4DAQz5oU1obOVzssNmhIg5DtltBeuJeZk-Cu_VlY2olC3BQ02'
# 	                                    'JaafmfuR30lkqHkQMrCXhle_pRMrIXcqIr2GuWBfIRALVEOTwsexbwF2fywurajzI6yzt3iCUViNAm'
# 	                                    'T_MsjWTO0M0kBRXRfSuIm3SAJVrwiN6P59tC-_PTsrEFd0g9vxRXca-_fwg_hvrm3CK4V9tbT8nTz6'
# 	                                    'wCiOlv9GbtDf8DHQAZdDY7VX5zvApqkqfPXffzy_orzNlrruxkvs2gJyWcg72vhY69w7wMsrf98GPc'
# 	                                    'lF2aQSw1Oxr0CISD-blym3ojzX0cOKljjexqHOzRKPQdxL86vJ2VBUnjKLRFPGe7_kGRVLtTZHxftc'
# 	                                    '8AvfkUoGAsW7XNqmtJq5dTEy0dwTIxWaQHUcxX3HSINaRnkojtErFlfK5IjWhK1UJKIjLaEu3poHtS'
# 	                                    'FdtMqUKHodzQlrCHpZF596huvZefO3bx-wGH6teKAPZtYqevuxELGXHwLnQKWUbZurfKOZIIPD6-gJ'
# 	                                    '_IAv3dMEP_3ttgyKHe3Qn93xdV3nxhjGt93kh7lhNZHFo_4OXUlF0LUhh8FjrgmXmrpSpQHH0ZUSbB'
# 	                                    'C2mgOZU-k4jTQ_z3fOb6Rzz3JkxJ7gBG5BQa-FPyQdWstaszr5wQUeNADTfmZCNlrAAKjxZlpBYJlG'
# 	                                    'vyIV87EIhbIRITj0FaxWBUUTgFqtI08LpNMc7Kwwo15li3YugcFbfHsOJIvsKeqv5srTQJ-6TXQ8Gm'
# 	                                    'tLyBt9jsEMRp7y5tJW83pKPUV7zbb8FbEQRJyIIDlNvHjnewWF9SsykcbkfWl9VP9J_V0Nh4fEf8EB'
# 	                                    'sCD5OuAgBcNCmE0gLZAVWq0yU9cqB9jWmNPuhdbbMGGOsd50CTbFl2Kw9Fd1WEGyvwD6Uf40_Pb3ws'
# 	                                    '9J4qUJCG4_HL-Mx51v_uZAuIQg356BQFo97kj_HUfkHaa9qyGTfpt6TdIIdMehDkV5OhhENJnOT5AG'
# 	                                    'B7TIsMxHAgnn-u3nyfbN8rvm-X_tPNGnKt4drDsRnONK1hKWc6hN7oH0-0Ldk9WmF89uyzb3j6SOVD'
# 	                                    'akrSkZTEg_0zS7QBD6a7NxcHU9xqNdR7g2_sQPNjVI0yFJiO4_U5IQJfC1Nxnsit0Z3x5-REdBret4'
# 	                                    'G4kaKxehXF0X1dfFPJ0yu9jqZJYbKk2fO1HVS-Gt-2x25XTGTp60oa-19k9vDMsJJpG6HJSOsgRLL7'
# 	                                    'Nmr0ofijpAolmW_KtohRCMdzm3_FAVEE_hpRY9y2h8MLgFLttj-GOhbWKWp8e8kS9TtEYEKZ7ygjoU'
# 	                                    'zvtvkb2tXw-yhHhaPOmhnXLAWzQOhJhYTe1cvr_pxxGc43aNuS6etTk0mq0MczhKYZ7avlRQoOwmry'
# 	                                    'TFPiJNwakKfVH-oQ6p7BVJClNjfGM7xnc6wJ_GT3songWIxURs4lSbwFh0C9lHUkUyBkSYKR-rcA8a'
# 	                                    'iBKWSa5bIaR9Q-zRYNajGcb25YhyDeAa0jaPf0TTELrY6npp9E3Dh5A6xfojjBcIH06qvab-YilCfO'
# 	                                    'PLepoPthvTBVSAak03Hx2RbAHtTaPGCLKAEze9aEERHLhlBufsXaEhtD20dd_7ZbbSg3sWT2UvpQex'
# 	                                    'JtT1N-nJFVHJqrYGderKVzbAS1ON__1RpO9hEIaVJj1xh1fY-c0nwx73QWs54wstgdX60yUJgNGPPS'
# 	                                    'qXzhfrGcMdrTfljeiCuXTiIqQHuZEDC7Dzvxp-tI8qj2GaWk3tG1463JC7D7rlIHPRy6Fp1Eu5oF31'
# 	                                    'aDn08w',
# 	'tt': tt
# }

# 自检ip
# response1 = requests.get("https://icanhazip.com/")
# print(response.text)

