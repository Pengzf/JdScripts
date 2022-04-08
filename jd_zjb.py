#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_zjb
活动名称: 赚金币助力
Author: SheYu09
cron: 0 0 * * * jd_zjb.py
new Env('极速版 -*- 赚金币助力')
'''
import requests, os
s = requests.session()
SheYu09 = 'https://raw.gh.fakev.cn/SheYu09/JdScripts/main/'
try: from GetJDUser import *
except: os.system(f'wget {SheYu09}GetJDUser.so')
requests.packages.urllib3.disable_warnings()

def JD_API_HOST():
	r = s.post('https://api.m.jd.com/', verify=False)
	return r.text if r.content else ''

def JD_API_BODY():
	global body
	s.params = {
		'functionId': 'TaskInviteService',
		'body': {},
		'appid': 'market-task-h5',
		'uuid': ''
	}
	body = {
		'method': '',
		'data': {
			'channel': '1'
		}
	}
	s.params['_t'] = int(time()*1e3)
	s.headers['Referer'] = 'https://gray.jd.com/'
	s.headers['User-Agent'] = userAgent()

def inviteTaskHomePage():
	global inviteTask; JD_API_BODY()
	body['method'] = stack()[0][3]
	s.params['body'] = dumps(body)
	inviteTask = JD_API_HOST()

def participateInviteTask(e):
	global participate; JD_API_BODY()
	body['method'] = stack()[0][3]
	body['data']['encryptionInviterPin'] = e
	body['data']['type'] = 1
	s.params['body'] = dumps(body)
	participate = JD_API_HOST()

def BoostCode(i):
	s.headers['Cookie'] = i
	if GetJDUser(): return
	print(f"开始【京东账号{ckList.index(i)+1}】{s.userLevel}级 {s.levelName}: {s.nickName}\n"); inviteTaskHomePage(); encryptionInviterPin = re_key('"encryptionInviterPin":"(.*?)"', inviteTask); print(f"【京东账号{ckList.index(i)+1}（{s.nickName}）的赚金币好友互助码】{encryptionInviterPin}\n"); encryptionInviterPin and encryptionInviterPinList.append(encryptionInviterPin)

def Goldcoins(i, e):
	s.headers['Cookie'] = i
	if GetJDUser(): return
	print(f"【用户{ckList.index(i)+1}（{s.nickName}）助力】{e}\n"); participateInviteTask(e); coinReward = re_key('"coinReward":(.*?)\}', participate)
	(coinReward and [print(f"您也获得: {coinReward}金币\n")] or [print(re_key('"message":"(.*?)"', participate), "\n")])[0]
	sleep(s.t)

def start():
	global Names, ckList, encryptionInviterPin, encryptionInviterPinList; print("🔔赚金币助力, 开始!\n"); encryptionInviterPinList = list(); Names = Name(); ckList = jdCookie(); s.t = 1
	[BoostCode(c) for c in [c for c in ckList if re_pin(c) in Names]]
	encryptionInviterPinList and [Goldcoins(c, e) for e in encryptionInviterPinList for c in ckList]

if __name__ == '__main__':
	start()
