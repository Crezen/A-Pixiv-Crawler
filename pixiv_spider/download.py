import os
import time
import imageio
import requests
import zipfile


class Download:
	def __init__(self):
		pass

	def catch_pics(self, url_list, sleep_time, header, file_path):
		for url in url_list:
			file_name = url[url.rfind('/') + 1:-1]
			time.sleep(sleep_time)
			response = requests.get(url, headers=header)
			with open(file_path + file_name, 'wb') as file1:
				file1.write(response.content)
				print('catch ' + file_name)
			if file_name.find('.zip') != -1:
				self.create_gif(file_path + file_name, 0.06)
			os.remove(file_path + file_name)

	def create_gif(self, file_path, duration):
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
