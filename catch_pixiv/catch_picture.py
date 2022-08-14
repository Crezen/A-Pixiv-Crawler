import time
import requests


def catch_pics(sleep_time, header, file_path):
	with open('data.txt', 'r+') as file:
		while True:
			url = file.readline()
			if url == '':
				break
			pic_name = url[url.rfind('/')+1:-1]
			time.sleep(sleep_time)
			response = requests.get(url, headers=header)
			with open(file_path + pic_name, 'wb') as file1:
				file1.write(response.content)
				print('catch ' + pic_name)
