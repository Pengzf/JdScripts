#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_zjb
活动名称: 赚金币助力
Author: SheYu09
cron: 0 0 * * * jd_zjb.py
new Env('极速版 -*- 赚金币助力')
'''
import requests
s = requests.session()
from jdCookie import *
from inspect import stack
from time import sleep, time
from threading import Thread
from json import dumps, loads
from GetJDUser import GetJDUser
requests.packages.urllib3.disable_warnings()
s.params = {
	'functionId': 'TaskInviteService',
	'body': {},
	'appid': 'market-task-h5',
	'uuid': '',
	'_t': '',
	
}
s.headers['Referer'] = 'https://gray.jd.com/'
s.headers['User-Agent'] = 'JDMobileLite/3.8.10 (iPhone; iOS 15.3; Scale/3.00)'

def Goldcoins():
	for i in ckList:
		s.headers['Cookie'] = i
		ck, levelName, nickName, userLevel = GetJDUser(s)
		if not ck:
			continue
		print(f"【用户{ckList.index(i)+1}（{nickName}）助力】{encryptionInviterPin}\n")
		s.headers['Cookie'] = ck
		participateInviteTask(encryptionInviterPin)
		if participate:
			try:
				if participate['isSuccess']:
					print(f"您也获得: {participate['data']['coinReward']}金币\n")
				else:
					message = participate['message']
					print(message, "\n")
			except Exception as e:
				print("participate:", e, "\n")
		sleep(2)

def JD_API_HOST():
	r = s.post('https://api.m.jd.com', verify=False)
	if r.content:
		return loads(r.text, strict=False)
	else:
		return 

def JD_API_BODY():
	global body
	body = {
		'method': '',
		'data': {
			'channel': '1'
		}
	}

def inviteTaskHomePage():
	global inviteTask
	JD_API_BODY()
	body['method'] = stack()[0][3]
	s.params['body'] = dumps(body)
	s.params['_t'] = int(time()*1000)
	inviteTask = JD_API_HOST()

def participateInviteTask(encryptionInviterPin):
	global participate
	JD_API_BODY()
	body['method'] = stack()[0][3]
	body['data']['encryptionInviterPin'] = encryptionInviterPin
	body['data']['type'] = 1
	s.params['body'] = dumps(body)
	s.params['_t'] = int(time()*1000)
	participate = JD_API_HOST()

def start():
	global encryptionInviterPin, ckList
	print("🔔赚金币助力, 开始!\n")
	ckList, pinList = jdCookie()
	for ckname in Name():
		try:
			ckNum = pinList.index(ckname)
		except:
			print(f"请检查被助力账号【{ckname}】名称是否正确？提示：助力名字填pt_pin的值。\n")
			continue
		s.headers['Cookie'] = ckList[ckNum]
		ck, levelName, nickName, userLevel = GetJDUser(s)
		if not ck:
			continue
		print(f"开始【京东账号{ckNum+1}】{userLevel}级 {levelName}: {nickName}\n")
		s.headers['Cookie'] = ck
		inviteTaskHomePage() # 获取助力码
		if inviteTask['isSuccess']:
			encryptionInviterPin = inviteTask['data']['encryptionInviterPin']
		else:
			print(f"【京东账号{ckNum+1}（{nickName}）】获取互助码失败。请稍后再试！\n")
			continue
		print(f"【京东账号{ckNum+1}（{nickName}）的赚金币好友互助码】{encryptionInviterPin}\n")
		Goldcoins()

if __name__ == '__main__':
	start()
