#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JdScript / jdCookie
活动名称: 读取COOKIE / WSKEY
Author: SheYu09
'''
import re
from os import environ
from inspect import stack
from time import strftime, localtime

def Name():
	try:
		if len(environ["Name"]):
			Name = environ["Name"].split('&')
			print("已获取并使用Env环境 Name:", Name, "\n")
			return Name
	except:
		print("自行添加环境变量：Name, 不同好友中间用&符号隔开\n")
		exit()

def JD_API_HOST(C):
	try:
		if len(environ[f'JD_{C}']):
			print(f"   ****** 已获取并使用Env环境 {C} ******\n")
			return environ[f'JD_{C}']
	except:
		print(f"   ****** 获取Env环境 {C} 失败 ******")
		print(f"自行添加环境变量：JD_{C}\n")
		return 

def COOKIE():
	global ptkeyList, ptpinList
	ck = JD_API_HOST(stack()[0][3])
	ptkeyList = re.split('&|\n', ck) if ck else ''
	ptpinList = re.compile(r'pin=(.*?);').findall(ck) if ck else ''

def WSKEY():
	global wskeyList, wspinList
	ck = JD_API_HOST(stack()[0][3])
	wskeyList = re.split('&|\n', ck) if ck else ''
	wspinList = re.compile(r'pin=(.*?);').findall(ck) if ck else ''

def jdCookie():
	COOKIE()
	WSKEY()
	if wskeyList and wspinList:
		ckNumList = []
		for i in wspinList:
			try:
				ckNum = ptpinList.index(i)
				ckNumList.append(ckNum)
			except:
				pass
		if ckNumList and ptkeyList:
			for i in ckNumList:
				ptkeyList.pop(i)
				ptpinList.pop(i)
	if ptkeyList and wskeyList:
		cookiesList = wskeyList + ptkeyList
		pinNameList = wspinList + ptpinList
	elif ptkeyList and not wskeyList:
		cookiesList = ptkeyList
		pinNameList = ptpinList
	elif not ptkeyList and wskeyList:
		cookiesList = wskeyList
		pinNameList = wspinList
	else:
		print("没有可用Cookie，已退出\n")
		exit()
	print(f"====================共{len(cookiesList)}个京东账号Cookie=====================\n")
	print(f"==================脚本执行- 北京时间(UTC+8)：{strftime('%Y-%m-%d %H:%M:%S', localtime())}==================\n")
	return cookiesList, pinNameList

