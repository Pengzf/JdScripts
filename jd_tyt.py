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
SheYu09 = 'https://raw.gh.fakev.cn/SheYu09/JdScripts/main/'
try:
	from GetJDUser import *
except:
	os.system(f'wget {SheYu09}GetJDUser.so')
requests.packages.urllib3.disable_warnings()

def pop_ck():
	while len(Names)+1 <= len(ckList): ckList.pop()
	return True

def JD_API_PARAMS():
	s.params = {
		'functionId': '',
		'appid': 'megatron',
		'client': 'H5',
		'clientVersion': '1.0.0'
	}
	s.params['t'] = int(time()*1e3); JD_API_BODY()
	s.params['body'] = dumps(body, separators=(',', ':'))
	s.headers['Referer'] = 'https://pushgold.jd.com/'
	s.headers['User-Agent'] = userAgent()

def JD_API_BODY():
	global body
	body = {
		'actId': '49f40d2f40b3470e8d6c39aa4866c7ff',
		'channel': 'coin_dozer',
		'antiToken': '',
		'referer': '-1',
		'frontendInitStatus': ''
	}

def JD_API_HOST():
	r = s.post('https://api.m.jd.com/', verify=False)
	return r.text if r.content else ''

def initiateCoinDozer():
	global initiate; JD_API_PARAMS()
	s.params['functionId'] = stack()[0][3]
	initiate = JD_API_HOST()

def coinDozerBackFlow():
	global coinDozer; JD_API_PARAMS()
	s.params['functionId'] = stack()[0][3]
	coinDozer = JD_API_HOST()

def getCoinDozerInfo():
	global getCoin; JD_API_PARAMS()
	s.params['functionId'] = stack()[0][3]
	getCoin = JD_API_HOST()

def helpCoinDozer(packetId):
	global helpCoin; JD_API_PARAMS()
	s.params['functionId'] = stack()[0][3]
	body['packetId'] = packetId
	s.params['body'] = dumps(body, separators=(',', ':'))
	s.params['appid'] = 'station-soa-h5'
	h5st('10005'); helpCoin = JD_API_HOST()

def BoostCode(i):
	s.headers['Cookie'] = i
	if GetJDUser(): return
	print(f"开始【京东账号{ckList.index(i)+1}】{s.userLevel}级 {s.levelName}: {s.nickName}\n"); initiateCoinDozer(); msg = re_key('"msg":"(.*?)"', initiate); packetId = msg == 'OK' and [re_key('"packetId":"(.*?)"', initiate), coinDozerBackFlow(), sleep(3)][0] or '完成' in msg and '' or '重复' in msg and [getCoinDozerInfo(), re_key('"packetId":"(.*?)"', getCoin)][1]
	print(packetId, "\n") if msg in ['OK', '重复发起活动'] else print(msg, "\n")
	packetId and packetIdList.append(packetId)

def HelpFriends(i):
	packetId = packetIdList[0]
	s.headers['Cookie'] = i
	if GetJDUser(): return
	print(f"【用户{ckList.index(i)+1}（{s.nickName}）助力】{packetId}\n"); helpCoinDozer(packetId)
	msg = re_key('"msg":"(.*?)"', helpCoin)
	amount = re_key('"amount":"(.*?)"', helpCoin) if msg == 'OK' else ''
	print(msg, amount, "\n")
	if packetIdList.pop(0) if msg in ['已完成砍价', '帮砍排队'] and len(packetIdList) != 1 else pop_ck() if msg in ['已完成砍价', '帮砍排队'] and len(packetIdList) == 1 else '': sleep(s.t); return
	sleep(s.t)

def start():
	global Names, ckList, packetIdList; print("🔔推推赚大钱, 开始!\n"); packetIdList = list(); Names = Name(); ckList = jdCookie(); s.t = 10
	[BoostCode(c) for c in [c for c in ckList if re_pin(c) in Names]]
	packetIdList and [HelpFriends(c) for c in ckList]

if __name__ == '__main__':
	start()
