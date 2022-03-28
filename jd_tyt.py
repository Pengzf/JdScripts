#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JdScript / jd_tyt
活动名称: 推推赚大钱
Author: SheYu09
cron: 1 0 * * * jd_tyt.py
new Env('极速版 -*- 推一推')
'''
import requests, os
s = requests.session()
SheYu09 = 'https://raw.fastgit.org/SheYu09/JdScripts/main/'
try:
	from h5st import h5st
except:
	os.system(f'wget {SheYu09}h5st.so')
from jdCookie import *
from re import compile
from inspect import stack
from time import sleep, time
from json import dumps, loads
try:
	from GetJDUser import GetJDUser
except:
	os.system(f'wget {SheYu09}GetJDUser.so')
try:
	from USER_AGENTS import userAgent
requests.packages.urllib3.disable_warnings()
body = {
	'actId': '49f40d2f40b3470e8d6c39aa4866c7ff',
	'channel': 'coin_dozer',
	'antiToken': '',
	'referer': '-1',
	'frontendInitStatus': ''
}
s.params = {
	'functionId': '',
	'appid': 'megatron',
	'client': 'H5',
	'clientVersion': '1.0.0',
	't': '',
	'body': {}
}
s.headers['Referer'] = 'https://pushgold.jd.com/'

def re_pin(r):
	try:
		return compile(r'pin=(.*?);wskey=.*?;').findall(r)[0]
	except:
		try:
			return compile(r'pt_key=.*?;pt_pin=(.*?);').findall(r)[0]
		except:
			print(r, '\nck格式不正确，请检查\n')

def re_key(r, e):
	try:
		return compile(rf'{r}').findall(e)[::-1][0]
	except:
		pass

def JD_API_HOST():
	s.headers['User-Agent'] = userAgent()
	r = s.post('https://api.m.jd.com', verify=False)
	return r.text if r.content else ''

def initiateCoinDozer():
	global initiate
	s.params['functionId'] = stack()[0][3]
	s.params['body'] = dumps(body, separators=(',', ':'))
	s.params['t'] = int(time()*1e3)
	initiate = JD_API_HOST()

def coinDozerBackFlow():
	global coinDozer
	s.params['functionId'] = stack()[0][3]
	s.params['body'] = dumps(body, separators=(',', ':'))
	s.params['t'] = int(time()*1e3)
	coinDozer = JD_API_HOST()

def getCoinDozerInfo():
	global getCoin
	s.params['functionId'] = stack()[0][3]
	s.params['body'] = dumps(body, separators=(',', ':'))
	s.params['t'] = int(time()*1e3)
	getCoin = JD_API_HOST()

def helpCoinDozer(packetId):
	global s, helpCoin
	s.params['functionId'] = stack()[0][3]
	body['packetId'] = packetId
	s.params['body'] = dumps(body, separators=(',', ':'))
	s.params['t'] = int(time()*1e3)
	s.params['appid'] = 'station-soa-h5'
	s = h5st(s, '10005')
	helpCoin = JD_API_HOST()

def BoostCode(i):
	s.headers['Cookie'] = i; ck, levelName, nickName, userLevel = GetJDUser(s)
	if not ck: return
	s.headers['Cookie'] = ck; print(f"开始【京东账号{ckList.index(i)+1}】{userLevel}级 {levelName}: {nickName}\n"); initiateCoinDozer(); msg = re_key('"msg":"(.*?)"', initiate); packetId = msg == 'OK' and [re_key('"packetId":"(.*?)"', initiate), coinDozerBackFlow(), sleep(3)][0] or '完成' in msg and '' or '重复' in msg and [getCoinDozerInfo(), re_key('"packetId":"(.*?)"', getCoin)][1]
	print(packetId, "\n") if msg in ['OK', '重复发起活动'] else print(msg, "\n")
	packetId and packetIdList.append(packetId)

def HelpFriends(i, packetId):
	s.headers['Cookie'] = i; ck, levelName, nickName, userLevel = GetJDUser(s)
	if not ck: return
	s.headers['Cookie'] = ck; print(f"【用户{ckList.index(i)+1}（{nickName}）助力】{packetId}\n"); helpCoinDozer(packetId)
	msg = re_key('"msg":"(.*?)"', helpCoin)
	amount = re_key('"amount":"(.*?)"', helpCoin) if msg == 'OK' else ''
	print(msg, amount, "\n")
	msg in ['已完成砍价', '排队帮砍'] and packetIdList.remove(packetId)
	sleep(10)

def start():
	global packetIdList, ckList; print("🔔推推赚大钱, 开始!\n"); packetIdList = list(); ckList = jdCookie(); [BoostCode(c) for c in [c for c in ckList if re_pin(c) in Name()]]
	packetIdList and [HelpFriends(c, packetId) for c in ckList for packetId in packetIdList]

if __name__ == '__main__':
	start()
