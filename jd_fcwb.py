#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_fcwb
活动名称: 发财挖宝
Author: SheYu09
cron: 0 0 * * * jd_fcwb.py
new Env('极速版 -*- 发财挖宝')
'''
import requests, os
s = requests.session()
SheYu09 = 'https://raw.gh.fakev.cn/SheYu09/JdScripts/main/'
try: from GetJDUser import *
except: os.system(f'wget {SheYu09}GetJDUser.so')
requests.packages.urllib3.disable_warnings()

def pop_ck():
	while len(Names) >= len(ckList): ckList.pop()
	return True

def JD_API_PARAMS():
	s.params = {
		'functionId': '',
		'body': '',
		't': '',
		'appid': 'activities_platform',
		'client': 'H5',
		'clientVersion': '1.0.0'
	}
	s.params['t'] = int(time()*1e3)
	s.headers['Referer'] = 'https://bnzf.jd.com/'
	s.headers['User-Agent'] = userAgent()

def JD_API_BODY():
	global body
	body = {
		'linkId': 'pTTvJeSTrpthgk9ASBVGsw'
	}

def JD_API_HOST():
	r = s.get('https://api.m.jd.com/', verify=False)
	return r.text if r.content else ''

def happyDigHome():
	global DigHomeinfo; JD_API_PARAMS()
	s.params['functionId'] = stack()[0][3]
	s.params['body'] = dumps(body, separators=(',', ':'))
	h5st('ce6c2'); DigHomeinfo = JD_API_HOST()

def happyDigDo(round, rowIdx, colIdx):
	global DigDoinfo; JD_API_PARAMS(); JD_API_BODY()
	s.params['functionId'] = stack()[0][3]
	body['round'] = round
	body['rowIdx'] = rowIdx
	body['colIdx'] = colIdx
	s.params['body'] = dumps(body, separators=(',', ':'))
	DigDoinfo = JD_API_HOST()

def happyDigHelpList():
	global DigHelpListinfo; JD_API_PARAMS(); JD_API_BODY()
	s.params['functionId'] = stack()[0][3]
	body['pageNum'] = 1
	body['pageSize'] = 50
	s.params['body'] = dumps(body, separators=(',', ':'))
	DigHelpListinfo = JD_API_HOST()

def happyDigHelp(inviter, inviteCode):
	global DigHelpinfo; JD_API_PARAMS(); JD_API_BODY()
	s.params['functionId'] = stack()[0][3]
	body['inviter'] = inviter
	body['inviteCode'] = inviteCode
	s.params['body'] = dumps(body, separators=(',', ':'))
	h5st('8dd95'); DigHelpinfo = JD_API_HOST()

def BoostCode(i):
	s.headers['Cookie'] = i
	if GetJDUser(): return
	JD_API_BODY(); happyDigHome(); DigTreasure(i); happyDigHelpList(); inviter = re_key('"markedPin":"(.*?)"', DigHomeinfo); inviteCode = re_key('"inviteCode":"(.*?)"', DigHomeinfo); personNum = int(re_key('"personNum":(.*?),', DigHelpListinfo)); inviterList.append(inviter); inviteCodeList.append(inviteCode); personNumList.append(personNum)
	print(f"inviter: {inviter}\ninviteCode: {inviteCode}\n邀请人数: {personNum}\n"); sleep(s.t)

def HelpFriends(i):
	inviter, inviteCode, personNum = inviterList[0], inviteCodeList[0], personNumList[0]
	if [inviterList.remove(inviter), inviteCodeList.remove(inviteCode), personNumList.pop(0)][2] if personNum >= 40 and len(inviteCodeList) != 1 else pop_ck() if personNum >= 40 and len(inviteCodeList) == 1 else '': return
	s.headers['Cookie'] = i
	if GetJDUser(): return
	print(f"【用户{ckList.index(i)+1}（{s.nickName}）助力】{inviter}\n"); happyDigHelp(inviter, inviteCode); errMsg = re_key('"errMsg":"(.*?)"', DigHelpinfo); print(errMsg, "\n")
	if errMsg == 'success': personNumList[0] += 1; print(f"邀请人数: {personNum+1}\n")
	sleep(s.t)

def DigTreasure(i):
	s.headers['Cookie'] = i
	if GetJDUser(): return
	print(f"开始挖宝【京东账号{ckList.index(i)+1}】{s.userLevel}级 {s.levelName}: {s.nickName}\n")
	break_info = False
	for round in range(3):
		JD_API_BODY(); body['round'] = round+1; happyDigHome(); DigHome = loads(re_key('"roundList":(\[.*?\]),', DigHomeinfo), strict=False)[round]
		if DigHome['state'] != 0: continue
		for i in DigHome['chunks']:
			if i['type']: continue
			happyDigDo(round+1, i['rowIdx'], i['colIdx']); errMsg = re_key('"errMsg":"(.*?)"', DigDoinfo); print(errMsg, "\n")
			if '生命值' in errMsg or '不一致' in errMsg: break_info = True; break
			type = re_key('"type":(.*?),', DigDoinfo)
			value = re_key('"value":"(.*?)"', DigDoinfo) if type != '4' else '💣'
			type = type == '1' and '优惠卷' or type == '2' and '京东红包' or type == '3' and '微信红包' or type == '4' and '炸弹'
			print(f"挖到{type}: {value}\n"); sleep(s.t)
		if break_info: break

def start():
	global Names, ckList, inviterList, inviteCodeList, personNumList; print("🔔发财挖宝, 开始!\n"); inviterList, inviteCodeList, personNumList = list(), list(), list(); Names = Name(); ckList = jdCookie(); s.t = 5
	[BoostCode(c) for c in [c for c in ckList if re_pin(c) in Names]]
	inviterList and inviteCodeList and [HelpFriends(c) for c in ckList]
	[DigTreasure(c) for c in [c for c in ckList if re_pin(c) in Names]]

if __name__ == '__main__':
	start()
