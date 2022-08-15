import os
import time
import imageio
import requests
import zipfile


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


def make_gif_from_zip(path_aim, path_zip, gif_name, duration, path_gif):
	# 作用：解压相应位置的压缩包，并且加压到对应位置,同时对该对应位置的文件夹内的图片进行gif制作
	# 参数：压缩包位置，解压文件夹位置,gif名称,帧速,gif放置位置
	z = zipfile.ZipFile(path_zip, 'r')
	for p in z.namelist():
		z.extract(p, path_aim)
	z.close()
	pic_list = os.listdir(path_aim)
	gif_images = []
	for name in pic_list:
		filename = os.path.join(path_aim, name)
		gif_images.append(imageio.imread(filename))
	os.makedirs(path_gif, exist_ok=True)
	imageio.mimsave(path_gif + '\\' + gif_name, gif_images, "GIF", duration=duration)


