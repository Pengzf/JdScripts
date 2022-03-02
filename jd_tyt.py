#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JdScript / jd_tyt
活动名称: 推推赚大钱
Author: SheYu09
cron: 0 0 * * * jd_tyt.py
new Env('极速版 -*- 推一推')
'''
import requests, os
s = requests.session()
SheYu09 = 'https://raw.fastgit.org/SheYu09/JdScripts/main/'
try:
	from h5st import h5st
except:
	os.system(f'wget {SheYu09}h5st.so')
try:
	from jdCookie import *
except:
	os.system(f'wget {SheYu09}jdCookie.py')
from inspect import stack
from time import sleep, time
from json import dumps, loads
try:
	from GetJDUser import GetJDUser
except:
	os.system(f'wget {SheYu09}GetJDUser.so')
requests.packages.urllib3.disable_warnings()
body = {
	"actId": "49f40d2f40b3470e8d6c39aa4866c7ff",
	"channel": "coin_dozer",
	"antiToken":"",
	"referer":"-1",
	"frontendInitStatus":""
}
s.params = {
	'functionId': '',
	'appid': '',
	'client': 'H5',
	'clientVersion': '1.0.0',
	't': '',
	'body': {}
}
s.headers['Referer'] = 'https://pushgold.jd.com/'
s.headers['User-Agent'] = 'JDMobileLite/3.8.10 (iPhone; iOS 15.3; Scale/3.00)'

def jdcoupon():
	for i in ckList:
		s.headers['Cookie'] = i
		ck, levelName, nickName, userLevel = GetJDUser(s)
		if not ck:
			continue
		print(f"【用户{ckList.index(i)+1}（{nickName}）助力】{packetId}\n")
		s.headers['Cookie'] = ck
		helpCoinDozer()
		if helpCoin:
			if helpCoin['success']:
				print(f"帮砍：{helpCoin['data']['amount']}\n")
			else:
				print(helpCoin['msg'], "\n")
				code = helpCoin['code']
				if code in [99, 508, 705, 747]:
					continue
				elif code == 703:
					break
		else:
			continue
	sleep(10)

def JD_API_HOST():
	r = s.post('https://api.m.jd.com', verify=False)
	if r.content:
		return r.json()
	else:
		return 

def initiateCoinDozer():
	global initiate
	s.params['functionId'] = stack()[0][3]
	s.params['body'] = dumps(body)
	s.params['t'] = int(time()*1000)
	s.params['appid'] = 'megatron'
	initiate = JD_API_HOST()

def coinDozerBackFlow():
	global coinDozer
	s.params['functionId'] = stack()[0][3]
	s.params['t'] = int(time()*1000)
	coinDozer = JD_API_HOST()

def getCoinDozerInfo():
	global getCoin
	s.params['functionId'] = stack()[0][3]
	s.params['body'] = dumps(body)
	s.params['t'] = int(time()*1000)
	s.params['appid'] = 'megatron'
	getCoin = JD_API_HOST()

def helpCoinDozer():
	global helpCoin
	s.params['functionId'] = stack()[0][3]
	body['packetId'] = packetId
	s.params['body'] = dumps(body)
	s.params['t'] = int(time()*1000)
	s.params['_stk'] = 'appid,body,client,clientVersion,functionId,t'
	s.params['h5st'] = h5st('10005')
	s.params['appid'] = 'station-soa-h5'
	helpCoin = JD_API_HOST()

def start():
	global packetId, ckList
	print("🔔推推赚大钱, 开始!\n")
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
		initiateCoinDozer() # 活动开启
		if initiate['success']:
			packetId = initiate['data']['packetId']
			coinDozerBackFlow() # 逛会场
		elif initiate['code'] == 703:
			print("已完成砍价\n")
			continue
		elif initiate['code'] == 66:
			print(initiate['msg'])
			exit()
		else:
			if initiate['code'] == 508:
				print(initiate['msg'], "\n")
				continue
			getCoinDozerInfo() # 参数
			if getCoin['success']:
				packetId = getCoin['data']['sponsorActivityInfo']['packetId']
		print(f"【京东账号{ckNum+1}（{nickName}）的推一推好友互助码】{packetId}\n")
		if not packetId:
			print(f"【京东账号{ckNum+1}（{nickName}）】获取互助码失败。请稍后再试！\n")
			continue
		jdcoupon()

if __name__ == '__main__':
	start()
