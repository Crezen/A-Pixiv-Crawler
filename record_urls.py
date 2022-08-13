# 这是一个示例 Python 脚本。
import ssl
import sys
import time
import requests
from bs4 import BeautifulSoup
ssl._create_default_https_context = ssl._create_unverified_context


# 设置参数
author_name = "ek121"   # 作者id
end_num = sys.maxsize   # 要获取的作品数量
file_path = ""          # 储存图片的路径

# 手动输入cookies
cookie = input('请输入cookies')
header = {
	'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
	'cookie': cookie,
	'referer': "https://www.pixiv.net/tags/ek121/artworks?s_mode=s_tag"
}
# 暂且无用的代理ip
# proxies = {
# 	"http": "http://47.92.113.71:80",
# 	"https": "https://211.24.95.49:47615",  # useless
# }
website = "https://www.pixiv.net/"

# 获取作者uid
url = "https://www.pixiv.net/search_user.php?nick=" + author_name + "&s_mode=s_usr"
response = requests.get(url, headers=header)
bs = BeautifulSoup(response.text, 'lxml')
response.close()
find_uid = bs.find('a', {'target': '_blank'}, text=author_name)
uid = find_uid['href'][6:]

# 获取作者所有作品的id
get_artwork_site = "https://www.pixiv.net/ajax/user" + uid + "/profile/all?lang=zh"
get_artwork = requests.get(get_artwork_site, headers=header)
JSON = get_artwork.json()
get_artwork.close()
artwork_ids = JSON['body']['illusts']
nums = len(artwork_ids)   # 获取作品数量

# 爬取所有图片大图的url
for i in range(0, min(end_num, nums)):
	artwork_id = artwork_ids[i]  # 作品id
	site = website + "ajax/illust/" + artwork_id + "/pages?lang=zh"
	time.sleep(2)
	session = requests.get(site, headers=header)
	JSON = session.json()
	session.close()
	for body in JSON["body"]:
		URL = body['urls']['original']
		with open('data.txt', 'w+') as file:
			file.writelines(URL)

# session = requests.session()
# response = session.get("https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2F&lang=zh&source=pc&view_type=page",
#                        headers=header)
#
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
# 	'recaptcha_enterprise_score_token': '03ANYolqvGzzcOUYbcxz1f24ROABvsIacD-rFfEYad-B0KZZn29l_KlXrl8Z7aflwxStRKEO6_UwIr3NnHKIWFvMkHa5rQe7yV4lmSRLcpnNdP8vx7Gil2pWsITBwpvd0pQWkKx9ksvya6Y-TYxgtRV-yTE4JeeE0G_nLgEU6Uew-WKpdvwahYmw-4DAQz5oU1obOVzssNmhIg5DtltBeuJeZk-Cu_VlY2olC3BQ02JaafmfuR30lkqHkQMrCXhle_pRMrIXcqIr2GuWBfIRALVEOTwsexbwF2fywurajzI6yzt3iCUViNAmT_MsjWTO0M0kBRXRfSuIm3SAJVrwiN6P59tC-_PTsrEFd0g9vxRXca-_fwg_hvrm3CK4V9tbT8nTz6wCiOlv9GbtDf8DHQAZdDY7VX5zvApqkqfPXffzy_orzNlrruxkvs2gJyWcg72vhY69w7wMsrf98GPclF2aQSw1Oxr0CISD-blym3ojzX0cOKljjexqHOzRKPQdxL86vJ2VBUnjKLRFPGe7_kGRVLtTZHxftc8AvfkUoGAsW7XNqmtJq5dTEy0dwTIxWaQHUcxX3HSINaRnkojtErFlfK5IjWhK1UJKIjLaEu3poHtSFdtMqUKHodzQlrCHpZF596huvZefO3bx-wGH6teKAPZtYqevuxELGXHwLnQKWUbZurfKOZIIPD6-gJ_IAv3dMEP_3ttgyKHe3Qn93xdV3nxhjGt93kh7lhNZHFo_4OXUlF0LUhh8FjrgmXmrpSpQHH0ZUSbBC2mgOZU-k4jTQ_z3fOb6Rzz3JkxJ7gBG5BQa-FPyQdWstaszr5wQUeNADTfmZCNlrAAKjxZlpBYJlGvyIV87EIhbIRITj0FaxWBUUTgFqtI08LpNMc7Kwwo15li3YugcFbfHsOJIvsKeqv5srTQJ-6TXQ8GmtLyBt9jsEMRp7y5tJW83pKPUV7zbb8FbEQRJyIIDlNvHjnewWF9SsykcbkfWl9VP9J_V0Nh4fEf8EBsCD5OuAgBcNCmE0gLZAVWq0yU9cqB9jWmNPuhdbbMGGOsd50CTbFl2Kw9Fd1WEGyvwD6Uf40_Pb3ws9J4qUJCG4_HL-Mx51v_uZAuIQg356BQFo97kj_HUfkHaa9qyGTfpt6TdIIdMehDkV5OhhENJnOT5AGB7TIsMxHAgnn-u3nyfbN8rvm-X_tPNGnKt4drDsRnONK1hKWc6hN7oH0-0Ldk9WmF89uyzb3j6SOVDakrSkZTEg_0zS7QBD6a7NxcHU9xqNdR7g2_sQPNjVI0yFJiO4_U5IQJfC1Nxnsit0Z3x5-REdBret4G4kaKxehXF0X1dfFPJ0yu9jqZJYbKk2fO1HVS-Gt-2x25XTGTp60oa-19k9vDMsJJpG6HJSOsgRLL7Nmr0ofijpAolmW_KtohRCMdzm3_FAVEE_hpRY9y2h8MLgFLttj-GOhbWKWp8e8kS9TtEYEKZ7ygjoUzvtvkb2tXw-yhHhaPOmhnXLAWzQOhJhYTe1cvr_pxxGc43aNuS6etTk0mq0MczhKYZ7avlRQoOwmryTFPiJNwakKfVH-oQ6p7BVJClNjfGM7xnc6wJ_GT3songWIxURs4lSbwFh0C9lHUkUyBkSYKR-rcA8aiBKWSa5bIaR9Q-zRYNajGcb25YhyDeAa0jaPf0TTELrY6npp9E3Dh5A6xfojjBcIH06qvab-YilCfOPLepoPthvTBVSAak03Hx2RbAHtTaPGCLKAEze9aEERHLhlBufsXaEhtD20dd_7ZbbSg3sWT2UvpQexJtT1N-nJFVHJqrYGderKVzbAS1ON__1RpO9hEIaVJj1xh1fY-c0nwx73QWs54wstgdX60yUJgNGPPSqXzhfrGcMdrTfljeiCuXTiIqQHuZEDC7Dzvxp-tI8qj2GaWk3tG1463JC7D7rlIHPRy6Fp1Eu5oF31aDn08w',
# 	'tt': tt
# }

# response1 = requests.get("https://icanhazip.com/")
# print(response.text)


# 按间距中的绿色按钮以运行脚本。


# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
