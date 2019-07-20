# -*- coding: utf-8 -*-
"""
音乐下载器类
@author: syj
"""
import sys
from platforms import kuwo
class MusicDownloader():
	def __init__(self, **kwargs):
		self.INFO = '''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
操作帮助:
	输入r: 返回主菜单(即重新选择平台号)
	输入q: 退出程序
	其他: 选择想要下载的歌曲时,输入{1,2,5}可同时下载第1,2,5首歌
歌曲保存路径:
	当前路径下的results文件夹内
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
		self.RESOURCES = '酷我音乐'
		self.platform_now_name = None
	'''外部调用'''
	def run(self):
		self.platform_now,self.platform_now_name = self.__Platform()
		while True:
			print(self.INFO)
			self.__userSearch()
	def __Platform(self):
			print('支持的平台:\n',self.RESOURCES)
			return kuwo.kuwo(), 'kuwo'
	'''用户搜索操作'''
	def __userSearch(self):
		songname = self.__input(' 请输入歌曲名或者歌手名 --> ' )
		if songname is None:
			return
		results = self.platform_now.get(mode='search', songname=songname)
		if len(results) == 0:
			print('未检索到歌曲%s的相关信息, 请重新输入:' % songname)
			return
		while True:
			print(' 搜索结果如下 -->')
			for idx, result in enumerate(sorted(results.keys())):
				print('[%d]. %s' % (idx+1, result))
			need_down_numbers = self.__input(' 请输入需要下载的歌曲编号(1-%d) --> ' % (len(results.keys())))
			if need_down_numbers is None:
				return
			need_down_numbers = need_down_numbers.split(',')
			numbers_legal = [str(i) for i in range(1, len(results.keys())+1)]
			error_flag = False
			for number in need_down_numbers:
				if number not in numbers_legal:
					print('<ERROR>--歌曲号输入有误, 请重新输入--<ERROR>')
					error_flag = True
					break
			if error_flag:
				continue
			need_down_list = []
			for number in need_down_numbers:
				need_down_list.append(sorted(results.keys())[int(number)-1])
			break
		return self.__download(need_down_list)
	'''下载用户选择的歌曲'''
	def __download(self, need_down_list):
		return self.platform_now.get(mode='download', need_down_list=need_down_list)
	'''处理用户输入'''
	def __input(self, tip=None):
		if tip is None:
			user_input = input()
		else:
			user_input = input(tip)
		if user_input.lower() == 'q':
			print('Bye...')
			sys.exit(-1)
		elif user_input.lower() == 'r':
			self.platform_now, self.platform_now_name = self.__Platform()
			return None
		else:
			return user_input
if __name__ == '__main__':
	try:
		MusicDownloader().run()
	except KeyboardInterrupt:
		print('Bye...')
		sys.exit(-1)