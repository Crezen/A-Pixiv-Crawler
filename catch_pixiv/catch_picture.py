import os
import time
import imageio
import requests
import zipfile


def catch_pics(sleep_time, header, file_path):
	with open('D:\\Work\\Code\\learn_crawler\\catch_pixiv\\data.txt', 'r') as file:
		while True:
			url = file.readline()
			if url == '':
				break
			pic_name = url[url.rfind('/') + 1:-1]
			time.sleep(sleep_time)
			response = requests.get(url, headers=header)
			with open(file_path + pic_name, 'wb') as file1:
				file1.write(response.content)
				print('catch ' + pic_name)


def create_gif(file_path, duration):
	"""
		将目标压缩包解压为一组图片，并在同一文件夹下生成gif动图
        参数：压缩包名称（包含文件路径）, 帧速
    """
	# 去除.zip后形成一个文件夹路径
	dir_path = file_path[:-4]
	# 将zip解压至该文件夹下
	with zipfile.ZipFile(file_path, 'r') as file:
		for pic in file.namelist():
			file.extract(pic, dir_path)
	# 获取图片名称列表
	pic_list = os.listdir(dir_path)

	# 将这组图片生成gif
	frames = []
	for name in pic_list:
		filename = os.path.join(dir_path, name)
		frames.append(imageio.v3.imread(filename))
	gif_name = dir_path + '.gif'
	imageio.mimsave(gif_name, frames, duration=duration)

	# 删除之前解压生成的文件夹
	for file in os.listdir(dir_path):
		os.remove(dir_path + '\\' + file)
	os.removedirs(dir_path)
